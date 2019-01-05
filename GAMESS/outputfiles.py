

class OutputParser(object):
    @staticmethod
    def get_unique_optimized_geometry(data):
        start_position = data.find('EQUILIBRIUM GEOMETRY LOCATED')
        end_position = data.find('COORDINATES OF ALL ATOMS ARE (ANGS)', start_position)
        structure_lines = data[start_position:end_position].splitlines()[4:-1]
        return structure_lines

    @staticmethod
    def get_all_optimized_geometry(data):
        start_position = data.find('EQUILIBRIUM GEOMETRY LOCATED')
        start_position = data.find('COORDINATES OF ALL ATOMS ARE (ANGS)', start_position)
        end_position = data.find('INTERNUCLEAR DISTANCES', start_position)
        structure_lines = data[start_position:end_position].splitlines()[3:-2]
        return structure_lines

    @staticmethod
    def get_unique_optimized_geometry_rule(file_path):
        with open(file_path, 'r') as file:
            data = file.read()
        structure_lines = OutputParser.get_unique_optimized_geometry(data)
        if len(structure_lines) == 0:
            structure_lines = OutputParser.get_all_optimized_geometry(data)
        if len(structure_lines) == 0:
            raise Exception('no any geometry lines in file')
        # TODO: not nice solution
        geometry = ''
        for line in structure_lines[1:-2]:
            geometry += line
            geometry += '\n'
        geometry += structure_lines[-1]
        geometry_rule = ('*Geometry*', geometry)

        return geometry_rule
