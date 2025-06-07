import kvant
import linje_funktioner as lf
import numpy as np
import kalibrering as ka

#initiala variabler
#Vet ej hur jag ska hantera dag 1 mätningar så jag tänker ej göra det
sheets = ['Matning 4 -Cd', 'Matning 5.1 - Cd', 'Matning 5.2 - Na',  
          'matning 6 - Na', 'Matning 7 - Na', 'Matning 8 - H', 'Matning 9 - H']
element = ["Cd", "Cd", "Na", "Na", "Na", "H", "H"]
data = kvant.loada(name = "jsons\\res.json")

#blädrar genom alla givna sheets och printar transitions sannolikheter
for i, sheet in enumerate(sheets):
    wl = np.array([entry['midx'] for entry in data[sheet]])
    wl = ka.adjust(wl)
    amp = np.array([entry['midy'] for entry in data[sheet]])
    lines = lf.get_lines(element[i], minint=1)
    
    print(sheet)
    print(lf.data_till_prob(amp, wl, lines))