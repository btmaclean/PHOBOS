#!/usr/local/bin/python

#--------------- PARAMETER_PHOBOS -------------------#
#-- This is the MAIN Phobos scripts, which minimizes EP-slope, RW-slope and Ion-Difference to calculate stellar parameters, based on EW measurements made by Fe-Phobos or by hand.

#-- Check for existence of a moog_input line file. If exists, Phobos runs. If not, Fe-Phobos runs.
if not os.path.exists('moog_input/'):
	os.mkdir('moog_input/')

if os.path.exists('moog_input/{}.fe.lines'.format(name)):
	print 'Moog_input line file exists, Phobos will run.'
else:
	print 'No moog_input line file exists yet. Running Fe-Phobos.'
	execfile('{}/fe_phobos.py'.format(scriptloc))
	pyclean(scriptloc)
	sys.exit()

#-- Set metallicity to the value determined by Fe-Phobos, or last Parameter-Phobos run.
psumlist = psum(name,Teff,logg,xi)
fe_h = psumlist[3] - 7.5

#-- Initial run of model/moog with original parameters.
model(name,location,Teff,logg,xi,fe_h)
plotornot = 0
moog(star,name,feelements,location,plotornot)

#-- Opens the moog_output and moog_input line files in chosen.
subprocess.Popen(['{}'.format(texteditor), 'photo.params'])
subprocess.Popen(['{}'.format(texteditor), 'spectro.params'])
subprocess.Popen(['{}'.format(texteditor), 'moog_input/{n}.fe.lines'.format(n=name)])
subprocess.Popen(['{}'.format(texteditor), 'moog_out2/{n}.out2'.format(n=name)])

#-- Create arrays: 'ablist' that contains an abundance value or stdev in each element; 'EPslope' and 'RWslope' which contain each value for FeI and FeII; and 'psumlist[2]' which specifies FeI-FeII.
psumlist = psum(name,Teff,logg,xi)
fe_h = psumlist[3] - 7.5
#-- Set original values for Runaway-Phobos error.
Tefforig = Teff
loggorig = logg
xiorig = xi

def resetparamstoorig(name,location,Teff,Tefforig,logg,loggorig,xi,xiorig,fe_h,star,feelements):
	Teff = Tefforig
	logg = loggorig
	xi = xiorig
	model(name,location,Teff,logg,xi,fe_h)
	plotornot = 1
	moog(star,name,feelements,location,plotornot)
	return

Teffbounds = 1000
xibounds = 1
loggbounds = 1

#-- MINIMIZE EP slope, RW slope, and Ion Difference by testing varying parameters sequentially until the 3 values are in a minimum range.

#-- Take 1 (no logg, slope tolerance 0.025)

#-- Teff
if psumlist[0] <= -0.025:
	while psumlist[0] <= -0.025:
		Teff = Teff - 10
		if abs(Tefforig - Teff) >= Teffbounds:
			resetparamstoorig(name,location,Teff,Tefforig,logg,loggorig,xi,xiorig,fe_h,star,feelements)
			pyclean(scriptloc)
			sys.exit('\nRunaway-Phobos error: Teff altered by >{}K, please check EWs.\nParameters reset to photometric.'.format(Teffbounds))
		model(name,location,Teff,logg,xi,fe_h)
		if not os.path.exists('models/{}.model.dat'.format(name)):
			pyclean(scriptloc)
			sys.exit('{} failed model creation'.format(name))
		moog(star,name,feelements,location,plotornot) 
		psumlist = psum(name,Teff,logg,xi)
		fe_h = psumlist[3] - 7.5
elif psumlist[0] >= 0.025:
	while psumlist[0] >= 0.025:
		Teff = Teff + 10
		if abs(Tefforig - Teff) >= Teffbounds:
			resetparamstoorig(name,location,Teff,Tefforig,logg,loggorig,xi,xiorig,fe_h,star,feelements)
			pyclean(scriptloc)
			sys.exit('\nRunaway-Phobos error: Teff altered by >{}K, please check EWs.\nParameters reset to photometric.'.format(Teffbounds))
		model(name,location,Teff,logg,xi,fe_h)
		if not os.path.exists('models/{}.model.dat'.format(name)):
			pyclean(scriptloc)
			sys.exit('{} failed model creation'.format(name))
		moog(star,name,feelements,location,plotornot) 
		psumlist = psum(name,Teff,logg,xi)
		fe_h = psumlist[3] - 7.5
