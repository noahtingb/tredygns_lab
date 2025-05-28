import matplotlib.pyplot as plt
import linje_funktioner
import kvant

name = "matning 6 - Na"
data=kvant.loada()
plt.plot(data[name+"_x"],data[name+"_y"])

wl, intens = linje_funktioner.NIST_spektrum("Na",6e-7)
plt.vlines(wl-1.1, 0,intens, color = "orange")
plt.xlim(587,590)
plt.semilogy()
plt.show()