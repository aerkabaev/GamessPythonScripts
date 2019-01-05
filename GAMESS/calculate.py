import inputfiles
import subprocess
import os
import shutil
import outputfiles


class Calculate(object):
    def __init__(self, template, gamess_path, gamess_command, gamess_parameters):
        with open(template, 'r') as file:
            self.template = file.read()
        self._gamess_path = gamess_path
        self._input = inputfiles.InputFiles(self.template, gamess_path, gamess_command, gamess_parameters)

    def single_run(self, input_file_path, output_file_path, cmd_file_path, rule_list):
        # create input files
        self._input.create_input(input_file_path, rule_list)
        self._input.create_run_command(cmd_file_path, input_file_path, output_file_path)

        # run
        # requirement of GAMESS-US for windows: to be started in GAMESS working folder:
        os.chdir(self._gamess_path)
        subprocess.check_call(cmd_file_path, shell=True)

        # check
        with open(output_file_path, 'r') as file:
            f = file.read()
            success = 'EXECUTION OF GAMESS TERMINATED NORMALLY' in f

        if not success:
            raise Exception('Calculation error')

    @staticmethod
    def path(working_folder, file_name, method, ext):
        out = os.path.join(working_folder, file_name)
        out += '.' + method.name + '.' + ext
        return out

    def run(self, structure_file_path, working_folder, file_name, method, charge):
        if not os.path.exists(structure_file_path):
            raise FileNotFoundError("structure_file_path")
        # TODO: clear the folder, don't delete it
        if not os.path.isdir(working_folder):
            os.makedirs(working_folder)

        # parse structure file
        structure_file = inputfiles.StructureParser(structure_file_path)
        name_rule = structure_file.name_rule
        symmetry_rule = structure_file.symmetry_rule
        geometry_rule = structure_file.geometry_rule
        charge_rule = ('*Charge*', charge)

        # input file must be in gamess folder. facepalm
        cmd_file_path = os.path.join(working_folder, 'run.bat')
        input_file_path = self.path(self._gamess_path, file_name, method, 'inp')

        # run check
        output_file_path = self.path(working_folder, file_name, method, 'check')
        if not os.path.exists(output_file_path):
            rule_list = inputfiles.ExeTyp.Check.value, method.value, charge_rule,\
                        inputfiles.RunTyp.Energy.value, name_rule, symmetry_rule, geometry_rule
            self.single_run(input_file_path, output_file_path, cmd_file_path, rule_list)

        # run optimize
        output_file_path = self.path(working_folder, file_name, method, 'opt')
        if not os.path.exists(output_file_path):
            rule_list = inputfiles.ExeTyp.Run.value, method.value, charge_rule,\
                        inputfiles.RunTyp.Optimize.value, name_rule, symmetry_rule, geometry_rule
            self.single_run(input_file_path, output_file_path, cmd_file_path, rule_list)

        # run hessian
        output_file_path = self.path(working_folder, file_name, method, 'hess')
        if not os.path.exists(output_file_path):
            geometry_rule = outputfiles.OutputParser.get_unique_optimized_geometry_rule(output_file_path)
            rule_list = inputfiles.ExeTyp.Run.value, method.value, charge_rule, \
                        inputfiles.RunTyp.Hessian.value, name_rule, symmetry_rule, geometry_rule
            self.single_run(input_file_path, output_file_path, cmd_file_path, rule_list)
