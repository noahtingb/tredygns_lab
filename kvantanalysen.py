import numpy as np
from scipy.optimize import curve_fit
import json
import matplotlib.pyplot as plt

def fitpeak(x, y, minpoint, maxpoint):
    """Find a peak by fitting a Gaussian to data

    Parameters
    ----------
    x
        x values of the data (channel number or energy)
    y
        y values of the data (number of counts)
    minpoint
        Left edge of region where fitting is performed. (Channel number
        if x are a channel numbers, energy if x are energies)
    maxpoint
        Right edge of region where fitting is performed. (Channel number
        if x are a channel numbers, energy if x are energies)

    Returns
    -------
    Tuple (mid, fity, fitx) where mid is the center of the Gaussian
    (channel number if x are channel numbers, energy if x
    are energies), fity are the y-values of the fitted
    Gaussian, and fitx the corresponding x values.

    """

    def gauss(x, amplitude, x0, sigma):
        y = np.exp(-0.5 * ((x - x0) / sigma) ** 2)
        return amplitude * y

    Range = [i for i in range(len(x)) if minpoint < x[i] < maxpoint]
    X_range = x[Range]
    Y_range = y[Range]

    # Reasonable initial guesses of the parameters
    initial = [np.max(Y_range), np.mean(X_range), (X_range[1] - X_range[0]) / 2]

    popt, _ = curve_fit(gauss, X_range, Y_range, p0=initial)
    amplitude, x0, sigma = popt
    mid = x0
    fity = gauss(X_range, amplitude, x0, sigma)
    fitx = X_range

    return mid, fity, fitx
def dumpa(name="jsons\\kvant.json",result=None):
    with open(name, 'w') as f:
        json.dump(result,f)
def loada(name="jsons\\kvant.json"):
    with open(name,"r") as f:
        return json.load(f)

def plotaone(data):
    nonames=['Dag1 matning2']
    names=['Dag1 matningar', 'Dag1 Matning 3.1', 'Dag1 Matning 3.2', 'Matning 4 -Cd', 'Matning 5.1 - Cd', 'Matning 5.2 - Na', 'matning 6 - Na', 'Matning 7 - Na', 'Matning 8 - H', 'Matning 9 - H']
    for name in names:
        plt.title(name)
        print(name,np.argmax(np.array(data[name+"_y"])))
        plt.plot(data[name+"_x"],data[name+"_y"])
        plt.show()

#data=loada()
#plotaone(data)