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

if not os.path.exists('phobos_iterations/'):
	os.mkdir('phobos_iterations/')

if os.path.exists('phobos_iterations/{}.iterations'.format(name)):
	os.remove('phobos_iterations/{}.iterations'.format(name))

#-- Initial run of model/moog with original parameters.
model(name,location,Teff,logg,xi,fe_h)
plotornot = 0
moog(star,name,feelements,location,plotornot)

#-- Set metallicity to the value determined by Fe-Phobos, or last Parameter-Phobos run.
psumlist = psum(name,Teff,logg,xi)
fe_h = psumlist[3] - 7.5
iteration = [(Teff,logg,xi,psumlist[3],psumlist[4],psumlist[6],psumlist[7],psumlist[0],psumlist[1])]
with open('phobos_iterations/{}.iterations'.format(name),'a') as f_handle:
    np.savetxt(f_handle,iteration,delimiter=' ',fmt='%s')

def slope_err(name,location):
	EPs = np.genfromtxt('moog_out2/{}.out2'.format(name),skip_header=6,skip_footer=15,usecols=2)
	RWs = np.genfromtxt('moog_out2/{}.out2'.format(name),skip_header=6,skip_footer=15,usecols=5)
	Fes = np.genfromtxt('moog_out2/{}.out2'.format(name),skip_header=6,skip_footer=15,usecols=6) 
	slope1, intercept1, r_value1, p_value1, EP_slope_err = stats.linregress(EPs,Fes)
	slope2, intercept2, r_value2, p_value2, RW_slope_err = stats.linregress(RWs,Fes)
	return EP_slope_err, RW_slope_err

def Teff_analysis(name,location,Teff,logg,xi,Vmag,fe_h,star,feelements,dist_mod,EP_slope_err,Trange):
	model(name,location,Teff,logg,xi,fe_h)
	if not os.path.exists('models/{}.model.dat'.format(name)):
		pyclean(scriptloc)
		sys.exit('{} failed model creation'.format(name))
	moog(star,name,feelements,location,plotornot) 
	psumlist = psum(name,Teff,logg,xi)
	EPslopeph = psumlist[0]
	Teffp = Teff + Trange
	model(name,location,Teffp,logg,xi,fe_h)
	if not os.path.exists('models/{}.model.dat'.format(name)):
		pyclean(scriptloc)
		sys.exit('{} failed model creation'.format(name))
	moog(star,name,feelements,location,plotornot) 
	psumlist = psum(name,Teffp,logg,xi)
	EPslopep = psumlist[0]
	Teffm = Teff - Trange
	if Teffm < 3500:
		Teffm = 3501
	model(name,location,Teffm,logg,xi,fe_h)
	if not os.path.exists('models/{}.model.dat'.format(name)):
		pyclean(scriptloc)
		sys.exit('{} failed model creation'.format(name))
	moog(star,name,feelements,location,plotornot) 
	psumlist = psum(name,Teffm,logg,xi)
	EPslopem = psumlist[0]
	m = -400/(EPslopem - EPslopep)
	Teff =  int(round(Teff - m*EPslopeph))
	if Teff < 3500:
		Teff = 3500
	Teffuncert = abs(int(round(m*EP_slope_err - m*-EP_slope_err))/2)
	return Teff, Teffuncert

def xi_analysis(name,location,Teff,logg,xi,Vmag,fe_h,star,feelements,dist_mod,RW_slope_err,xirange):
	model(name,location,Teff,logg,xi,fe_h)
	if not os.path.exists('models/{}.model.dat'.format(name)):
		pyclean(scriptloc)
		sys.exit('{} failed model creation'.format(name))
	moog(star,name,feelements,location,plotornot) 
	psumlist = psum(name,Teff,logg,xi)
	RWslopeph = psumlist[1]
	xip = xi + xirange
	model(name,location,Teff,logg,xip,fe_h)
	if not os.path.exists('models/{}.model.dat'.format(name)):
		pyclean(scriptloc)
		sys.exit('{} failed model creation'.format(name))
	moog(star,name,feelements,location,plotornot) 
	psumlist = psum(name,Teff,logg,xip)
	RWslopep = psumlist[1]
	xim = xi - xirange
	model(name,location,Teff,logg,xim,fe_h)
	if not os.path.exists('models/{}.model.dat'.format(name)):
		pyclean(scriptloc)
		sys.exit('{} failed model creation'.format(name))
	moog(star,name,feelements,location,plotornot) 
	psumlist = psum(name,Teff,logg,xim)
	RWslopem = psumlist[1]
	m = -0.4/(RWslopem - RWslopep)
	xi =  round(xi - m*RWslopeph, 2)
	xiuncert = round(abs((m*RW_slope_err - m*-RW_slope_err)/2), 2)
	return xi, xiuncert

