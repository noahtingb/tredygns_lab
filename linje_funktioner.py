#kod för inläsning av tabelerad data för spektral linjer
import pandas as pd
import numpy as np

#Ger all data som finns i csv filerna, och om raw är false så ignoreras eventuella
#symboler som indikerar detaljer om datan
def get_lines(element, raw = False):
    filnamn = ""

    match element:
        case "Cd":
            filnamn = "excels\Cd_I_lines.csv"

        case "Na":
            filnamn = "excels\\Na_I_lines.csv"

        case "H":
            filnamn = "excels\H_I_lines.csv"

        case "Ne":
            filnamn = "excels\\Ne_I_lines.csv"

        case _:
            raise Exception("Inkorrekt elementförkortning eller ej med i tabulerade element.")
    
    retur_varde = pd.read_csv(filnamn)
    if(not raw):
        retur_varde = retur_varde.replace(['[\[\]="*wrbl()f]'],[""], regex = True)

    return retur_varde

#Ger tillbaka våglängder och de relativa intensiteterna för de specifika våglängderna.
#Där den högsta relativa intensiteten normeras till att vara lika stor som den
#maximala relativa tabulerade intensiteten.
#Relativ intensitet är inget absolut mått och anger bara intensitet relativ någon annan
def NIST_spektrum(element, max_peak):
    linjer = get_lines(element)
    intensiteter = pd.to_numeric(linjer["intens"])
    wl = pd.to_numeric(linjer["obs_wl_air(nm)"])
    max_intens = np.max(intensiteter)
    norm_intens = intensiteter/max_intens
    
    return wl, norm_intens*max_peak

#anger våglängder med icke exakta värden i exakta "hinkar" för ämnet i fråga
#och returnerar korrekt amplitud med korrekt våglängd
#amplituder, våglängder och element
def bucketer(amp, wl, element):
    lines = get_lines(element)
    wl_t = pd.to_numeric(lines["ritz_wl_air(nm)"]) #ritz våglängd, våglängden som fås från energiskillnaden
    
    ut_amp  = np.zeros(len(wl_t))
    
    
    
    for i, a in enumerate(wl):
        index = np.argmin(np.abs(wl_t - a)) #returnerar indexet av den exakta våglängden som minimerar avståndet mellan den exakta och uppmätta.
        if(ut_amp[index] != 0):
            raise Exception("angivna våglängden: " + wl[index] + "är för nära annan våglängd. Filtrera ut våglängder längre ifrån" + a)
        else:
            ut_amp[index] = amp[i]
            
    return ut_amp


#använder amplituder av våglängder för att beräkna transitions sannolikheter för
#specifierade transitioner. Transitionerna kommer mappas tillbaka till våglängder
#då våglängderna identifierar transitionerna unikt
#P = amplitud för wl/summa av amplituder för wl med samma initala energi
def trans_prob(element, amp):
    
    lines = get_lines(element)
    wl_t = lines["ritz_wl_air(nm)"]
    
    E_k = lines["Ek(eV)"] #initial energier
    
    u_Ek = np.unique(E_k)
    
    trans_prob = np.zeros(len(wl)) #transitions sannolikheter
    
    for wl_i in u_Ek:
        index = np.where(wl_i == wl)[0] #plockar ut index med spec. våglängd
        
        if(len(index) == 1):
            trans_prob[index] = 1
            
        else:
            norm = np.sum(amp[index]) #summerar amp för norm
            np.put(trans_prob, index, amp[index]/norm) #sätter in beräknade sannolikheter där de ska vara
            
    return trans_prob
    
#konverterar inexakt data till transitions sannolikheter för alla möjliga våglängder för en neutral atom mellan 200 till 1000 nm   
def data_till_prob(amp, wl, element):
    return trans_prob(element, bucketer(amp, wl, element))
    
    
    
    
    
    
    
    
    
    