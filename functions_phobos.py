#!/usr/local/bin/python

#-------------- PYCLEAN ----------------------------#
#-- Remove temporary *.pyc files from the Phobos location directory.
def pyclean(scriptloc):
    import os
    if os.path.exists('{}/functions_phobos.pyc'.format(scriptloc)):
        os.remove('{}/functions_phobos.pyc'.format(scriptloc))
    return

#-------------- PURGE ----------------------------#
#-- Reset the analysis folder back to the starting point, leaving only the /fits directory, photometry.txt, and any backup files created.
def purge(location):
    import os
    import shutil
    if os.path.exists('{}/ares'.format(location)):
        shutil.rmtree('{}/ares'.format(location))
    if os.path.exists('{}/models'.format(location)):
        shutil.rmtree('{}/models'.format(location))
    if os.path.exists('{}/moog_input'.format(location)):
        shutil.rmtree('{}/moog_input'.format(location))
    if os.path.exists('{}/moog_out1'.format(location)):
        shutil.rmtree('{}/moog_out1'.format(location))
    if os.path.exists('{}/moog_out2'.format(location)):
        shutil.rmtree('{}/moog_out2'.format(location))
    if os.path.exists('{}/moog_parameters'.format(location)):
        shutil.rmtree('{}/moog_parameters'.format(location))
    if os.path.exists('{}/spectro.params'.format(location)):
        os.remove('{}/spectro.params'.format(location))
    if os.path.exists('{}/photo.params'.format(location)):
        os.remove('{}/photo.params'.format(location))
    return

#-------------- PHOTO REPLACE ----------------------------#
#-- Reset the parameters and model of the star to the initial photometric estimation (from photo.params)
def photoreplace(name,location,Teff,logg,xi,fe_h,arrayelement):
    import numpy as np
    params = np.genfromtxt('photo.params',dtype=None)
    name = params[arrayelement][0]
    Teff = int(params[arrayelement][1])
    logg = params[arrayelement][2]
    xi = params[arrayelement][3]
    model(name,location,Teff,logg,xi,fe_h)
    params = np.genfromtxt('spectro.params',dtype=None)
    params[arrayelement][1] = int(Teff)
    params[arrayelement][2] = logg
    params[arrayelement][3] = xi
    np.savetxt('spectro.params', params, fmt='%s')
    return

#-------------- DELETE STAR ----------------------------#
#-- Delete either: i) the iron abundance files and reset parameters to photometric, ii) the elemental abundance files, or iii) all abundance files and reset parameters to photometric.
def deletestar(Teff,logg,xi,fe_h,name,location,feelements,star,arrayelement):
    import os
    if os.path.exists('{}/ares/{}.{}.ares'.format(location,name,feelements)):
        os.remove('{}/ares/{}.{}.ares'.format(location,name,feelements))
    if os.path.exists('{}/models/{}.model.dat'.format(location,name)):
        os.remove('{}/models/{}.model.dat'.format(location,name))
    if os.path.exists('{}/moog_input/{}.{}.lines'.format(location,name,feelements)):
        os.remove('{}/moog_input/{}.{}.lines'.format(location,name,feelements))
    if os.path.exists('{}/moog_out1/{}.out1'.format(location,name)):
        os.remove('{}/moog_out1/{}.out1'.format(location,name))
    if os.path.exists('{}/moog_out2/{}.out2'.format(location,name)):
        os.remove('{}/moog_out2/{}.out2'.format(location,name))
    if os.path.exists('{}/moog_parameters/{}'.format(location,star)):
        os.remove('{}/moog_parameters/{}'.format(location,star))
    if feelements == 'fe':
        photoreplace(name,location,Teff,logg,xi,fe_h,arrayelement)
    return

