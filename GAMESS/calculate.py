import inputfiles
import subprocess
import os
import shutil


class Calculate(object):
    def __init__(self, template, gamess_command_path, gamess_string):
        with open(template, 'r') as file:
            self.template = file.read()
        self.gamess_command_path = gamess_command_path
        self.gamess_string = gamess_string
        self.input = inputfiles.InputFiles(self.template, self.gamess_command_path, self.gamess_string)

    def single_run(self, input_file_path, output_file_path, cmd_file_path, rule_list):
        # create input files
        self.input.create_input(input_file_path, rule_list)
        self.input.create_run_command(cmd_file_path, input_file_path, output_file_path)

        # run
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

    def run(self, structure_file_path, working_folder, file_name, method, charge=('*Charge*','0')):
        if not os.path.exists(structure_file_path):
            raise FileNotFoundError("structure_file_path")
        if os.path.isdir(working_folder):
            shutil.rmtree(working_folder, ignore_errors=True)
        os.makedirs(working_folder)

        # TODO: move parsing to a separate module
        # parse structure file
        with open(structure_file_path, 'r') as file:
            input_structure = file.read().splitlines()

        if (not ('$DATA' in input_structure[0])) or (not ('$END' in input_structure[-1])):
            raise Exception('Incorrect data format')

        name_rule = ('*Name*', input_structure[1])

        structure_index = 3
        if 'C1' in input_structure[2]:
            symmetry_rule = ('*Symmetry*', 'C1')
        else:
            symmetry_rule = ('*Symmetry*', input_structure[2] + '\n' + input_structure[3])
            structure_index = 4

        # TODO: not nice solution
        geometry_lines = input_structure[structure_index+1:-1]
        geometry = input_structure[structure_index]
        for line in geometry_lines:
            geometry += '\n'
            geometry += line
        geometry_rule = ('*Geometry*', geometry)

        cmd_file_path = os.path.join(working_folder, 'run.bat')
        input_file_path = self.path(working_folder, file_name, method, 'inp')

        # run check
        output_file_path = self.path(working_folder, file_name, method, 'check')
        rule_list = inputfiles.ExeTyp.Check.value, method.value, charge,\
                    inputfiles.RunTyp.Energy.value, name_rule, symmetry_rule, geometry_rule
        self.single_run(input_file_path, output_file_path, cmd_file_path, rule_list)

        # check

        # run optimize
        output_file_path = self.path(working_folder, file_name, method, 'opt')
        rule_list = inputfiles.ExeTyp.Run.value, method.value, charge,\
                    inputfiles.RunTyp.Optimize.value, name_rule, symmetry_rule, geometry_rule
        self.single_run(input_file_path, output_file_path, cmd_file_path, rule_list)

        # TODO: use optimized geometry
        geometry_rule = ('*Geometry*', 'geometry')

        # run hessian
        output_file_path = self.path(working_folder, file_name, method, 'hess')
        rule_list = inputfiles.ExeTyp.Run.value, method.value, charge, \
                    inputfiles.RunTyp.Hessian.value, name_rule, symmetry_rule, geometry_rule
        self.single_run(self, input_file_path, output_file_path, cmd_file_path, rule_list)
