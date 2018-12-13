from input import Input

class Calculate(object):
    def __init__(self, structure_file_path, template):
        self.template = template
        with open(structure_file_path, 'r') as file:
            self.input_structure = file.read()
        
# create check input

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
