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
        self.template = template
        self.gamess_command_path = gamess_command_path
        self.gamess_string = gamess_string

    # def __init__(self, template_path):
    # with open(template_path, 'r') as file:
    #     self.template = file.read()

    def create_input(self, output_path, rule_list):
        out = self.template
        out = reduce(lambda a, kv: a.replace(*kv), rule_list, out)

        with open(output_path, 'w') as file:
            file.write(out)

    def create_run_command(self, output_path, input_file_name, output_file_name):
        # for windows:
        out = 'del restart\\*.dat \n del restart\\*.rst \n @CALL %s %s %s %s'.format(self.gamess_command_path,
                                                                                     input_file_name,
                                                                                     self.gamess_string,
                                                                                     output_file_name)
        with open(output_path, 'w') as file:
            file.write(out)