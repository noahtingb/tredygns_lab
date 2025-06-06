import numpy as np
import kvant
from scipy.optimize import curve_fit


#kalibrering till mätning 6
def init_calibrering():
    #arbiträra begränsingar på data för att bättra anpassa till peaks
    ovre_lim = 55
    ondre_lim = 20
    
    #inladdning av datan
    name = "matning 6 - Na"
    data=kvant.loada()
    x = data[name+"_x"][ondre_lim:ovre_lim]
    y = data[name+"_y"][ondre_lim:ovre_lim]
    
    #gauss funktion
    def gauss(x, amplitude, x0, sigma):
        y = np.exp(-0.5 * ((x - x0) / sigma) ** 2)
        return amplitude * y

    #två gaussfunktioner adderade, denna optimeras för att ge resultat
    def dubbel_gauss(x, amp0, amp1, x0, x1, sigma0, sigma1):
        y = gauss(x, amp0, x0, sigma0) + gauss(x, amp1, x1, sigma1)
        return y
    
    initial = [5e-6, 5e-6, 587.8, 588.5, 0.01, 0.01] #initiala gissningar
    popt, _ = curve_fit(dubbel_gauss, x, y, p0=initial) #optimerar parametrar och matar ut dessa
    
    amp0, amp1, x0, x1, sig0, sig1 = popt #konstruerar plot av optimerad funktion
    y = dubbel_gauss(x, amp0, amp1, x0, x1, sig0, sig1)
    
    return popt, x, y
#körning av denna funktion ger parametrarna array([2.50124678e-06, 1.94075463e-06, 5.87878676e+02, 5.88487472e+02,
#       1.46314734e-01, 1.49659665e-01])
#vilket alltså är x0 = 5.87878676e+02 och x1= 5.88487472e+02


#gör linfit mellan observerade och databas peaks
def calib():
    
    #kalibrering gjort m.a.p mätning 9 med väte
    x = [395.78279299, 408.95198254,432.88231291, 484.68510924,655.06996891,843.74378532,867.2670103]
    y = [397.0075, 410.1734, 434.0472, 486.135 , 656.279 , 843.795 , 866.502 ]
    w = np.polyfit(x,y,1)
    k = w[0]
    m = w[1]
    
    return k, m

#linfit från mätning 9, denna funktion tar in okalibrerad x koordinater och ger kalibrerade x koordinater
def adjust(z):
    return 0.996492895776221*z + 2.842074706455973
    
    