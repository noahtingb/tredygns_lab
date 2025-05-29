import matplotlib.pyplot as plt
import linje_funktioner
import kvant
import numpy as np

name = "matning 6 - Na"
data=kvant.loada()
x = data[name+"_x"]
y = data[name+"_y"]
plt.plot(x,y, alpha = 0.5)
ymax = np.max(y)


wl, intens = linje_funktioner.NIST_spektrum("Na",ymax)
intens = intens.fillna(0)/ymax
plt.vlines(wl, 0,intens, color = "orange", alpha = intens)
plt.xlim(580,600)
plt.semilogy()
plt.show()