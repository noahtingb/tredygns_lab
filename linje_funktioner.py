#kod för inläsning av tabelerad data för spektral linjer
import pandas as pd
import numpy as np

#Ger all data som finns i csv filerna, och om raw är false så ignoreras eventuella
#symboler som indikerar detaljer om datan
def get_lines(element, raw = False, typ = "I", minint = 100):
    filnamn = ""
    
    match typ:
        case "A_ki":
            match element:
                case "Cd":
                    filnamn = "excels\Cd_Aki.csv"

                case "Na":
                    filnamn = "excels\\Na_Aki.csv"

                case "H":
                    filnamn = "excels\H_Aki.csv"

                case "Ne":
                    filnamn = "excels\\Ne_I_lines.csv"

                case _:
                    raise Exception("Inkorrekt elementförkortning eller ej med i tabulerade element.")
            
        case "I":
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
        case _:
            raise Exception("Inkorrekt typ eller ej med i tabulerade typer.")
    
    
    retur_varde = pd.read_csv(filnamn)
    if(not raw):
        retur_varde = retur_varde.replace(['[\[\]="*wrbld()f]'],[""], regex = True)
        retur_varde = retur_varde[pd.to_numeric(retur_varde["intens"]) >= minint]

    return retur_varde

#Ger tillbaka våglängder och de relativa intensiteterna för de specifika våglängderna.
#Där den högsta relativa intensiteten normeras till att vara lika stor som den
#maximala relativa tabulerade intensiteten.
#Relativ intensitet är inget absolut mått och anger bara intensitet relativ någon annan
def NIST_spektrum(linjer, max_peak):
    
    intensiteter = pd.to_numeric(linjer["intens"])
    wl = pd.to_numeric(linjer["obs_wl_air(nm)"])
    max_intens = np.max(intensiteter)
    norm_intens = intensiteter/max_intens
    
    return wl, norm_intens*max_peak

#anger våglängder med icke exakta värden i exakta "hinkar" för ämnet i fråga
#och returnerar korrekt amplitud med korrekt våglängd
#amplituder, våglängder och element
def bucketer(amp, wl, lines, max_err = 5):
    
    
    wl_t = np.array(pd.to_numeric(lines["ritz_wl_air(nm)"])) #ritz våglängd, våglängden som fås från energiskillnaden
    
    ut_amp  = np.zeros(len(wl_t))
    err = np.ones(len(wl_t))*max_err #anger vad det minimala funna felet för ett visst wl är.
    #max_err anger maximala tillåtna felet innan funktionen ignorerar våglängds kandidaten.
    
    
    for i, a in enumerate(wl):
        index = np.argmin(np.abs(wl_t - a)) #returnerar indexet av den exakta våglängden som minimerar avståndet mellan den exakta och uppmätta.
        lokal_err = np.abs(wl_t[index] - a) #värdet av det funna minimumet
        if(err[index] > lokal_err): #bekräftar att detta minimat är det minsta funna
            ut_amp[index] = amp[i]
            err[index] = lokal_err
    
    print(amp ,"bucketer")
    return ut_amp



#använder amplituder av våglängder för att beräkna transitions sannolikheter för
#specifierade transitioner. Transitionerna kommer mappas tillbaka till våglängder
#då våglängderna identifierar transitionerna unikt
#P = amplitud för wl/summa av amplituder för wl med samma initala energi
def trans_prob(lines, amp):
    
    
    wl = pd.to_numeric(lines["ritz_wl_air(nm)"])
    
    E_k = lines["Ek(eV)"] #initial energier
    
    u_Ek = np.unique(pd.to_numeric(E_k))
    
    trans_prob = np.zeros(len(wl)) #transitions sannolikheter
    
    
    for wl_i in u_Ek:
        index = np.where(abs(wl_i - wl) < 0.01)[0] #plockar ut index med spec. våglängd
        print(index)
        
        if(len(index) == 1):
            trans_prob[index] = 1
            
        else:
            norm = np.sum(amp[index]) #summerar amp för norm
            np.put(trans_prob, index, amp[index]/norm) #sätter in beräknade sannolikheter där de ska vara
           
    return trans_prob


#använder data för att konstruera matris som beskriver sannolikheten för en energinivå att övergå till en annan
#funktionen returnerar sannolikhetsmatrisen, start energinivåerna som betecknas Ek och slutenerginivåerna som betecknas Ei
#matrisen anger INTE hur snabbt en energinivå transformeras till en annan, bara sannolikheten att en elektron vid
#någon framtida punkt antingen transfereras till en eller annan energinivå
def data_till_prob(amp, wl, lines, maxerr = 5):
    wl_f = auto_assigner(wl, lines)
    
    Ei = lines[pd.to_numeric(lines["obs_wl_air(nm)"]).isin(wl_f)]["Ei(eV)"]
    Ek = lines[pd.to_numeric(lines["obs_wl_air(nm)"]).isin(wl_f)]["Ek(eV)"]
    
    #unika energinivåer
    uEi = np.unique(Ei)
    uEk = np.unique(Ek)
    #dessa funktioner fiskar ur energinivåer
    
    trans_matris = np.zeros((len(uEi),len(uEk)))
    
    
    for a, wl_i in enumerate(wl_f):
        Ei_h = np.array(Ei)[a]
        Ek_h = np.array(Ek)[a]
        index_i = np.where(uEi == Ei_h)[0][0]
        index_k = np.where(uEk == Ek_h)[0][0]
        trans_matris[index_i][index_k] = amp[a]
        
      
    trans_matris = np.transpose(trans_matris)
    for a in range(len(trans_matris)):
        trans_matris[a] = trans_matris[a]/np.sum(trans_matris[a])
    
    trans_matris = np.transpose(trans_matris)
    
    return trans_matris, uEk, uEi
    
    

#returnerar observerade våglängder från NIST data som passar våglängder bäst
def auto_assigner(wl,lines,max_err=2):
    wl_t = pd.to_numeric(lines["obs_wl_air(nm)"])
    
    found = np.full(len(wl_t),False) #anger om det finns en våglängd
    
    
    
    for i, a in enumerate(wl_t):
        found[i] = max_err >= np.min(np.abs(wl - a)) #tar absolut värdet mellan alla angivna våglängder och en viss NIST våglängd
        #jämför minimat med max_err och ger True när det är mindre än max_err
    
    
    return np.array(wl_t)[found] #filtrerar ut så det är endast funna våglängder

    
    
    
    
    
    
    
    
    
    