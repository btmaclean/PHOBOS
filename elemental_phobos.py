#!/usr/local/bin/python

#--------------- ELEMENTS_PHOBOS -------------------#
#-- This is pretty much the same as Fe-Phobos, except that is used the elemental line list (no fe lines).

#-- Check for existence of a moog_input line file, otherwise the ARES section of this script would overwrite it if it does.
print "THIS IS EDITED!!"
if not os.path.exists('moog_input/'):
    os.mkdir('moog_input/')
if not os.path.exists('backups/'):
    os.mkdir('backups/')

#-- Set metallicity to the value determined last Parameter-Phobos run if done. If Fe never done for star, use default value set in user_variables file.
if os.path.exists('moog_input/{}.fe.lines'.format(name)):
    #plotornot = 0
    #feelements = 'fe'
    #model(name,location,Teff,logg,xi,fe_h)
    #moog(star,name,feelements,location,plotornot)
    #psumlist = psum(name,Teff,logg,xi)
    #fe_h = psumlist[3] - 7.5
    #print '{}'.format(fe_h)
    feelements = 'elements'

if os.path.exists('moog_input/{}.elements.lines'.format(name)):
    print 'Moog_input line file already exists, running MOOG on input file.'
    plotornot = 0
    model(name,location,Teff,logg,xi,fe_h)
    moog(star,name,feelements,location,plotornot)
    X_lines_summary(name,location,feelements)
    # subprocess.Popen(['{}'.format(texteditor), 'moog_input/{n}.elements.lines'.format(n=name)])
    # subprocess.Popen(['{}'.format(texteditor), 'moog_out2/{n}.out2'.format(n=name)])
    shutil.copy('moog_input/{}.elements.lines'.format(name),'backups/{}.elements.lines'.format(name))
    # psumlist = psum(name,Teff,logg,xi)
    # results = [(name, psumlist[3],psumlist[4],psumlist[6],psumlist[7])]
    # os.chdir('{}/X_line_abundance_summaries'.format(location))
#     with open('Fe_results.txt','a') as f_handle:
#         np.savetxt(f_handle,results,delimiter=' ',fmt='%s')
    pyclean(scriptloc)
    sys.exit('\nElemental-Phobos succeeded for {n} (star {s}). Please check the file moog_out2/{n}.out2 for elemental abundances.'.format(n=name,s=star))
else:
    print 'No moog_input line file exists yet.'

operation = raw_input('\nAre you sure you want to run Elemental-Phobos? [y/N] ')
if operation.lower().startswith('y'):
    print 'Beginning Elemental-Phobos'
else:
    pyclean(scriptloc)
    sys.exit('\nExiting Elemental-Phobos')

#-------------- CASTELLI -------------------------#
#-- Creates a MOOG friendly atmospheric model.

model(name,location,Teff,logg,xi,fe_h)

#-------------- ARES ----------------------------#
#-- Run star through ARES, and prepares the MOOG input file from the ARES output file and line list.

ares(name,location,feelements,linelist_fe,linelist_elements)

#--------------- MOOG -------------------------#
#-- Make a MOOG parameter file for each star, run through MOOG and summarise abundances in a text file in root analysis directory.

plotornot = 0
moog(star,name,feelements,location,plotornot)
X_lines_summary(name,location,feelements)

#-- Opens the moog_output and moog_input line files in chosen.
subprocess.Popen(['{}'.format(texteditor), 'moog_input/{n}.elements.lines'.format(n=name)])
subprocess.Popen(['{}'.format(texteditor), 'moog_out2/{n}.out2'.format(n=name)])
subprocess.Popen(['{}'.format(texteditor), '{}'.format(linelist_elements)])

# psumlist = psum(name,Teff,logg,xi)
# results = [(name, psumlist[3],psumlist[4],psumlist[6],psumlist[7])]
# os.chdir('{}/X_line_abundance_summaries'.format(location))
# with open('Fe_results.txt','a') as f_handle:
#     np.savetxt(f_handle,results,delimiter=' ',fmt='%s')

if not os.path.exists('backups/'):
    os.mkdir('backups/')
shutil.copy('moog_input/{}.elements.lines'.format(name),'backups/{}.elements.lines'.format(name))

pyclean(scriptloc)
sys.exit('\nElemental-Phobos succeeded for {n} (star {s}). Please check the file moog_out2/{n}.out2 for elemental abundances.'.format(n=name,s=star))