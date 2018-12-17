from enum import Enum
from functools import reduce


class ExeTyp(Enum):
    Run = ('*ExeTyp*', 'Run')
    Check = ('*ExeTyp*', 'Check')


class RunTyp(Enum):
    Energy = ('*RunTyp*', 'Energy')
    Optimize = ('*RunTyp*', 'Optimize')
    Hessian = ('*RunTyp*', 'Hessian')


class Method(Enum):
    RHF = ('*Method*', '')
    DFT = ('*Method*', 'mplevl = 2')
    MP2 = ('*Method*', 'dfttyp = b3lyp')


class InputFiles(object):
    def __init__(self, template, gamess_command_path, gamess_string):
        self._template = template
        self._gamess_command_path = gamess_command_path
        self._gamess_string = gamess_string

    # def __init__(self, template_path):
    # with open(template_path, 'r') as file:
    #     self.template = file.read()

    def create_input(self, output_path, rule_list):
        out = self._template
        out = reduce(lambda a, kv: a.replace(*kv), rule_list, out)

        with open(output_path, 'w') as file:
            file.write(out)

    def create_run_command(self, output_path, input_file_name, output_file_name):
        # TODO: do it not only for windows
        # for windows:
        out = 'del restart\\*.dat\ndel restart\\*.rst\n@CALL {0} {1} {2} {3}'.format(self._gamess_command_path,
                                                                                     input_file_name,
                                                                                     self._gamess_string,
                                                                                     output_file_name)
        with open(output_path, 'w') as file:
            file.write(out)


class StructureParser(object):
    def __init__(self, structure_file_path):
        with open(structure_file_path, 'r') as file:
            input_structure = file.read().splitlines()

        if (not ('$DATA' in input_structure[0])) or (not ('$END' in input_structure[-1])):
            raise Exception('Incorrect data format')

        self.name_rule = ('*Name*', input_structure[1])
        structure_index = 3
        if 'C1' in input_structure[2]:
            self.symmetry_rule = ('*Symmetry*', 'C1')
        else:
            self.symmetry_rule = ('*Symmetry*', input_structure[2] + '\n' + input_structure[3])
            structure_index = 4

        # TODO: not nice solution
        geometry_lines = input_structure[structure_index+1:-1]
        geometry = input_structure[structure_index]
        for line in geometry_lines:
            geometry += '\n'
            geometry += line
        self.geometry_rule = ('*Geometry*', geometry)
