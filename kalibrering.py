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
def calib(z):
    #observerade våglängder från dubbelpeak av Na från NIST är 
    #588.995095 nm och 589.592424 nm
    
    x = [5.87878676e+02,5.88487472e+02]
    y = [588.995095, 589.592424]
    w = np.polyfit(x,y,1)
    k = w[0]
    m = w[1]
    
    return k*z + m