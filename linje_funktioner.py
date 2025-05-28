#kod för inläsning av tabelerad data för spektral linjer
import pandas as pd
def get_lines(element):
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

    return pd.read_csv(filnamn)