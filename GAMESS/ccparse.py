from cclib.parser import GAMESS


filename = "\\\\gamestation\\gamess-64\\CF3SO3_CH3CN_n_smd\\C3NH3SO3F3_2\\C3NH3SO3F3_2.DFT.hess"
file = GAMESS(filename)
data = file.parse()
attributes = data.getattributes()
#data = cclib.io.ccread(filename)
print("There are %i atoms and %i MOs" % (data.natom, data.nmo))