else: print 'EP slope within tolerance'

#-- xi
if psumlist[1] <= -0.025:
	while psumlist[1] <= -0.025:
		xi = xi - 0.05
		if abs(xiorig - xi) >= xibounds:
			resetparamstoorig(name,location,Teff,Tefforig,logg,loggorig,xi,xiorig,fe_h,star,feelements)
			pyclean(scriptloc)
			sys.exit('\nRunaway-Phobos error: microturbulence altered by >{} km/s, please check EWs.\nParameters reset to photometric.'.format(xibounds))
		model(name,location,Teff,logg,xi,fe_h)
		if not os.path.exists('models/{}.model.dat'.format(name)):
			pyclean(scriptloc)
			sys.exit('{} failed model creation'.format(name))
		moog(star,name,feelements,location,plotornot) 
		psumlist = psum(name,Teff,logg,xi)
		fe_h = psumlist[3] - 7.5
elif psumlist[1] >= 0.025:
	while psumlist[1] >= 0.025:
		xi = xi + 0.05
		if abs(xiorig - xi) >= xibounds:
			resetparamstoorig(name,location,Teff,Tefforig,logg,loggorig,xi,xiorig,fe_h,star,feelements)
			pyclean(scriptloc)
			sys.exit('\nRunaway-Phobos error: microturbulence altered by >{} km/s, please check EWs.\nParameters reset to photometric.'.format(xibounds))
		model(name,location,Teff,logg,xi,fe_h)
		if not os.path.exists('models/{}.model.dat'.format(name)):
			pyclean(scriptloc)
			sys.exit('{} failed model creation'.format(name))
		moog(star,name,feelements,location,plotornot) 
		psumlist = psum(name,Teff,logg,xi)
		fe_h = psumlist[3] - 7.5
else: print 'RW slope within tolerance'

#-- Take 2 (no logg, slope tolerance 0.02)

#-- Teff
if psumlist[0] <= -0.02:
	while psumlist[0] <= -0.02:
		Teff = Teff - 10
		if abs(Tefforig - Teff) >= Teffbounds:
			resetparamstoorig(name,location,Teff,Tefforig,logg,loggorig,xi,xiorig,fe_h,star,feelements)
			pyclean(scriptloc)
			sys.exit('\nRunaway-Phobos error: Teff altered by >{}K, please check EWs.\nParameters reset to photometric.'.format(Teffbounds))
		model(name,location,Teff,logg,xi,fe_h)
		if not os.path.exists('models/{}.model.dat'.format(name)):
			pyclean(scriptloc)
			sys.exit('{} failed model creation'.format(name))
		moog(star,name,feelements,location,plotornot) 
		psumlist = psum(name,Teff,logg,xi)
		fe_h = psumlist[3] - 7.5
elif psumlist[0] >= 0.02:
	while psumlist[0] >= 0.02:
		Teff = Teff + 10
		if abs(Tefforig - Teff) >= Teffbounds:
			resetparamstoorig(name,location,Teff,Tefforig,logg,loggorig,xi,xiorig,fe_h,star,feelements)
			pyclean(scriptloc)
			sys.exit('\nRunaway-Phobos error: Teff altered by >{}K, please check EWs.\nParameters reset to photometric.'.format(Teffbounds))
		model(name,location,Teff,logg,xi,fe_h)
		if not os.path.exists('models/{}.model.dat'.format(name)):
			pyclean(scriptloc)
			sys.exit('{} failed model creation'.format(name))
		moog(star,name,feelements,location,plotornot) 
		psumlist = psum(name,Teff,logg,xi)
		fe_h = psumlist[3] - 7.5
else: print 'EP slope within tolerance'

#-- xi
if psumlist[1] <= -0.02:
	while psumlist[1] <= -0.02:
		xi = xi - 0.05
		if abs(xiorig - xi) >= xibounds:
			resetparamstoorig(name,location,Teff,Tefforig,logg,loggorig,xi,xiorig,fe_h,star,feelements)
			pyclean(scriptloc)
			sys.exit('\nRunaway-Phobos error: microturbulence altered by >{} km/s, please check EWs.\nParameters reset to photometric.'.format(xibounds))
		model(name,location,Teff,logg,xi,fe_h)
		if not os.path.exists('models/{}.model.dat'.format(name)):
			pyclean(scriptloc)
			sys.exit('{} failed model creation'.format(name))
		moog(star,name,feelements,location,plotornot) 
		psumlist = psum(name,Teff,logg,xi)
		fe_h = psumlist[3] - 7.5
