import calculate
import inputfiles


calculate_method = calculate.Calculate('template.inp', 'C:\\Users\\Public\\gamess-64\\', 'rungms.bat',
                                       '2016-pgi-linux-mkl 4 0')
calculate_method.run('struct.inp', 'C:\\Users\\Public\\gamess-64\\folder', 'filename', inputfiles.Method.DFT)
