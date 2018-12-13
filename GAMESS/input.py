from enum import Enum
from functools import reduce

class ExeTyp(Enum):
    Run = ('*ExeTyp*','Run')
    Check = ('*ExeTyp*','Check')

class RunTyp(Enum):
    Energy = ('*RunTyp*','Energy')
    Optimize = ('*RunTyp*','Optimize')
    Hessian = ('*RunTyp*','Hessian')

class Method(Enum):
    RHF = ('*Method*','')
    DFT = ('*Method*','mplevl = 2')
    MP2 = ('*Method*','dfttyp = b3lyp')

class Input(object):
    def __init__(self, template_path):
        with open(template_path, 'r') as file:
            self.template = file.read()

    def Generate(self, output_path, rule_list):
        out = self.template
        out = reduce(lambda a, kv: a.replace(*kv), rule_list, out)

        with open(output_path, 'w') as file:
            file.write(out)

# input = InputFile('C:\\Users\\Public\\gamess-64\\template.inp')
# rule_list = ExeTyp.Run.value, Method.DFT.value, RunTyp.Optimize.value, ('*Name*', 'name'), ('*Symmetry*', 'C1'), ('*Geometry*', 'geometry')
# input.Generate('C:\\Users\\Public\\gamess-64\\output.inp', rule_list)
