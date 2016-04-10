#-- CREATE PHOTOMETRIC MODEL --
#-- Clear variables
unset star
unset arrayelement
unset name
unset Teff
unset logg
unset xi
unset linelist_fe
unset linelist_elements
unset location
unset texteditor

source user_variables.sh
 
#-- Ask user which star to use (ie. 1-50).
echo "Please specify which number star you would like to create a model for (i.e. 1 to n, where n is the total number of stars)."
read star

#Coz bash arrays are stupid and start at zero.
arrayelement=$(($star - 1))
#--------CASTELLI--------------------------------

#Create MOOG friendly atmospheric models for each star, with a terminal summary at the end.

#Go to appropriate directory.
cd $location

#Set the variable 'name, etc' as an array with n lines, each with the name/parameter of a single star.
name=($(awk '{print $1}' photo.params))
Teff=($(awk '{print $2}' photo.params))
logg=($(awk '{print $3}' photo.params))
xi=($(awk '{print $4}' photo.params))
loggneg=-0.5

if [ -d "models/" ]; then
  cd models/
else echo "Input model files required!"
	exit
fi

#Clean directory.
rm ${name[$arrayelement]}.model.dat
rm *.fail

#-- Depending on the parameters Teff and logg, a model is created with Castelli using an input grid that covers the parameters.
if [[ ${Teff[$arrayelement]} -ge 3500 && ${Teff[$arrayelement]} -le 4000 && (( $(bc <<< "${logg[$arrayelement]} >= 0.0") == 1 && $(bc <<< "${logg[$arrayelement]} <= 1.0") == 1 ))]]; then
	echo "Start ${name[$arrayelement]} model creation"
	echo -e "m-10/35k40,00g10.in\n${Teff[$arrayelement]},${logg[$arrayelement]}\n${name[$arrayelement]}a.model.dat" | castelli
	elif [[ ${Teff[$arrayelement]} -ge 3500 && ${Teff[$arrayelement]} -le 4000 && (( $(bc <<< "${logg[$arrayelement]} >= 1.0") == 1 && $(bc <<< "${logg[$arrayelement]} <= 2.0") == 1 ))]]; then
		echo "Start ${name[$arrayelement]} model creation"
		echo -e "m-10/35k40,10g20.in\n${Teff[$arrayelement]},${logg[$arrayelement]}\n${name[$arrayelement]}a.model.dat" | castelli
		
		elif [[ ${Teff[$arrayelement]} -ge 4000 && ${Teff[$arrayelement]} -le 4500 && (( $(bc <<< "${logg[$arrayelement]} >= 0.0") == 1 && $(bc <<< "${logg[$arrayelement]} <= 1.0") == 1 ))]]; then
			echo "Start ${name[$arrayelement]} model creation"
			echo -e "m-10/40k45,00g10.in\n${Teff[$arrayelement]},${logg[$arrayelement]}\n${name[$arrayelement]}a.model.dat" | castelli
			elif [[ ${Teff[$arrayelement]} -ge 4000 && ${Teff[$arrayelement]} -le 4500 && (( $(bc <<< "${logg[$arrayelement]} >= 1.0") == 1 && $(bc <<< "${logg[$arrayelement]} <= 2.0") == 1 ))]]; then
				echo "Start ${name[$arrayelement]} model creation"
				echo -e "m-10/40k45,10g20.in\n${Teff[$arrayelement]},${logg[$arrayelement]}\n${name[$arrayelement]}a.model.dat" | castelli
				elif [[ ${Teff[$arrayelement]} -ge 4000 && ${Teff[$arrayelement]} -le 4500 && (( $(bc <<< "${logg[$arrayelement]} >= 2.0") == 1 && $(bc <<< "${logg[$arrayelement]} <= 3.0") == 1 ))]]; then
					echo "Start ${name[$arrayelement]} model creation"
					echo -e "m-10/40k45,20g30.in\n${Teff[$arrayelement]},${logg[$arrayelement]}\n${name[$arrayelement]}a.model.dat" | castelli
					
					elif [[ ${Teff[$arrayelement]} -ge 4500 && ${Teff[$arrayelement]} -le 5000 && (( $(bc <<< "${logg[$arrayelement]} >= 1.0") == 1 && $(bc <<< "${logg[$arrayelement]} <= 2.0") == 1 ))]]; then
						echo "Start ${name[$arrayelement]} model creation"
						echo -e "m-10/45k50,10g20.in\n${Teff[$arrayelement]},${logg[$arrayelement]}\n${name[$arrayelement]}a.model.dat" | castelli
						elif [[ ${Teff[$arrayelement]} -ge 4500 && ${Teff[$arrayelement]} -le 5000 && (( $(bc <<< "${logg[$arrayelement]} >= 2.0") == 1 && $(bc <<< "${logg[$arrayelement]} <= 3.0") == 1 ))]]; then
							echo "Start ${name[$arrayelement]} model creation"
							echo -e "m-10/45k50,20g30.in\n${Teff[$arrayelement]},${logg[$arrayelement]}\n${name[$arrayelement]}a.model.dat" | castelli
							elif [[ ${Teff[$arrayelement]} -ge 4500 && ${Teff[$arrayelement]} -le 5000 && (( $(bc <<< "${logg[$arrayelement]} >= 3.0") == 1 && $(bc <<< "${logg[$arrayelement]} <= 4.0") == 1 ))]]; then
								echo "Start ${name[$arrayelement]} model creation"
								echo -e "m-10/45k50,30g40.in\n${Teff[$arrayelement]},${logg[$arrayelement]}\n${name[$arrayelement]}a.model.dat" | castelli
								
							elif [[ ${Teff[$arrayelement]} -ge 5000 && ${Teff[$arrayelement]} -le 5500 && (( $(bc <<< "${logg[$arrayelement]} >= 0.0") == 1 && $(bc <<< "${logg[$arrayelement]} <= 1.0") == 1 ))]]; then
								echo "Start ${name[$arrayelement]} model creation"
								echo -e "m-10/50k55,00g10.in\n${Teff[$arrayelement]},${logg[$arrayelement]}\n${name[$arrayelement]}a.model.dat" | castelli
								elif [[ ${Teff[$arrayelement]} -ge 5000 && ${Teff[$arrayelement]} -le 5500 && (( $(bc <<< "${logg[$arrayelement]} >= 1.0") == 1 && $(bc <<< "${logg[$arrayelement]} <= 2.0") == 1 ))]]; then
									echo "Start ${name[$arrayelement]} model creation"
									echo -e "m-10/50k55,10g20.in\n${Teff[$arrayelement]},${logg[$arrayelement]}\n${name[$arrayelement]}a.model.dat" | castelli
									elif [[ ${Teff[$arrayelement]} -ge 5000 && ${Teff[$arrayelement]} -le 5500 && (( $(bc <<< "${logg[$arrayelement]} >= 2.0") == 1 && $(bc <<< "${logg[$arrayelement]} <= 3.0") == 1 ))]]; then
										echo "Start ${name[$arrayelement]} model creation"
										echo -e "m-10/50k55,20g30.in\n${Teff[$arrayelement]},${logg[$arrayelement]}\n${name[$arrayelement]}a.model.dat" | castelli
										elif [[ ${Teff[$arrayelement]} -ge 5000 && ${Teff[$arrayelement]} -le 5500 && (( $(bc <<< "${logg[$arrayelement]} >= 3.0") == 1 && $(bc <<< "${logg[$arrayelement]} <= 4.0") == 1 ))]]; then
											echo "Start ${name[$arrayelement]} model creation"
											echo -e "m-10/50k55,30g40.in\n${Teff[$arrayelement]},${logg[$arrayelement]}\n${name[$arrayelement]}a.model.dat" | castelli
										elif [[ ${Teff[$arrayelement]} -ge 5000 && ${Teff[$arrayelement]} -le 5500 && (( $(bc <<< "${logg[$arrayelement]} >= 4.0") == 1 && $(bc <<< "${logg[$arrayelement]} <= 5.0") == 1 ))]]; then
											echo "Start ${name[$arrayelement]} model creation"
											echo -e "m-10/50k55,40g50.in\n${Teff[$arrayelement]},${logg[$arrayelement]}\n${name[$arrayelement]}a.model.dat" | castelli
											
										elif [[ ${Teff[$arrayelement]} -ge 5500 && ${Teff[$arrayelement]} -le 6000 && (( $(bc <<< "${logg[$arrayelement]} >= 0.0") == 1 && $(bc <<< "${logg[$arrayelement]} <= 1.0") == 1 ))]]; then
											echo "Start ${name[$arrayelement]} model creation"
											echo -e "m-10/55k60,00g10.in\n${Teff[$arrayelement]},${logg[$arrayelement]}\n${name[$arrayelement]}a.model.dat" | castelli
										elif [[ ${Teff[$arrayelement]} -ge 5500 && ${Teff[$arrayelement]} -le 6000 && (( $(bc <<< "${logg[$arrayelement]} >= 1.0") == 1 && $(bc <<< "${logg[$arrayelement]} <= 2.0") == 1 ))]]; then
											echo "Start ${name[$arrayelement]} model creation"
											echo -e "m-10/55k60,10g20.in\n${Teff[$arrayelement]},${logg[$arrayelement]}\n${name[$arrayelement]}a.model.dat" | castelli
											elif [[ ${Teff[$arrayelement]} -ge 5500 && ${Teff[$arrayelement]} -le 6000 && (( $(bc <<< "${logg[$arrayelement]} >= 2.0") == 1 && $(bc <<< "${logg[$arrayelement]} <= 3.0") == 1 ))]]; then
												echo "Start ${name[$arrayelement]} model creation"
												echo -e "m-10/55k60,20g30.in\n${Teff[$arrayelement]},${logg[$arrayelement]}\n${name[$arrayelement]}a.model.dat" | castelli
												elif [[ ${Teff[$arrayelement]} -ge 5500 && ${Teff[$arrayelement]} -le 6000 && (( $(bc <<< "${logg[$arrayelement]} >= 3.0") == 1 && $(bc <<< "${logg[$arrayelement]} <= 4.0") == 1 ))]]; then
													echo "Start ${name[$arrayelement]} model creation"
													echo -e "m-10/55k60,30g40.in\n${Teff[$arrayelement]},${logg[$arrayelement]}\n${name[$arrayelement]}a.model.dat" | castelli
												elif [[ ${Teff[$arrayelement]} -ge 5500 && ${Teff[$arrayelement]} -le 6000 && (( $(bc <<< "${logg[$arrayelement]} >= 4.0") == 1 && $(bc <<< "${logg[$arrayelement]} <= 5.0") == 1 ))]]; then
													echo "Start ${name[$arrayelement]} model creation"
													echo -e "m-10/55k60,40g50.in\n${Teff[$arrayelement]},${logg[$arrayelement]}\n${name[$arrayelement]}a.model.dat" | castelli
													
												elif [[ ${Teff[$arrayelement]} -ge 6000 && ${Teff[$arrayelement]} -le 6500 && (( $(bc <<< "${logg[$arrayelement]} >= 1.0") == 1 && $(bc <<< "${logg[$arrayelement]} <= 2.0") == 1 ))]]; then
													echo "Start ${name[$arrayelement]} model creation"
													echo -e "m-10/60k65,10g20.in\n${Teff[$arrayelement]},${logg[$arrayelement]}\n${name[$arrayelement]}a.model.dat" | castelli
													elif [[ ${Teff[$arrayelement]} -ge 6000 && ${Teff[$arrayelement]} -le 6500 && (( $(bc <<< "${logg[$arrayelement]} >= 2.0") == 1 && $(bc <<< "${logg[$arrayelement]} <= 3.0") == 1 ))]]; then
														echo "Start ${name[$arrayelement]} model creation"
														echo -e "m-10/60k65,20g30.in\n${Teff[$arrayelement]},${logg[$arrayelement]}\n${name[$arrayelement]}a.model.dat" | castelli
														elif [[ ${Teff[$arrayelement]} -ge 6000 && ${Teff[$arrayelement]} -le 6500 && (( $(bc <<< "${logg[$arrayelement]} >= 3.0") == 1 && $(bc <<< "${logg[$arrayelement]} <= 4.0") == 1 ))]]; then
															echo "Start ${name[$arrayelement]} model creation"
															echo -e "m-10/60k65,30g40.in\n${Teff[$arrayelement]},${logg[$arrayelement]}\n${name[$arrayelement]}a.model.dat" | castelli
														elif [[ ${Teff[$arrayelement]} -ge 6000 && ${Teff[$arrayelement]} -le 6500 && (( $(bc <<< "${logg[$arrayelement]} >= 4.0") == 1 && $(bc <<< "${logg[$arrayelement]} <= 5.0") == 1 ))]]; then
															echo "Start ${name[$arrayelement]} model creation"
															echo -e "m-10/60k65,40g50.in\n${Teff[$arrayelement]},${logg[$arrayelement]}\n${name[$arrayelement]}a.model.dat" | castelli
															
														elif [[ ${Teff[$arrayelement]} -ge 6500 && ${Teff[$arrayelement]} -le 7000 && (( $(bc <<< "${logg[$arrayelement]} >= 2.0") == 1 && $(bc <<< "${logg[$arrayelement]} <= 3.0") == 1 ))]]; then
															echo "Start ${name[$arrayelement]} model creation"
															echo -e "m-10/65k70,20g30.in\n${Teff[$arrayelement]},${logg[$arrayelement]}\n${name[$arrayelement]}a.model.dat" | castelli
														elif [[ ${Teff[$arrayelement]} -ge 6500 && ${Teff[$arrayelement]} -le 7000 && (( $(bc <<< "${logg[$arrayelement]} >= 3.0") == 1 && $(bc <<< "${logg[$arrayelement]} <= 4.0") == 1 ))]]; then
															echo "Start ${name[$arrayelement]} model creation"
															echo -e "m-10/65k70,30g40.in\n${Teff[$arrayelement]},${logg[$arrayelement]}\n${name[$arrayelement]}a.model.dat" | castelli
														elif [[ ${Teff[$arrayelement]} -ge 6500 && ${Teff[$arrayelement]} -le 7000 && (( $(bc <<< "${logg[$arrayelement]} >= 4.0") == 1 && $(bc <<< "${logg[$arrayelement]} <= 5.0") == 1 ))]]; then
															echo "Start ${name[$arrayelement]} model creation"
															echo -e "m-10/65k70,40g50.in\n${Teff[$arrayelement]},${logg[$arrayelement]}\n${name[$arrayelement]}a.model.dat" | castelli
															
															elif [[ ${Teff[$arrayelement]} -ge 7000 && ${Teff[$arrayelement]} -le 7500 && (( $(bc <<< "${logg[$arrayelement]} >= 2.0") == 1 && $(bc <<< "${logg[$arrayelement]} <= 3.0") == 1 ))]]; then
																echo "Start ${name[$arrayelement]} model creation"
																echo -e "m-10/70k75,20g30.in\n${Teff[$arrayelement]},${logg[$arrayelement]}\n${name[$arrayelement]}a.model.dat" | castelli
															elif [[ ${Teff[$arrayelement]} -ge 7000 && ${Teff[$arrayelement]} -le 7500 && (( $(bc <<< "${logg[$arrayelement]} >= 3.0") == 1 && $(bc <<< "${logg[$arrayelement]} <= 4.0") == 1 ))]]; then
																echo "Start ${name[$arrayelement]} model creation"
																echo -e "m-10/70k75,30g40.in\n${Teff[$arrayelement]},${logg[$arrayelement]}\n${name[$arrayelement]}a.model.dat" | castelli	
															elif [[ ${Teff[$arrayelement]} -ge 7000 && ${Teff[$arrayelement]} -le 7500 && (( $(bc <<< "${logg[$arrayelement]} >= 4.0") == 1 && $(bc <<< "${logg[$arrayelement]} <= 5.0") == 1 ))]]; then
																echo "Start ${name[$arrayelement]} model creation"
																echo -e "m-10/70k75,40g50.in\n${Teff[$arrayelement]},${logg[$arrayelement]}\n${name[$arrayelement]}a.model.dat" | castelli		
																
														else
															echo "${name[$arrayelement]} failed model creation" > ${name[$arrayelement]}.fail
															exit
														fi

#Creates a MOOG model input file from the standard Castelli output.
echo "KURUCZ
TEFF  ${Teff[$arrayelement]} GRAVITY ${logg[$arrayelement]}
NTAU      72" > ${name[$arrayelement]}.model.dat
atmos=$(sed '24,95!d' ${name[$arrayelement]}a.model.dat)
echo "${atmos[*]}" >> ${name[$arrayelement]}.model.dat
echo "   ${xi[$arrayelement]}
NATOMS    1    0
26 6.5
NMOL      1
          106" >> ${name[$arrayelement]}.model.dat
		  
		  sed -i -e "s/2.000E+05/      NaN/g" ${name[$arrayelement]}.model.dat


#Removes temporary files.
rm *a.model.dat
rm *.model.dat-e