elif psumlist[1] >= 0.02:
	while psumlist[1] >= 0.02:
		xi = xi + 0.05
		if abs(xiorig - xi) >= xibounds:
			resetparamstoorig(name,location,Teff,Tefforig,logg,loggorig,xi,xiorig,fe_h,star,feelements)
			pyclean(scriptloc)
			sys.exit('\nRunaway-Phobos error: microturbulence altered by >{} km/s, please check EWs.\nParameters reset to photometric.'.format(xibounds))
		model(name,location,Teff,logg,xi,fe_h)
		if not os.path.exists('models/{}.model.dat'.format(name)):
			pyclean(scriptloc)
			sys.exit('{} failed model creation'.format(name))
		moog(star,name,feelements,location,plotornot) 
		psumlist = psum(name,Teff,logg,xi)
		fe_h = psumlist[3] - 7.5
else: print 'RW slope within tolerance'

#-- Take 3 (with logg, slope tolerance 0.015, psumlist[2] tolerance 0.15 dex)

#-- Teff
if psumlist[0] <= -0.015:
	while psumlist[0] <= -0.015:
		Teff = Teff - 10
		if abs(Tefforig - Teff) >= Teffbounds:
			resetparamstoorig(name,location,Teff,Tefforig,logg,loggorig,xi,xiorig,fe_h,star,feelements)
			pyclean(scriptloc)
			sys.exit('\nRunaway-Phobos error: Teff altered by >{}K, please check EWs.\nParameters reset to photometric.'.format(Teffbounds))
		model(name,location,Teff,logg,xi,fe_h)
		if not os.path.exists('models/{}.model.dat'.format(name)):
			pyclean(scriptloc)
			sys.exit('{} failed model creation'.format(name))
		moog(star,name,feelements,location,plotornot) 
		psumlist = psum(name,Teff,logg,xi)
		fe_h = psumlist[3] - 7.5
elif psumlist[0] >= 0.015:
	while psumlist[0] >= 0.015:
		Teff = Teff + 10
		if abs(Tefforig - Teff) >= Teffbounds:
			resetparamstoorig(name,location,Teff,Tefforig,logg,loggorig,xi,xiorig,fe_h,star,feelements)
			pyclean(scriptloc)
			sys.exit('\nRunaway-Phobos error: Teff altered by >{}K, please check EWs.\nParameters reset to photometric.'.format(Teffbounds))
		model(name,location,Teff,logg,xi,fe_h)
		if not os.path.exists('models/{}.model.dat'.format(name)):
			pyclean(scriptloc)
			sys.exit('{} failed model creation'.format(name))
		moog(star,name,feelements,location,plotornot) 
		psumlist = psum(name,Teff,logg,xi)
		fe_h = psumlist[3] - 7.5
else: print 'EP slope within tolerance'

#-- xi
if psumlist[1] <= -0.015:
	while psumlist[1] <= -0.015:
		xi = xi - 0.05
		if abs(xiorig - xi) >= xibounds:
			resetparamstoorig(name,location,Teff,Tefforig,logg,loggorig,xi,xiorig,fe_h,star,feelements)
			pyclean(scriptloc)
			sys.exit('\nRunaway-Phobos error: microturbulence altered by >{} km/s, please check EWs.\nParameters reset to photometric.'.format(xibounds))
		model(name,location,Teff,logg,xi,fe_h)
		if not os.path.exists('models/{}.model.dat'.format(name)):
			pyclean(scriptloc)
			sys.exit('{} failed model creation'.format(name))
		moog(star,name,feelements,location,plotornot) 
		psumlist = psum(name,Teff,logg,xi)
		fe_h = psumlist[3] - 7.5
elif psumlist[1] >= 0.015:
	while psumlist[1] >= 0.015:
		xi = xi + 0.05
		if abs(xiorig - xi) >= xibounds:
			resetparamstoorig(name,location,Teff,Tefforig,logg,loggorig,xi,xiorig,fe_h,star,feelements)
			pyclean(scriptloc)
			sys.exit('\nRunaway-Phobos error: microturbulence altered by >{} km/s, please check EWs.\nParameters reset to photometric.'.format(xibounds))
		model(name,location,Teff,logg,xi,fe_h)
		if not os.path.exists('models/{}.model.dat'.format(name)):
			pyclean(scriptloc)
			sys.exit('{} failed model creation'.format(name))
		moog(star,name,feelements,location,plotornot) 
		psumlist = psum(name,Teff,logg,xi)
		fe_h = psumlist[3] - 7.5
