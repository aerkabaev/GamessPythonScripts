

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
        for line in structure_lines[0:-1]:
            geometry += line
            geometry += '\n'
        geometry += structure_lines[-1]
        geometry_rule = ('*Geometry*', geometry)

        return geometry_rule

    @staticmethod
    def get_energy(data):
        start_position = data.find('IVIB=   0')
        start_position = data.find('E=    ', start_position)+4
        end_position = data.find('\n', start_position)
        energy = float(data[start_position:end_position])
        return energy

    @staticmethod
    def get_vibrations(data):
        start_position = data.find('MODE FREQ(CM**-1)  SYMMETRY  RED. MASS  IR INTENS.')
        end_position = data.find('THERMOCHEMISTRY', start_position)
        freq_lines = data[start_position:end_position].splitlines()[0:-2]

        # TODO: not nice solution
        freqs = ''
        for line in freq_lines:
            freqs += line
            freqs += '\n'

        return freqs

