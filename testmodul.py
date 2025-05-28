import matplotlib.pyplot as plt
import linje_funktioner
import kvant
import numpy as np

name = "Matning 5.1 - Cd"
data=kvant.loada()
x = data[name+"_x"]
y = data[name+"_y"]
plt.plot(x,y, alpha = 0.5)
ymax = np.max(y)


wl, intens = linje_funktioner.NIST_spektrum("Ne",ymax)
intens = intens.fillna(0)/ymax
plt.vlines(wl-1.1, 0,intens, color = "orange", alpha = intens)
plt.xlim(640,660)
plt.semilogy()
plt.show()