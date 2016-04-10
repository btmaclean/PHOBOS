#!/usr/local/bin/python

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
    fe_h = ablist[0] - 7.5
    psumlist = [EPslope[0],RWslope[0],Iondiff,ablist[0],ablist[1],int(ablist[2]),ablist[3],ablist[4],ablist[5]]
    print 'EP slope = {}'.format(EPslope[0])
    print 'RW slope = {}'.format(RWslope[0])
    print 'FeI-FeII = {}'.format(Iondiff)
    print 'Teff = {}'.format(Teff)
    print 'logg = {}'.format(logg)
    print 'xi = {}'.format(xi)
    print 'FeI = {} +/- {} ({})'.format(fe_h,ablist[1],int(ablist[2]))
    print 'FeII = {} +/- {} ({})'.format(ablist[3],ablist[4],int(ablist[5]))
    return psumlist