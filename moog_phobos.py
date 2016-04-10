#!/usr/local/bin/python

#---------------- MOOG -----------------------#
#-- Creates a MOOG parameter file (no plotting) and runs MOOG.
def moog(star,name,feelements,location,plotornot):
    import os
    import subprocess
    #-- Go to appropriate directory.
    os.chdir(location)
    if not os.path.exists('moog_out1/'):
        os.mkdir('moog_out1/')

    if not os.path.exists('moog_out2/'):
        os.mkdir('moog_out2/')

    if not os.path.exists('moog_parameters/'):
        os.mkdir('moog_parameters/')
        os.chdir('moog_parameters/')
    else:
        os.chdir('moog_parameters/')


    #-- Clean directory to prevent contamination.
    if os.path.exists('%s/moog_out1/{}.out1'.format(location,name)):
        os.remove('%s/moog_out1/{}.out1'.format(location,name))
    if os.path.exists('%s/moog_out2/{}.out2'.format(location,name)):
        os.remove('%s/moog_out2/{}.out2'.format(location,name))
    if os.path.exists('{}'.format(star)):
        os.remove('{}'.format(star))

    #-- Build the MOOG parameter file for the star, using the star names previously defined.
    with open('{}'.format(star), 'w') as moog_param_file:
        moog_param_file.write('abfind\n'\
        'terminal     x11\n'\
        'standard_out \'../moog_out1/{n}.out1\'\n'\
        'summary_out  \'../moog_out2/{n}.out2\'\n'\
        'model_in     \'../models/{n}.model.dat\'\n'\
        'lines_in     \'../moog_input/{n}.{fee}.lines\'\n'\
        'atmosphere 1\n'\
        'molecules 0\n'\
        'lines 1\n'\
        'freeform 1\n'\
        'flux/int 0\n'\
        'damping 0\n'\
        'plot {plotornot}'.format(n=name,fee=feelements,plotornot=plotornot))

    #-- Runs MOOG using the moog_input line file.
    subprocess.Popen(['MOOG'], stdin=subprocess.PIPE).communicate(input='\n{}\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n'.format(star))

    os.chdir(location)
    
    return