#!/usr/local/bin/python

#-------------- CREATE PHOTOMETRIC PARAMETER FILE ----------------------------#
#-- Creates photo.param file from photometry file photometry.txt.
#DISTANCE MODULUS? CHECK EQs FOR MISSED VARIABLES
def create_photom_params(location,fe_h,dist_mod,colour_scale):
    import os
    import math
    import numpy as np
    os.chdir(location)
    photometry = np.genfromtxt('photometry.txt',dtype=None)
    photo_params = []
    if colour_scale == 'BV':
        a0 = 0.5737; a1 = 0.4882; a2 = -0.0149; a3 = 0.0563; a4 = -0.1160; a5 = -0.0114
    elif colour_scale == 'VK':
        a0 = 0.4405; a1 = 0.3272; a2 = -0.0252; a3 = -0.0016; a4 = -0.0053; a5 = -0.0040
    elif colour_scale == 'VJ':
        a0 = 0.2943; a1 = 0.5604; a2 = -0.0677; a3 = 0.0179; a4 = -0.0532; a5 = -0.0088
    elif colour_scale == 'VH':
        a0 = 0.4354; a1 = 0.3405; a2 = -0.0263; a3 = -0.0012; a4 = -0.0049; a5 = -0.0027
    elif colour_scale == 'by':
        a0 = 0.5515; a1 = 0.9085; a2 = -0.1494; a3 = 0.0616; a4 = -0.0668; a5 = -0.0083
    else:
        sys.exit('\nUnsupported photometric colour scale. Exiting Phobos')
    for i in range(len(photometry)):
        name = photometry[i][0]
        V = photometry[i][1]
        colour = photometry[i][2]
        Teff = 5040/(a0+(a1*colour)+(a2*(colour**2))+(a3*colour*fe_h)+(a4*fe_h)+(a5*(fe_h**2)))
        Teff = int(float("{0:.0f}".format(Teff)))
        if Teff <= 4677:
            logg = 4.44+math.log10(0.8)+0.4*(V-dist_mod+((-5.531*10**(-2))/(math.log10(Teff)-3.52))-0.6177+(4.420*(math.log10(Teff)-3.52))-2.669*((math.log10(Teff)-3.52)**2)+(0.6943*(math.log10(Teff)-3.52)*fe_h)-0.1071*fe_h-(8.612*10**(-3))*(fe_h**2)-4.72)+4.0*math.log10(Teff)-15.0447 
        else:
            logg = 4.44+math.log10(0.8)+0.4*(V-dist_mod+((-9.930*10**(-2))/(math.log10(Teff)-3.52))+2.887*10**(-2)+(2.275*(math.log10(Teff)-3.52))-4.425*((math.log10(Teff)-3.52)**2)+(0.3505*(math.log10(Teff)-3.52)*fe_h)-(5.558*10**(-2))*fe_h-(5.375*10**(-3))*(fe_h**2)-4.72)+4.0*math.log10(Teff)-15.0447 
        logg = float("{0:.2f}".format(logg))
        xi = 2.22-0.322*logg
        xi = float("{0:.2f}".format(xi))
        photo_params.append([name, Teff, logg, xi])
    np.savetxt('photo.params', photo_params, fmt='%s', newline='\n')
    return