else: print 'RW slope within tolerance'

#-- logg
if 'AGB' in name:
	print 'AGB star. Skipping ionization balance'
else:
	if psumlist[2] <= -0.15:
		while psumlist[2] <= -0.15:
			logg = logg - 0.05
			if abs(loggorig - logg) >= loggbounds:
				resetparamstoorig(name,location,Teff,Tefforig,logg,loggorig,xi,xiorig,fe_h,star,feelements)
				sys.exit('\nRunaway-Phobos error: log(g) altered by >{} dex, please check EWs.\nParameters reset to photometric.'.format(loggbounds))
			model(name,location,Teff,logg,xi,fe_h)
			if not os.path.exists('models/{}.model.dat'.format(name)):
				pyclean(scriptloc)
				sys.exit('{} failed model creation'.format(name))
			moog(star,name,feelements,location,plotornot) 
			psumlist = psum(name,Teff,logg,xi)
			fe_h = psumlist[3] - 7.5
	elif psumlist[2] >= 0.15:
		while psumlist[2] >= 0.15:
			logg = logg + 0.05
			if abs(loggorig - logg) >= loggbounds:
				resetparamstoorig(name,location,Teff,Tefforig,logg,loggorig,xi,xiorig,fe_h,star,feelements)
				sys.exit('\nRunaway-Phobos error: log(g) altered by >{} dex, please check EWs.\nParameters reset to photometric.'.format(loggbounds))
			model(name,location,Teff,logg,xi,fe_h)
			if not os.path.exists('models/{}.model.dat'.format(name)):
				pyclean(scriptloc)
				sys.exit('{} failed model creation'.format(name))
			moog(star,name,feelements,location,plotornot) 
			psumlist = psum(name,Teff,logg,xi)
			fe_h = psumlist[3] - 7.5
	else: print 'Fe I - Fe II within tolerance'

#-- Take 4 (with logg, slope tolerance 0.015, psumlist[2] tolerance 0.1 dex)

#-- Teff
if psumlist[0] <= -0.015:
	while psumlist[0] <= -0.015:
		Teff = Teff - 10
		if abs(Tefforig - Teff) >= Teffbounds:
			resetparamstoorig(name,location,Teff,Tefforig,logg,loggorig,xi,xiorig,fe_h,star,feelements)
			pyclean(scriptloc)
			sys.exit('\nRunaway-Phobos error: Teff altered by >{}K, please check EWs.\nParameters reset to photometric.'.format(Teffbounds))
		model(name,location,Teff,logg,xi,fe_h)
		if not os.path.exists('models/{}.model.dat'.format(name)):
			pyclean(scriptloc)
			sys.exit('{} failed model creation'.format(name))
		moog(star,name,feelements,location,plotornot) 
		psumlist = psum(name,Teff,logg,xi)
		fe_h = psumlist[3] - 7.5
elif psumlist[0] >= 0.015:
	while psumlist[0] >= 0.015:
		Teff = Teff + 10
		if abs(Tefforig - Teff) >= Teffbounds:
			resetparamstoorig(name,location,Teff,Tefforig,logg,loggorig,xi,xiorig,fe_h,star,feelements)
			pyclean(scriptloc)
			sys.exit('\nRunaway-Phobos error: Teff altered by >{}K, please check EWs.\nParameters reset to photometric.'.format(Teffbounds))
		model(name,location,Teff,logg,xi,fe_h)
		if not os.path.exists('models/{}.model.dat'.format(name)):
			pyclean(scriptloc)
			sys.exit('{} failed model creation'.format(name))
		moog(star,name,feelements,location,plotornot) 
		psumlist = psum(name,Teff,logg,xi)
		fe_h = psumlist[3] - 7.5
else: print 'EP slope within tolerance'

