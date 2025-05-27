import pandas as pd
import json
import numpy as np
import matplotlib.pyplot as plt
def dumpa(name="cords.json",result=None):
    with open(name, 'w') as f:
            json.dump(result,f)
def loada(name="cords"):
    with open(name,"r") as f:
        return json.load(f)
def exceltojson(place="Gothenburg",fileold="data",filenew="data"):
    file=pd.read_excel("excels//"+fileold+".xlsx",sheet_name=place,index_col=None,header=None)
    #print(file[1][3:])
    latitude, longitude=file[0][1],file[1][1]
    time=list([str(i) for i in file[0][4:]])
    Ta=list(file[1][4:])
    print("working")
    #print(file)
    del file #to reduce size
    data={}
    del time #to reduce size
    del Ta #to reduce size
    dumpa("jsons//"+filenew+".json",data)
def maket(dif,avikelse,diam=5.73):
    return (dif-avikelse)*(np.pi/18)
def maketinv(dif,diam=5.73):
    return diam*dif
def returntsvfileas_2darray(file="riktigt_test_ons_kl16.tsv"):
    def fl(x):
        try:
            return float(x)
        except:
            print("error"+x+"error")
            return -1
    with open(file, "r") as f:
        ddd = f.read()
    del f,file
    ddd=ddd.replace(",",".")
    return [np.array([fl(d) for d in dd.split("\t")]) for dd in ddd.split("\n")]
from scipy import signal

def reducebrus(x):
    b, a = signal.ellip(10, 0.01, 1000, 0.1) 
    return signal.filtfilt(b, a, x,padlen=1000)
   
def plotres(file=None,data=None,index1=0):
    if data is None:
        if file is None:
            file=["riktigt_test_tors_kl18.tsv","riktigt_test_ons_kl16.tsv"][index1]
        data=returntsvfileas_2darray(file=file)
    print("")
    if index1==0:
        data[0]=data[0]*0.1
    for i in range(len(data)-1):
        t=data[i+1]
        y=data[0]
        sorted_pairs = sorted(zip(list(t), list(y))) 
        t, x = zip(*sorted_pairs)  
        t = np.array(t)
        y = np.array(x)
        
        #t=reducebrus(t)
        #y=reducebrus(y)
        l=np.shape(t)[0]
        indexm,ym=0.5,10
        for i9 in range(1000):
            if abs(t[i9*l//1000]-291.2)<ym:
                indexm=i9/1000
                ym=abs(t[i9*l//1000]-291.2)
        size=0.02
        print(t[int(indexm*l)],t[int((indexm-size)*l)],t[int((indexm+size)*l)],l)
        mt=np.mean(t[int((indexm-size)*l):int((indexm+size)*l)])
        my=np.mean(y[int((indexm-size)*l):int((indexm+size)*l)])
        print("mean",my,mt)
        model=(y-my)/(t-mt)/my
        indexm=int(indexm*l)
        a=0.05
        print("mean",1/(1-2*a)*((indexm/l-a)*np.mean(model[:indexm-int(l*a)])+(1-indexm/l-a)*np.mean(model[indexm+int(l*a):])))
        model=reducebrus(model)
        #print(my,mt)
        plt.plot(t,model,label=str(i))
        #plt.scatter(t,y,label=str(i),alpha=1,s=0.1)
        slfk,slfm=slf(data[i+1],data[0])
        error=slfv(data[i+1],data[0],slfk,slfm)
        print(error/(slfk*292+slfm))
        print((slfk)/(slfk*292+slfm))
        stringout="Mätning temp \n t1    \t t2    \t t3  "
        stringout+="\n"
        for k in range(2*np.shape(data[0])[0]//1000-1):
            stringout+="\n"
            for i in range(len(data)-1):        
                slfk,slfm=slf(data[i+1][k*500:500*(k+2)],data[0][500*k:500*(k+2)])
                error=slfv(data[i+1][k*500:500*(k+2)],data[0][500*k:500*(k+2)],slfk,slfm)
                mod=(slfk)/(slfk*292+slfm)
                res=error/(slfk*292+slfm)
                stringout+=f"{data[i+1][k*500]:.2f}\t{data[i+1][500*(k+2)]:.2f}\t{mod:7f}\t{res:10f}\t\t"
            
        print(stringout)
        x=np.array([np.min(data[i+1]),np.max(data[i+1])])

        #plt.plot(x,slfk*x+slfm,label=str(i)+"fit",linestyle="--")
    plt.legend()
    plt.ylim(-0.03,0.03)
    plt.show()
def slf(temp1d,current1d):
    x_=temp1d-np.mean(temp1d)
    y_=current1d-np.mean(current1d)
    return np.sum(x_*y_)/np.sum(x_**2),np.mean(current1d)-np.mean(temp1d)*np.sum(x_*y_)/np.sum(x_**2)    
def slfv(temp1d,current1d,k,m):
    x_=temp1d-np.mean(temp1d)
    y_=current1d-(k*temp1d+m)
    print(np.sum(y_**2),np.sum(x_**2))
    return 	1.96*np.sqrt(1/(np.shape(y_)[0]-2)*np.sum(y_**2)/np.sum(x_**2))    
def getd(theta,lambd=1.541837,structure="bbc"):
    n = np.abs(np.array([i*0-1.5+2 for i in range(len(theta))]))+0.5
    print("N:",n)
    sss={"bbc":[4,2,2,4,6,8,10,12,14,16,18,20],"ffc":[4,3,3,4,8,11,12,16,19,20],"sc":[2,1,1,2,3,4,5]}
    f=sss[structure][:len(theta)]
    theta = np.abs(np.array(theta))
    d=1/2*n*lambd/np.sin(2*theta)*np.array(f)**0.5
    return d
def del1():
    data=[1,1.35,5.7,6.05,7.2,8.05,10.35,10.65,14.2,14.55]
    avikelse=(data[3]+data[2]+data[0]+data[1])/2/2
    #print((6.05-1)/2+1,(5.7-1.35)/2+1.35)
    print(avikelse,np.array(data)-np.array(avikelse))
    thetas=[maket(i,avikelse) for i in data]
    ds=getd(thetas)
    print(np.array(thetas)*180/np.pi)
    print(ds)
def del11(strycture="fcc",lambd=1.541837,d=3.61):
    sss={"bbc":[4,2,2,4,6,8,10,12,14,16,18,20],"fcc":[4,3,3,4,8,11,12,16,19,20],"sc":[2,1,1,2,3,4,5]}
    sss=sss[strycture]
    n = np.abs(np.array([i-1.5 for i in range(len(sss))]))+0.5
    print(n),
    tt=1/2*(n*lambd)/d*np.sqrt(np.array(sss))
    t=np.arcsin(tt)
    print(tt,t)
    s=maketinv(t)
    print(s)
    return s

plotres()
plotres()

#print(np.array([1,1.35,5.7,6.05,7.2,8.05,10.35,10.65,14.2,14.55])-3.55)
#del1()
#del11()