#-------------- ARES ----------------------------#
#-- Run star through ARES, and prepares the MOOG input file from the ARES output file and line list.
def ares(name,location,feelements,linelist_fe,linelist_elements):
    import os
    import subprocess
    import numpy as np
    linelist = eval('linelist_{}'.format(feelements))
    #-- Go to appropriate directory.
    os.chdir(location)
    if not os.path.exists('ares/'):
        os.mkdir('ares/')
        os.chdir('ares/')
    else:
        os.chdir('ares/')
    #-- BLUE --#
    #-- Clean directory.    
    if os.path.exists('mine.opt'):
        os.remove('mine.opt')
    if os.path.exists('logARES.txt'):
        os.remove('logARES.txt')
    if os.path.exists('{}.{}.ares'.format(name,feelements)):
        os.remove('{}.{}.ares'.format(name,feelements))
    if os.path.exists('../moog_input/{}.{}.lines'.format(name,feelements)):
        os.remove('../moog_input/{}.{}.lines'.format(name,feelements))
    #-- Build the ARES parameter file for the star.
    with open('mine.opt', 'w') as ares_param_file:
        ares_param_file.write('specfits=\'../fits/{n}.fits\'\n'\
        'readlinedat=\'{ll}\'\n'\
        'fileout=\'{n}.{fee}.ares\'\n'\
        'lambdai=4500.\n'\
        'lambdaf=5000.\n'\
        'smoothder=4\n'\
        'space=1\n'\
        'rejt=0.9\n'\
        'lineresol=0.1\n'\
        'miniline=5\n'\
        'plots_flag=0\n'.format(n=name,ll=linelist,fee=feelements))
    #-- Run ARES until it fully completes
    ares_out = subprocess.Popen(['ARES'], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT).communicate(input=None)
    print ares_out
    while not os.path.exists('{}.{}.ares'.format(name,feelements)):
        ares_out = subprocess.Popen(['ARES'], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT).communicate(input=None)
        print '\nARES failed\n'
        print ares_out
    print '\nARES completed\n'
    #-- Create blue MOOG input file
    final_array_blue = []
    if os.path.getsize('{}.{}.ares'.format(name,feelements)) > 0:
        line_array = np.genfromtxt('{}'.format(linelist))
        ares_array_blue = np.genfromtxt('{}.{}.ares'.format(name,feelements))
        for row in line_array:
            index = np.where(ares_array_blue[:,0] == row[0])[0]
            if np.size(index) != 0:
                final_array_blue.append([row[0], row[1], row[2], row[3], 0, 0, ares_array_blue[index[0], 7]])
        final_array_blue = np.array(final_array_blue)
    else:
        print 'No blue absorption lines found.'
        final_array_blue.append([0, 0, 0, 0, 0, 0, 0])
    #-- GREEN, RED, IR --#
    #-- Clean directory.    
    if os.path.exists('mine.opt'):
        os.remove('mine.opt')
    if os.path.exists('logARES.txt'):
        os.remove('logARES.txt')
    if os.path.exists('{}.{}.ares'.format(name,feelements)):
        os.remove('{}.{}.ares'.format(name,feelements))
    #-- Build the ARES parameter file for the star.
    with open('mine.opt', 'w') as ares_param_file:
        ares_param_file.write('specfits=\'../fits/{n}.fits\'\n'\
        'readlinedat=\'{ll}\'\n'\
        'fileout=\'{n}.{fee}.ares\'\n'\
        'lambdai=5000.\n'\
        'lambdaf=8000.\n'\
        'smoothder=4\n'\
        'space=1\n'\
        'rejt=0.995\n'\
        'lineresol=0.1\n'\
        'miniline=5\n'\
        'plots_flag=0\n'.format(n=name,ll=linelist,fee=feelements))
    #-- Run ARES until it fully completes
    ares_out = subprocess.Popen(['ARES'], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT).communicate(input=None)
    print ares_out
    while not os.path.exists('{}.{}.ares'.format(name,feelements)):
        ares_out = subprocess.Popen(['ARES'], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT).communicate(input=None)
        print '\nARES failed\n'
        print ares_out
    print '\nARES completed\n'
    #-- Create green/red/ir MOOG input file
    final_array_grir = []
    if os.path.getsize('{}.{}.ares'.format(name,feelements)) > 0:
        line_array = np.genfromtxt('{}'.format(linelist))
        ares_array_grir = np.genfromtxt('{}.{}.ares'.format(name,feelements))
        for row in line_array:
            index = np.where(ares_array_grir[:,0] == row[0])[0]
            if np.size(index) != 0:
                final_array_grir.append([row[0], row[1], row[2], row[3], 0, 0, ares_array_grir[index[0], 7]])
        final_array_grir = np.array(final_array_grir)
    else:
        print 'No green, red or IR absorption lines found.'
        final_array_grir.append([0, 0, 0, 0, 0, 0, 0])
    #-- Create final MOOG input file
    final_array_pre = np.vstack((final_array_blue, final_array_grir))
    final_array_26_0 = final_array_pre[final_array_pre[:,1] == 26.0]
    final_array_26_1 = final_array_pre[final_array_pre[:,1] == 26.1]
    final_array_3_0 = final_array_pre[final_array_pre[:,1] == 3.0]
    final_array_6_0 = final_array_pre[final_array_pre[:,1] == 6.0]
    final_array_8_0 = final_array_pre[final_array_pre[:,1] == 8.0]
    final_array_11_0 = final_array_pre[final_array_pre[:,1] == 11.0]
    final_array_12_0 = final_array_pre[final_array_pre[:,1] == 12.0]
    final_array_13_0 = final_array_pre[final_array_pre[:,1] == 13.0]
    final_array_14_0 = final_array_pre[final_array_pre[:,1] == 14.0]
    final_array_19_0 = final_array_pre[final_array_pre[:,1] == 19.0]
    final_array_20_0 = final_array_pre[final_array_pre[:,1] == 20.0]
    final_array_21_0 = final_array_pre[final_array_pre[:,1] == 21.0]
    final_array_21_1 = final_array_pre[final_array_pre[:,1] == 21.1]
    final_array_22_0 = final_array_pre[final_array_pre[:,1] == 22.0]
    final_array_22_1 = final_array_pre[final_array_pre[:,1] == 22.1]
    final_array_23_0 = final_array_pre[final_array_pre[:,1] == 23.0]
    final_array_24_0 = final_array_pre[final_array_pre[:,1] == 24.0]
    final_array_24_1 = final_array_pre[final_array_pre[:,1] == 24.1]
    final_array_25_0 = final_array_pre[final_array_pre[:,1] == 25.0]
    final_array_27_0 = final_array_pre[final_array_pre[:,1] == 27.0]
    final_array_28_0 = final_array_pre[final_array_pre[:,1] == 28.0]
    final_array_29_0 = final_array_pre[final_array_pre[:,1] == 29.0]
    final_array_30_0 = final_array_pre[final_array_pre[:,1] == 30.0]
    final_array_37_0 = final_array_pre[final_array_pre[:,1] == 37.0]
    final_array_38_0 = final_array_pre[final_array_pre[:,1] == 38.0]
    final_array_39_0 = final_array_pre[final_array_pre[:,1] == 39.0]
    final_array_40_0 = final_array_pre[final_array_pre[:,1] == 40.0]
    final_array_44_0 = final_array_pre[final_array_pre[:,1] == 44.0]
    final_array_56_1 = final_array_pre[final_array_pre[:,1] == 56.1]
    final_array_57_1 = final_array_pre[final_array_pre[:,1] == 57.1]
    final_array_58_1 = final_array_pre[final_array_pre[:,1] == 58.1]
    final_array_60_1 = final_array_pre[final_array_pre[:,1] == 60.1]
    final_array_63_1 = final_array_pre[final_array_pre[:,1] == 63.1]
    final_array = np.vstack((final_array_26_0,final_array_26_1,final_array_3_0,final_array_6_0,final_array_8_0,final_array_11_0,final_array_12_0,final_array_13_0,final_array_14_0,final_array_19_0,final_array_20_0,final_array_21_0,final_array_21_1,final_array_22_0,final_array_22_1,final_array_23_0,final_array_24_0,final_array_24_1,final_array_25_0,final_array_27_0,final_array_28_0,final_array_29_0,final_array_30_0,final_array_37_0,final_array_38_0,final_array_39_0,final_array_40_0,final_array_44_0,final_array_56_1,final_array_57_1,final_array_58_1,final_array_60_1,final_array_63_1))
    #-- Print to file
    np.savetxt('{}/moog_input/{}.{}.lines'.format(location,name,feelements), final_array, fmt='%.2f\t%.1f\t%.3f\t%.3f\t%.0f\t%.0f\t%.2f', newline='\n', header=' ')
    if os.path.exists('mine.opt'):
        os.remove('mine.opt')
    if os.path.exists('logARES.txt'):
        os.remove('logARES.txt')
    os.chdir(location)
    return

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

