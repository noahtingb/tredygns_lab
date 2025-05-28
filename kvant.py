import numpy as np
from scipy.optimize import curve_fit
import pandas as pd
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
    
def getfiles():
    excel_file_path = 'excels\\Kvantdata.xlsx'

    # Read the entire Excel file with all sheets
    excel_data = pd.read_excel(excel_file_path, sheet_name=None, skiprows=[0])  # sheet_name=None reads all sheets

    # Iterate through the sheets and print their content
    ddddd={}
    print("ddodd")
    #s=[]
    sheet_names=["Dag1 mätningar", "Mätning 4 -Cd", "Mätning 5.1 - Cd", "Mätning 5.2 - Na", "mätning 6 - Na", "Mätning 7 - Na", "Mätning 8 - H", "Mätning 9 - H", "Övriga pkter"]
#    for sheet_name, sheet_data in excel_data.items():
#        s+=[sheet_name]
#        print(f"Sheet Name: {sheet_name}")
    names=[]
    for sheet_name, sheet_data in excel_data.items():
        print(sheet_name)

        #print(sheet_data)
        print("-"*60)
        if sheet_name!="Övriga pkter":
            names.append(sheet_name.replace('ä','a'))
            she=list(sheet_data["Vågläng - Plot 0"].values[2:])
            for i,j in enumerate(she):
                if j<1e10 and j>-1e10:
                    pass
                else:
                    she=she[:i]
                    break
            ddddd[f"{sheet_name.replace('ä','a')}_x"]=[float(i) for i in she]
            she=list(sheet_data["Ström - Plot 0"].values[2:])
            for i,j in enumerate(she):
                if j<1e10 and j>-1e10:
                    pass
                else:
                    she=she[:i]
                    break
            ddddd[f"{sheet_name.replace('ä','a')}_y"]=[float(i) for i in she]
        ddddd["k"]=names
    return ddddd



#plottar detta alla helt enkelt ?
def plotaone(data):
    nonames=['Dag1 matning2']
    names=['Dag1 matningar', 'Dag1 Matning 3.1', 'Dag1 Matning 3.2', 'Matning 4 -Cd', 'Matning 5.1 - Cd', 'Matning 5.2 - Na', 'matning 6 - Na', 'Matning 7 - Na', 'Matning 8 - H', 'Matning 9 - H']
    for name in names:
        plt.title(name)
        plt.plot(data[name+"_x"],data[name+"_y"])
        plt.show()
        
        
#dumpa(result=getfiles())
#data=loada()
#print(data.get("k"))
#plotaone(data)