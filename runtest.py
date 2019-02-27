import calculate
import inputfiles
import os
import outputfiles


def list_files(directory, extension):
    return (f for f in os.listdir(directory) if f.endswith('.' + extension))

calculate_method = calculate.Calculate('template.inp', 'C:\\Users\\Public\\gamess-64\\', 'rungms.bat',
                                       '2018-R1-pgi-mkl 4 0')
main_dir = 'C:\\Users\\Public\\gamess-64\\CF3SO3_CH3CN_n\\'
files = files = list_files(main_dir, "txt")

for file in files:
    name = os.path.splitext(file)[0]
    sub_dir = os.path.join(main_dir, name)
    try:
        calculate_method.run(os.path.join(main_dir, file), sub_dir, name, inputfiles.Method.DFT, '-1')
    except:
        pass
    try:
        calculate_method.run(os.path.join(main_dir, file), sub_dir, name, inputfiles.Method.MP2, '-1')
    except:
        pass
