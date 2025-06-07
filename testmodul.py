import matplotlib.pyplot as plt
import linje_funktioner as lf
import kvant
import numpy as np
import kalibrering as ka
from scipy.signal import find_peaks

name = 'Matning 5.2 - Na'
data=kvant.loada()
x = data[name+"_x"]
y = data[name+"_y"]
x = ka.adjust(np.array(x))

ymax = np.max(y)



wl2, intens = lf.NIST_spektrum(lf.get_lines("Na", minint=1, typ="I"),ymax)

wl, _ = find_peaks(y, threshold=1e-10)
wl = np.array(x)[wl]

plt.vlines(wl2, 0, 1e-6, color = "green")
#plt.vlines(wl, 0,10e-8, color = "orange")
plt.plot(x,y)
#plt.xlim(600,800)
#plt.ylim(0,1e-8)
plt.semilogy()
plt.show()

"""data=kvant.loada(name = "jsons\\res.json")

namn = "Matning 9 - H"
midx = np.array([entry['midx'] for entry in data[namn]])
#lf.auto_assigner(midx, lf.get_lines("H", minint=1, typ="I"))"""