#!/usr/local/bin/python

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
        
    print final_array_blue
    print final_array_grir
    
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