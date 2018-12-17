import calculate
import inputfiles


list1 = ['1', '2', '3', '4']

list0 = list1[2:3]

calculate_method = calculate.Calculate('template.inp', 'gamess.exe', '1 2')
calculate_method.run('struct.inp', 'folder', 'filename', inputfiles.Method.DFT)
