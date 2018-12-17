import inputfiles
import subprocess


class Calculate(object):
    def __init__(self, structure_file_path, template, gamess_command_path, gamess_string):
        self.template = template
        self.gamess_command_path = gamess_command_path
        self.gamess_string = gamess_string
        self.input = inputfiles.InputFiles()
        with open(structure_file_path, 'r') as file:
            self.input_structure = file.read()

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

    def run(self, file_name, folder, method):
        # TODO: parse structure file
        name_rule = ('*Name*', 'name')
        symmetry_rule = ('*Symmetry*', 'C1')
        geometry_rule = ('*Geometry*', 'geometry')

        # run check
        rule_list = inputfiles.ExeTyp.Check.value, method, inputfiles.RunTyp.Energy.value, name_rule, symmetry_rule, geometry_rule
        input_file_path = ''
        output_file_path = ''
        cmd_file_path = ''
        self.single_run(self, input_file_path, output_file_path, cmd_file_path, rule_list)

        # check

        # run optimize
        rule_list = inputfiles.ExeTyp.Run.value, method, inputfiles.RunTyp.Optimize.value, name_rule, symmetry_rule, geometry_rule
        input_file_path = ''
        output_file_path = ''
        cmd_file_path = ''
        self.single_run(self, input_file_path, output_file_path, cmd_file_path, rule_list)

        # run hessian
        geometry_rule = ('*Geometry*', 'geometry')  # TODO: read from optimized file
        rule_list = inputfiles.ExeTyp.Run.value, method, inputfiles.RunTyp.Hessian.value, name_rule, symmetry_rule, geometry_rule
        input_file_path = ''
        output_file_path = ''
        cmd_file_path = ''
        self.single_run(self, input_file_path, output_file_path, cmd_file_path, rule_list)
        