#-------------- PARAMETER SUMMARY ----------------------------#
#-- Create arrays: 'ablist' that contains an abundance value or stdev in each element; 'EPslope' and 'RWslope' which contain each value for FeI and FeII; and 'Iondiff' which specifies FeI-FeII.
def psum(name,Teff,logg,xi):
    ablist = []
    for line in open('moog_out2/{}.out2'.format(name)):
        if 'average abundance' in line:
            for t in line.split():
                try:
                    ablist.append(float(t))
                except ValueError:
                    pass
    EPslope = []
    for line in open('moog_out2/{}.out2'.format(name)):
        if 'E.P. correlation' in line:
            for t in line.split():
                try:
                    EPslope.append(float(t))
                except ValueError:
                    pass
    RWslope = []
    for line in open('moog_out2/{}.out2'.format(name)):
        if 'R.W. correlation' in line:
            for t in line.split():
                try:
                    RWslope.append(float(t))
                except ValueError:
                    pass
    Iondiff = ablist[0] - ablist[3]
    psumlist = [EPslope[0],RWslope[0],Iondiff,ablist[0],ablist[1],int(ablist[2]),ablist[3],ablist[4],ablist[5]]
    print 'EP slope = {}'.format(EPslope[0])
    print 'RW slope = {}'.format(RWslope[0])
    print 'FeI-FeII = {}'.format(Iondiff)
    print 'Teff = {}'.format(Teff)
    print 'logg = {}'.format(logg)
    print 'xi = {}'.format(xi)
    print 'FeI = {} +/- {} ({})'.format(ablist[0],ablist[1],int(ablist[2]))
    print 'FeII = {} +/- {} ({})'.format(ablist[3],ablist[4],int(ablist[5]))
    return psumlist

#-------------- CREATE PHOTOMETRIC PARAMETER FILE ----------------------------#
#-- Creates photo.param file from photometry file photometry.txt.
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

