import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# Specify the path to your Excel file
def getfile():
    excel_file_path = 'Bok 51.xlsx'

    # Read the entire Excel file with all sheets
    excel_data = pd.read_excel(excel_file_path, sheet_name=None)  # sheet_name=None reads all sheets

    # Iterate through the sheets and print their content
    counts=[]
    pressure=[]
    for sheet_name, sheet_data in excel_data.items():
    #    print(f"Sheet Name: {sheet_name}")
    #    print(sheet_data)
        print(sheet_data)
        print("-"*60)
        counts.append(np.array(sheet_data["Unnamed: 1"].values[2:]))
        pressure.append(np.array(sheet_data["Unnamed: 2"].values[2:]))
    return counts,pressure
def plot(counts,pressure,linefitsk,linefitsm):
    x1=np.linspace(0,1100,20)
    for i in range(len(counts)):
        plt.scatter(pressure[i],counts[i],alpha=0.7,linewidths=0.2,label=f"data serie:{i+1}")
    for i in range(len(counts)):
        plt.plot(x1,(x1-linefitsm[i])/linefitsk[i],alpha=1,linewidth=1,linestyle="--",label=f"fitted serie:{i+1}")
    #plt.plot(pressure[i],np.gradient(pressure[i],counts[i]))
    plt.xlabel("Pressure [hPa]")
    plt.ylabel("Counts [1]")
    plt.title("Antal counts vid givet tryck med linjära anpassningar till datan")

    plt.legend(loc="lower right",fontsize=8)
    plt.show()
def slf(counts1d,pressure1d):
    x_=counts1d-np.mean(counts1d)
    y_=pressure1d-np.mean(pressure1d)
    return np.sum(x_*y_)/np.sum(x_**2),np.mean(pressure1d)-np.mean(counts1d)*np.sum(x_*y_)/np.sum(x_**2)
def skattning(yp,y):
    return 1/(np.shape(y)[0]-1)* np.sum((yp-y)**2)
def analytic1(counts,pressure):
    res,res_=[], []
    for i in range(len(counts)):
        res1,res2=slf(counts[i],pressure[i])
        res.append(res1)
        res_.append(res2)
    return res,res_
def analytic2(value,P_0=1020,lamda=632.8e-9,l=0.05):
    return 1+P_0/value*lamda/(2*l)
counts,pressure=getfile()
slfs,xdif=analytic1(counts,pressure)
skatt=[skattning(counts[i]*slfs[i]+xdif[i],pressure[i]) for i in range(len(slfs))]
n=[analytic2(i) for i in slfs]
print("Brytningsidex \n"+"\n".join([f"{n[i]:.6f} of data sqrt(skattning)={np.sqrt(skatt[i]):.6f}" for i in range(len(n))]))
print(f"Brytningsindex mean {np.mean(np.array(n))} sqrt skattning: {np.sqrt(skattning(np.mean(np.array(n)),np.array(n)))}")
print("more \n"+"\n".join([f"{np.shape(pressure[i])[0]} {slfs[i]:.6f} {xdif[i]:.6f}" for i in range(len(n))]))

print(slfs)
plot(counts,pressure,slfs,xdif)