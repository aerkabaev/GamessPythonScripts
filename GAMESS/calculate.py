import inputfiles
import subprocess


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

    def run(self, structure_file_path, folder, method):
        # TODO: parse structure file
        with open(structure_file_path, 'r') as file:
            input_structure = file.readlines()

        if (not ('$DATA' in input_structure[0])) or (not ('$END' in input_structure[-1])):
            raise Exception('Incorrect data format')

        name_rule = ('*Name*', input_structure[1])

        structure_index = 4
        if 'C1' in input_structure[3]:
            symmetry_rule = ('*Symmetry*', 'C1')
        else:
            symmetry_rule = ('*Symmetry*', input_structure[3] + input_structure[4])
            structure_index = 5

        geometry_rule = ('*Geometry*', input_structure[structure_index::-2])

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

