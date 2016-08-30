#!/usr/local/bin/python

#--------------- FE-PHOBOS -------------------#
#-- The first step for a new star, creates a model from original parameter estimates, runs ARES EW measurement code, and runs EWs through MOOG to give an initial metallicity. To be called from Phobos after a check for whether a moog_input line list exists yet.

#-- !!!USE ONLY ONCE AS THIS WILL UNDO ANY LINE CULLING OR MANUAL CORRECTIONS IF CHECK FAILS!!!

#-- Check for existence of a moog_input line file, otherwise the ARES section of this script would overwrite it if it does.
if not os.path.exists('moog_input/'):
	os.mkdir('moog_input/')

if os.path.exists('moog_input/{}.fe.lines'.format(name)):
	pyclean(scriptloc)
	sys.exit('\nMoog_input line file already exists! Something is wrong in Parameter-Phobos to get here!')

operation = raw_input('\nAre you sure you want to run Fe-Phobos? [y/N] ')
if operation.lower().startswith('y'):
	print 'Beginning Fe-Phobos'
else:
	pyclean(scriptloc)
	sys.exit('\nExiting Fe-Phobos')

#-------------- CASTELLI -------------------------#
#-- Creates a MOOG friendly atmospheric model.

model(name,location,Teff,logg,xi,fe_h)

#-------------- ARES ----------------------------#
#-- Run star through ARES, and prepares the MOOG input file from the ARES output file and line list.

ares(name,location,feelements,linelist_fe,linelist_elements)

#--------------- MOOG -------------------------#
#-- Make a MOOG parameter file for each star, run through MOOG and summarise abundances in a text file in root analysis directory.

plotornot = 1
moog(star,name,feelements,location,plotornot)
X_lines_summary(name,location,feelements)

#-- Opens the moog_output and moog_input line files in chosen.
subprocess.Popen(['{}'.format(texteditor), '{}'.format(linelist_fe)])
subprocess.Popen(['{}'.format(texteditor), 'photo.params'])
subprocess.Popen(['{}'.format(texteditor), 'spectro.params'])
subprocess.Popen(['{}'.format(texteditor), 'moog_out2/{n}.out2'.format(n=name)])
subprocess.Popen(['{}'.format(texteditor), 'moog_input/{n}.fe.lines'.format(n=name)])

#-- Create arrays: 'ablist' that contains an abundance value or stdev in each element; 'EPslope' and 'RWslope' which contain each value for FeI and FeII; and 'Iondiff' which specifies FeI-FeII.
psumlist = psum(name,Teff,logg,xi)

pyclean(scriptloc)
sys.exit('\nFe-Phobos has executed for {n} (star {s}), please consider a line check before running Phobos again.'.format(n=name,s=star))