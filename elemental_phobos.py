#!/usr/local/bin/python

#--------------- ELEMENTS_PHOBOS -------------------#
#-- This is pretty much the same as Fe-Phobos, except that is used the elemental line list (no fe lines).

#-- Check for existence of a moog_input line file, otherwise the ARES section of this script would overwrite it if it does.
if not os.path.exists('moog_input/'):
    os.mkdir('moog_input/')
if not os.path.exists('backups/'):
    os.mkdir('backups/')

#-- Set metallicity to the value determined by Fe-Phobos, or last Parameter-Phobos run.
psumlist = psum(name,Teff,logg,xi)
fe_h = psumlist[3] - 7.5

if os.path.exists('moog_input/{}.elements.lines'.format(name)):
    print 'Moog_input line file already exists, running MOOG on input file.'
    plotornot = 0
    model(name,location,Teff,logg,xi,fe_h)
    moog(star,name,feelements,location,plotornot)
    subprocess.Popen(['{}'.format(texteditor), 'moog_out2/{n}.out2'.format(n=name)])
    subprocess.Popen(['{}'.format(texteditor), 'moog_input/{n}.elements.lines'.format(n=name)])
    shutil.copy('moog_input/{}.elements.lines'.format(name),'backups/{}.elements.lines'.format(name))
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

#-- Opens the moog_output and moog_input line files in chosen.
subprocess.Popen(['{}'.format(texteditor), 'moog_out2/{n}.out2'.format(n=name)])
subprocess.Popen(['{}'.format(texteditor), 'moog_input/{n}.elements.lines'.format(n=name)])

if not os.path.exists('backups/'):
    os.mkdir('backups/')
shutil.copy('moog_input/{}.elements.lines'.format(name),'backups/{}.elements.lines'.format(name))

pyclean(scriptloc)
sys.exit('\nElemental-Phobos succeeded for {n} (star {s}). Please check the file moog_out2/{n}.out2 for elemental abundances.'.format(n=name,s=star))