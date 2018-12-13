import input

class Calculate(object):
    def __init__(self, structure_file_path, template, gamess_command_path, gamess_string):
        self.template = template
        self.gamess_command_path = gamess_command_path
        self.gamess_string = gamess_string
        with open(structure_file_path, 'r') as file:
            self.input_structure = file.read()
        
    def CheckOptimizeHessian(self, input_structure_path, method):

        # parse structure file
        name = ''
        symmetry = ''
        geometry = ''

        name_rule = ('*Name*', name)
        symmetry_rule = ('*Symmetry*', symmetry)
        geometry_rule = ('*Geometry*', geometry)

        inp = input.InputFiles(template, )
        # create check input
        pass


# run check

# check

# create optimize input

# run optimize

# check

# get optimized configuration

# create hessian input

# run hessian

# check

# get optimized configuration