def recalc_ph_logg(name,location,Teff,logg,xi,Vmag,fe_h,star,feelements,dist_mod):
	psumlist = psum(name,Teff,logg,xi)
	fe_h = psumlist[3] - 7.5
	if 'AGB' in name:
		if Teff <= 4677:
			logg = round(4.44+math.log10(0.65)+0.4*(Vmag-dist_mod+((-5.531*10**(-2))/(math.log10(Teff)-3.52))-0.6177+(4.42*(math.log10(Teff)-3.52))-2.669*((math.log10(Teff)-3.52)**2)+(0.6943*(math.log10(Teff)-3.52)*-1.1)-0.1071*-1.1-(8.612*10**(-3))*(-1.1**2)-4.72)+4*math.log10(Teff)-15.0447, 2)
		else:
			logg = round(4.44+math.log10(0.65)+0.4*(Vmag-dist_mod+((-9.93*10**(-2))/(math.log10(Teff)-3.52))+2.887*10**(-2)+(2.275*(math.log10(Teff)-3.52))-4.425*((math.log10(Teff)-3.52)**2)+(0.3505*(math.log10(Teff)-3.52)*-1.1)-(5.558*10**(-2))*-1.1-(5.375*10**(-3))*(-1.1**2)-4.72)+4*math.log10(Teff)-15.0447, 2)
	else:
			if Teff <= 4677:
				logg = round(4.44+math.log10(0.8)+0.4*(Vmag-dist_mod+((-5.531*10**(-2))/(math.log10(Teff)-3.52))-0.6177+(4.42*(math.log10(Teff)-3.52))-2.669*((math.log10(Teff)-3.52)**2)+(0.6943*(math.log10(Teff)-3.52)*-1.1)-0.1071*-1.1-(8.612*10**(-3))*(-1.1**2)-4.72)+4*math.log10(Teff)-15.0447, 2)
			else:
				logg = round(4.44+math.log10(0.8)+0.4*(Vmag-dist_mod+((-9.93*10**(-2))/(math.log10(Teff)-3.52))+2.887*10**(-2)+(2.275*(math.log10(Teff)-3.52))-4.425*((math.log10(Teff)-3.52)**2)+(0.3505*(math.log10(Teff)-3.52)*-1.1)-(5.558*10**(-2))*-1.1-(5.375*10**(-3))*(-1.1**2)-4.72)+4*math.log10(Teff)-15.0447, 2)
	if logg < 0.0:
		logg = 0.0
	return logg, fe_h

def param_analysis(name,location,Teff,logg,xi,Vmag,fe_h,star,feelements,dist_mod,Trange,xirange):
	EP_slope_err, RW_slope_err = slope_err(name,location)
	Teff, Teffuncert = Teff_analysis(name,location,Teff,logg,xi,Vmag,fe_h,star,feelements,dist_mod,EP_slope_err,Trange)
	xi, xiuncert = xi_analysis(name,location,Teff,logg,xi,Vmag,fe_h,star,feelements,dist_mod,RW_slope_err,xirange)
	logg, fe_h = recalc_ph_logg(name,location,Teff,logg,xi,Vmag,fe_h,star,feelements,dist_mod)
	model(name,location,Teff,logg,xi,fe_h)
	if not os.path.exists('models/{}.model.dat'.format(name)):
		pyclean(scriptloc)
		sys.exit('{} failed model creation'.format(name))
	moog(star,name,feelements,location,plotornot)
	psumlist = psum(name,Teff,logg,xi)
	iteration = [(Teff,logg,xi,psumlist[3],psumlist[4],psumlist[6],psumlist[7],psumlist[0],psumlist[1])]
	with open('phobos_iterations/{}.iterations'.format(name),'a') as f_handle:
	    np.savetxt(f_handle,iteration,delimiter=' ',fmt='%s')
	return (Teff, Teffuncert, logg, xi, xiuncert, fe_h)

