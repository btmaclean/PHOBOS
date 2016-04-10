#!/usr/local/bin/python

#-------------- MAKEKURUCZ ------------------------#
#-- Creates MOOG friendly atmospheric model. To be called from Phobos.
def model(name,location,Teff,logg,xi,fe_h):
    import os
    import subprocess
    #-- Go to appropriate directory.
    os.chdir(location)
    if not os.path.exists('models/'):
        os.mkdir('models/')
        os.chdir('models/')
    else:
        os.chdir('models/')

    #-- Clean directory.    
    if os.path.exists('{}.model.dat'.format(name)):
        os.remove('{}.model.dat'.format(name))

    #-- Depending on the parameters Teff and logg, a model is created with Castelli using an input grid that covers the parameters.
    subprocess.Popen(['makekurucz3'], stdin=subprocess.PIPE).communicate(input='{},{},{},{}\nAODFNEW'.format(Teff,logg,fe_h,xi))
    
    #-- Remove temp files and rename model.
    os.rename('FINALMODEL', '{}.model.dat'.format(name))

    os.chdir(location)
  
    return