#-- xi
if psumlist[1] <= -0.015:
	while psumlist[1] <= -0.015:
		xi = xi - 0.05
		if abs(xiorig - xi) >= xibounds:
			resetparamstoorig(name,location,Teff,Tefforig,logg,loggorig,xi,xiorig,fe_h,star,feelements)
			pyclean(scriptloc)
			sys.exit('\nRunaway-Phobos error: microturbulence altered by >{} km/s, please check EWs.\nParameters reset to photometric.'.format(xibounds))
		model(name,location,Teff,logg,xi,fe_h)
		if not os.path.exists('models/{}.model.dat'.format(name)):
			pyclean(scriptloc)
			sys.exit('{} failed model creation'.format(name))
		moog(star,name,feelements,location,plotornot) 
		psumlist = psum(name,Teff,logg,xi)
		fe_h = psumlist[3] - 7.5
elif psumlist[1] >= 0.015:
	while psumlist[1] >= 0.015:
		xi = xi + 0.05
		if abs(xiorig - xi) >= xibounds:
			resetparamstoorig(name,location,Teff,Tefforig,logg,loggorig,xi,xiorig,fe_h,star,feelements)
			pyclean(scriptloc)
			sys.exit('\nRunaway-Phobos error: microturbulence altered by >{} km/s, please check EWs.\nParameters reset to photometric.'.format(xibounds))
		model(name,location,Teff,logg,xi,fe_h)
		if not os.path.exists('models/{}.model.dat'.format(name)):
			pyclean(scriptloc)
			sys.exit('{} failed model creation'.format(name))
		moog(star,name,feelements,location,plotornot) 
		psumlist = psum(name,Teff,logg,xi)
		fe_h = psumlist[3] - 7.5
else: print 'RW slope within tolerance'

#-- logg
if 'AGB' in name:
	print 'AGB star. Skipping ionization balance'
else:
	if psumlist[2] <= -0.1:
		while psumlist[2] <= -0.1:
			logg = logg - 0.05
			if abs(loggorig - logg) >= loggbounds:
				resetparamstoorig(name,location,Teff,Tefforig,logg,loggorig,xi,xiorig,fe_h,star,feelements)
				sys.exit('\nRunaway-Phobos error: log(g) altered by >{} dex, please check EWs.\nParameters reset to photometric.'.format(loggbounds))
			model(name,location,Teff,logg,xi,fe_h)
			if not os.path.exists('models/{}.model.dat'.format(name)):
				pyclean(scriptloc)
				sys.exit('{} failed model creation'.format(name))
			moog(star,name,feelements,location,plotornot) 
			psumlist = psum(name,Teff,logg,xi)
			fe_h = psumlist[3] - 7.5
	elif psumlist[2] >= 0.1:
		while psumlist[2] >= 0.1:
			logg = logg + 0.05
			if abs(loggorig - logg) >= loggbounds:
				resetparamstoorig(name,location,Teff,Tefforig,logg,loggorig,xi,xiorig,fe_h,star,feelements)
				sys.exit('\nRunaway-Phobos error: log(g) altered by >{} dex, please check EWs.\nParameters reset to photometric.'.format(loggbounds))
			model(name,location,Teff,logg,xi,fe_h)
			if not os.path.exists('models/{}.model.dat'.format(name)):
				pyclean(scriptloc)
				sys.exit('{} failed model creation'.format(name))
			moog(star,name,feelements,location,plotornot) 
			psumlist = psum(name,Teff,logg,xi)
			fe_h = psumlist[3] - 7.5
	else: print 'Fe I - Fe II within tolerance'

#-- Recreates MOOG parameter with plotting activated.
plotornot = 1
moog(star,name,feelements,location,plotornot)
X_lines_summary(name,location,feelements)

#-- Display final parameters.
print '\n\n\n\n\nPhobos succeeded for {n} (star {s}).'.format(n=name,s=star)
psumlist = psum(name,Teff,logg,xi)
fe_h = psumlist[3] - 7.5
print '\nSpec Params: {}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(Teff,logg,xi,psumlist[3],psumlist[4],psumlist[5],psumlist[6],psumlist[7],psumlist[8])

#-- Update spectroscopic parameter file and backup moog_input line file.
params[arrayelement][1] = int(Teff)
params[arrayelement][2] = logg
params[arrayelement][3] = xi
np.savetxt('spectro.params', params, fmt='%s')
if not os.path.exists('backups/'):
	os.mkdir('backups/')
shutil.copy('moog_input/{}.fe.lines'.format(name),'backups/{}.fe.lines'.format(name))


pyclean(scriptloc)
sys.exit('\nParameter-Phobos has executed for {n} (star {s}), please consider a line check before running Phobos again.'.format(n=name,s=star))