Trange = 200
xirange = 0.2
Teff, Teffuncert, logg, xi, xiuncert, fe_h = param_analysis(name,location,Teff,logg,xi,Vmag,fe_h,star,feelements,dist_mod,Trange,xirange)
Teff, Teffuncert, logg, xi, xiuncert, fe_h = param_analysis(name,location,Teff,logg,xi,Vmag,fe_h,star,feelements,dist_mod,Trange,xirange)
Teff, Teffuncert, logg, xi, xiuncert, fe_h = param_analysis(name,location,Teff,logg,xi,Vmag,fe_h,star,feelements,dist_mod,Trange,xirange)

count = 0
while abs(psumlist[0]) >= 0.005:
	Teff, Teffuncert, logg, xi, xiuncert, fe_h = param_analysis(name,location,Teff,logg,xi,Vmag,fe_h,star,feelements,dist_mod,Trange,xirange)
	count = count + 1
	if count >= 5:
		break
	
if abs(psumlist[1]) >= 0.003:
	Teff, Teffuncert, logg, xi, xiuncert, fe_h = param_analysis(name,location,Teff,logg,xi,Vmag,fe_h,star,feelements,dist_mod,Trange,xirange)
if abs(psumlist[0]) >= 0.005:
	Teff, Teffuncert, logg, xi, xiuncert, fe_h = param_analysis(name,location,Teff,logg,xi,Vmag,fe_h,star,feelements,dist_mod,Trange,xirange)
if abs(psumlist[1]) >= 0.002:
	Teff, Teffuncert, logg, xi, xiuncert, fe_h = param_analysis(name,location,Teff,logg,xi,Vmag,fe_h,star,feelements,dist_mod,Trange,xirange)


plotornot = 0
model(name,location,Teff,logg,xi,fe_h)
moog(star,name,feelements,location,plotornot)
X_lines_summary(name,location,feelements)

#-- Display final parameters.
psumlist = psum(name,Teff,logg,xi)
fe_h = psumlist[3] - 7.5
print '\nSpec Params: Teff\tTeff_u\tlogg\txi\txi_u\tFeI\tFeI_u\tFeII\tFeII_u\tEP_sl\tRW_sl'
print 'Spec Params: {}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(Teff,Teffuncert,logg,xi,xiuncert,psumlist[3],psumlist[4],psumlist[6],psumlist[7],psumlist[0],psumlist[1])

#-- Update spectroscopic parameter file and backup moog_input line file.
params[arrayelement][1] = int(Teff)
params[arrayelement][2] = logg
params[arrayelement][3] = xi
np.savetxt('spectro.params', params, fmt='%s')
if not os.path.exists('backups/'):
	os.mkdir('backups/')
shutil.copy('moog_input/{}.fe.lines'.format(name),'backups/{}.fe.lines'.format(name))

results = [(name,Teff,Teffuncert,logg,xi,xiuncert,psumlist[3],psumlist[4],psumlist[6],psumlist[7],psumlist[0],psumlist[1])]
os.chdir('{}/X_line_abundance_summaries'.format(location))
with open('Fe_results.txt','a') as f_handle:
    np.savetxt(f_handle,results,delimiter=' ',fmt='%s')

os.chdir('{}'.format(location))
# subprocess.Popen(['{}'.format(texteditor), 'spectro.params'])
# subprocess.Popen(['{}'.format(texteditor), 'X_line_abundance_summaries/Fe_results.txt'])
# subprocess.Popen(['{}'.format(texteditor), 'moog_input/{n}.fe.lines'.format(n=name)])
# subprocess.Popen(['{}'.format(texteditor), 'moog_out2/{n}.out2'.format(n=name)])

pyclean(scriptloc)
#sys.exit('\nParameter-Phobos has executed for {n} (star {s}), please consider a line check before running Phobos again.'.format(n=name,s=star))
sys.exit('Phobos succeeded for {n} (star {s}).'.format(n=name,s=star).format(n=name,s=star))
