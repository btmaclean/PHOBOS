#!/bin/bash

location=/Users/macleanb/data/m4/m4_members/analysis/

cd $location

namelist=($(awk '{print $1}' spectro.params))
array_elements=$((${#namelist[@]} - 1))
rm X_line_abundance_summaries/EWs_7771_O.txt
rm X_line_abundance_summaries/EWs_4730_Mg.txt
rm X_line_abundance_summaries/EWs_5711_Mg.txt
rm X_line_abundance_summaries/EWs_7691_Mg.txt

for ((i=0; i<=array_elements; i++)); do
	#echo -e "$(($i + 1))\ne" | phobos
    #grep '7771' X_line_abundance_summaries/${namelist[$i]}/O_lines.summary | echo $(awk '{print $2}') >> X_line_abundance_summaries/EWs_7771_O.txt
    grep '4730' X_line_abundance_summaries/${namelist[$i]}/Mg_lines.summary | echo $(awk '{print $2} {print $3}') >> X_line_abundance_summaries/EWs_4730_Mg.txt
	grep '5711' X_line_abundance_summaries/${namelist[$i]}/Mg_lines.summary | echo $(awk '{print $2} {print $3}') >> X_line_abundance_summaries/EWs_5711_Mg.txt
	grep '7691' X_line_abundance_summaries/${namelist[$i]}/Mg_lines.summary | echo $(awk '{print $2} {print $3}') >> X_line_abundance_summaries/EWs_7691_Mg.txt
done
