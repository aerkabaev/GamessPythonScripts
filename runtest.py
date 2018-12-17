import calculate
import inputfiles


calculate_method = calculate.Calculate('template.inp', 'gamess.exe', '1 2')
calculate_method.run('struct.inp', 'folder', 'filename', inputfiles.Method.DFT)
