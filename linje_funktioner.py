#kod för inläsning av tabelerad data för spektral linjer
import pandas as pd
import numpy as np

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
        retur_varde = retur_varde.replace(['[\[\]="*wrbl()]'],[""], regex = True)

    return retur_varde

def NIST_spektrum(element, max_peak):
    linjer = get_lines(element)
    intensiteter = pd.to_numeric(linjer["intens"])
    wl = pd.to_numeric(linjer["obs_wl_air(nm)"])
    max_intens = np.max(intensiteter)
    norm_intens = intensiteter/max_intens
    
    return wl, norm_intens*max_peak