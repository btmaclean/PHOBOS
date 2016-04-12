# PHOBOS
--------------------------INTRODUCTION

Phobos is a Python 2.7 pipeline for high-resolution spectroscopic parameter and abundance analysis following the ARES+MOOG analysis
method (Sousa, 2014; http://adsabs.harvard.edu/abs/2014arXiv1407.5817S).

Originally written to handle globular cluster spectra from the multi-fibre HERMES facility on the AAT (Siding Spring Observatory),
Phobos can be easily adapted for data from other high-facilities, or for different stellar targets (where reliable photometric
values and distances are known).

Written by B. T. Maclean, School of Physics and Astronomy, Monash University, Australia (ben.maclean@monash.edu.au).

--------------------------REQUIRED SOFTWARE

MOOG (June 2014, http://www.as.utexas.edu/~chris/moog.html)
-gfortran
-supermongo

ARES (v2, http://www.astro.up.pt/~sousasag/ares/)
-cfitsio
-gcc
-gsl
-OpenMP

makekurucz3 (*reference?*)

Python (at least v2.7)
-numpy

--------------------------INSTALLATION / SET-UP (FOLDERS AND FILES)

1. In the file 'user_variables.py', several strings and values must be defined before Phobos can be used. These include:

   location = 'path/to/analysis-folder'
   linelist_fe = 'path/to/iron-line-list'*
   linelist_elements = 'path/to/elemental-line-list'*
   texteditor = 'Terminal command to launch preferred text editor'
   fe_h = Initial metallicity estimate
   dist_mod = Distance modulus of star/cluster
   colour_scale = 'Photometric colour to be used for inital parameter estimate. Options: BV, VJ, VK, VH, or by'

   *Note that the list of iron lines must be in a separate file to the lines of the other elements.

2. In the analysis folder, there must a directory called 'fits' (i.e. path/to/analysis-folder/fits).
   In this directory must be 1 dimensional spectra, one for each star, called 'star-name.fits' 
   (e.g., AGB00788.fits
          AGB03590.fits)

3. In the analysis folder, there must be a file called photometry.txt (i.e. path/to/analysis-folder/photometry.txt).
   This file must have no header, as many rows as stars in sample, and 3 columns as follows:
   1.Star-name(no-spaces)   2.V-band-magnitude   3.Photometric-colour-(e.g.B-V)
   (e.g., AGB00788   12.21	0.85
          AGB03590   12.40	0.85)
          
4. The line-lists (one for iron, another for all other elements) must have a two-row header (skipped by MOOG), and have 4 columns as follows:
   1.Wavelength(Angstroms)   2.Element(.0-for-neutral,.1-for-singly-ionized)   3.Excitation-potential(E.P.)   4.log(gf)
   (e.g., 4788.76   26.0   3.237   -1.763
          4794.36   26.0   2.424   -3.950)
          
5. All Phobos Python files must be in the same directory as the main Phobos file. This directory must be in your PATH environment variable.
   MOOG, ARES and makekurucz3 locations/executables must also be in the PATH environment variable.

--------------------------USAGE INSTRUCTIONS

1. MAIN (PHOBOS)
When Phobos is run, it will print all the user variables that have been defined. Please check that these are correct before continuing.
The analysis directory will be checked for the required fits directory and the photometry.txt file, and exit if they do not exist.
Stellar parameters will be estimated using the photometry.txt file, and saved to the file photo.params, which has 4 columns as follows:
   1.Star-name   2.Teff(K)   3.log(g)(cgs)   4.microturbulence(xi,km/s)
   This file will never change.
A copy is made of photo.params, called spectro.params. This file will be updated by the Parameter-Phobos routine, which determines stellar 
  parameters spectroscopically.
The user is asked which star they would like to analyse. This must an integer from 1 n, where n is the total number of stars in the sample. 
  The order of stars is as in photometry.txt (in the examples above, AGB00788 is star number 1). The parameters of this star are read from spectro.params.
The user is then asked which routine to run.
  'f' or 'p' initialise Parameter-Phobos.
  'e' initialises Elemental-Phobos.
  'm' will either create an atmospheric model based on spectro.params, or reset the parameters and model of the star to the initial
      photometric estimation (from photo.params).
  'del' will delete either: i) the iron abundance files and reset parameters to photometric, ii) the elemental abundance files, or iii) all
        abundance files and reset parameters to photometric.
  'PURGE' will reset the analysis folder back to the starting point, leaving only the /fits directory, photometry.txt, and any backup files created.

2. FE-PHOBOS
If Phobos has not been run for a star before, selecting 'f' or 'p' in MAIN will result in Phobos running once through ARES, makekurucz3,
  and MOOG, using photometric values and the iron line-list specified.
It is recommended to check the EWs (/moog_input) and line-to-line scatter (Fe I error) before continuing.
  ARES can be unreliable for spectra with low S/N, so I usually use ARES as an initial estimate of EWs, and manually remeasure many lines.
The ARES and MOOG output files (containing EW measurements and individual iron line abundances), photo.params, and spectro.params are opened
  with the user specified text editor, and a backup is created of the /moog_input file (star-name.fe.lines).

3. PARAMETER-PHOBOS
This is the heart of Phobos.
From the second time onwards that 'f' or 'p' are selected in MAIN, Phobos will systematically vary stellar parameters (Teff, log(g), xi), 
  over several interations, until: 
  i) there is no trend between individual iron line abundances (determined by MOOG) and E.P. (specified in the line-list),
  ii) there is no trend between individual iron line abundances (determined by MOOG) and reduced EW (EW/wavelength),
  iii) the average abundances of Fe I and Fe II are equal (to within 0.1 dex).
  This method is described in detail in Sousa (2014). Once the parameters have converged, they are saved to spectro.params.
ARES will not be run again unless the /moog_input file is deleted, in which case Fe-Phobos will intialise instead of Parameter-Phobos.

4. ELEMENTAL-PHOBOS
The first time 'e' is selected in MAIN, Phobos will run the star through ARES, makekurucz3, and MOOG, using the saved spectroscopic parameters (or photometric if Parameter-Phobos
  has not been used), and the elemental line-list specified.
From the second time 'e' is selected in MAIN, Elemental-Phobos will skip ARES, to allow for manual EW remeasurements.

5. USER-VARIABLES
Used in the set-up, to instruct Phobos as to the required directory paths, cluster parameters, etc. See INSTALLATION.

6. FUNCTIONS-PHOBOS
This file contains all sub-routines used throughout Phobos.

--------------------------ACKNOWLEDGEMENTS

Thank-you to Chris Sneden who wrote MOOG, Sérgio Sousa who wrote ARES, and the unknown author of makekurucz3.
Thank-you to my supervisors John Lattanzio, Simon Campbell, and Gayandhi De Silva.
Thank-you to my wife Grace MacLean-Rizkallah.
Thank-you to all the others that helped with bits and pieces of Phobos.
