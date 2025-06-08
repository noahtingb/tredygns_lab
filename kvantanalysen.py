import numpy as np
from scipy.optimize import curve_fit
import json
import matplotlib.pyplot as plt

def fitpeak(x, y, minpoint, maxpoint):
    if minpoint==maxpoint:
        return x[minpoint],np.array([y[minpoint]]),np.array([x[minpoint]])
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

    X_range = np.array(x[minpoint:maxpoint+1])
    Y_range = np.array(y[minpoint:maxpoint+1])

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
    #valuesfit=loada("jsons\\values.json")
    #for i in names:
    #    valuesfit[i]={["mid":0, "fity":[], "fitx":[]]}
    fitaround=loada("jsons\\values.json")
    fitaroundres=loada("jsons\\res.json")
    #dumpa("jsons\\values.json",fitaround)
    #dumpa("jsons\\res.json",fitaroundres)
    names=['Matning 5.1 - Cd']
    for name in names:
        #fitaround[name]=[{"mid":955,"size":2},{"mid":1086,"size":2},{"mid":1326,"size":2},{"mid":1845,"size":3},{"mid":1914,"size":2},{"mid":1921,"size":3},
        #                 {"mid":2312,"size":3},{"mid":2797,"size":3},{"mid":3019,"size":3},{"mid":3122,"size":3},{"mid":3145,"size":3},{"mid":3549,"size":4},
        #                 {"mid":3620,"size":3},{"mid":3729,"size":3},{"mid":3988,"size":3},{"mid":4060,"size":3},{"mid":4138,"size":3},{"mid":4765,"size":3},
        #                 {"mid":4930,"size":3},{"mid":5192,"size":3},{"mid":5435,"size":3},{"mid":5670,"size":3},{"mid":6717,"size":3}]
        #[{"mid":208,"size":3},{"mid":285,"size":3},{"mid":454,"size":3},{"mid":472,"size":3},{"mid":592,"size":2},{"mid":619,"size":2},{"mid":666,"size":2},{"mid":771,"size":0}]#[{"mid":286,"size":3},{"mid":470,"size":2}]#[{"mid":27,"size":4},{"mid":49,"size":3}]#[{"mid":368,"size":1},{"mid":387,"size":3},{"mid":549,"size":1},{"mid":562,"size":1},{"mid":566,"size":1},{"mid":570,"size":3},{"mid":602,"size":2},{"mid":610,"size":2}]
        fitaroundres[name]=[{"midi":-1,"midx":0,"midy":0} for i in range(len(fitaround[name]))]
        x=data[name+"_x"]
        y=data[name+"_y"]
        print(len(x))
        plt.plot(data[name+"_y"])
        plt.show()
        plt.title(name)
        def intervall(value):
            return max(min(len(x)-1,value),0)
        fitsx,fitsy=[],[]
        for i,fits in enumerate(fitaround[name]):
            #print(fits["mid"])
            #print(intervall(fits["mid"]-fits["size"]),intervall(fits["mid"]+fits["size"]))
            #print(y[fits["mid"]])
            midv,fity,fitx=fitpeak(x,y,intervall(fits["mid"]-fits["size"]),intervall(fits["mid"]+fits["size"]))
            fitaroundres[name][i]["midx"]=float(midv)
            fitaroundres[name][i]["midy"]=float(np.max(fity))
            print(float(midv),float(np.max(fity)))
            fitsx.append(fitx)
            fitsy.append(fity)
        print(len(data[name+"_y"]))
        print(name,np.argmax(np.array(data[name+"_y"])))
        plt.plot(data[name+"_x"],data[name+"_y"])
        for i in range(len(fitsx)):
            plt.plot(fitsx[i],fitsy[i])
        print(fitaroundres[name])
        dumpa("jsons\\res.json",fitaroundres)
        dumpa("jsons\\values.json",fitaround)
        plt.show()
import pandas as pd
def writeofjson(name="jsons\\res.json"):
    pd.read_json(name).to_excel('output.xlsx')
def aplot():
    data=loada("jsons\\kvant.json")
    x_=np.array(data["Matning 5.1 - Cd_x"])+1.13
    y_=np.array(data["Matning 5.1 - Cd_y"])*1e6
    del data
    plt.plot(x_,y_,label="Mätning 5.1 - Cd")
    plt.xlabel("Våglängd [nm]")
    plt.ylabel("Ström [µA]")
    plt.title("Våglängder hos fotoner för Kadium")
    plt.legend()
    plt.show()
aplot()
#writeofjson()
#data=loada()
#plotaone(data)
