#!/bin/bash
# mlasserre@pasteur.edu.uy
# help: apply command fastq-dump --split-3 for a batch of files within folders

if [ -z "$1" ]
then

echo "
Apply command fastq-dump --split-3 for a batch of .sra files within folders, and 
compress the .sra file with tar and remove the original to save space

-----------------------------   HELP   -----------------------------

It uses:
- fastq-dump (from SRAtoolkit version 2.5.2)
- tar

Usage: fastqDump4Batches.sh configFile 
- paired/single - 'paired' for paired end library, 'single' for single end library

WARNING: Only one .sra file must exist inside each of the provided folders

Config file example:
<pathtofolder1_thatHas.sra_files> paired/single
<pathtofolder2_thatHas.sra_files> paired/single
..
<pathtofolderN_thatHas.sra_files> paired/single

---------------------------------------------------------------------
"

else

while read i;
do

linea=( $i )
camino=${linea[0]}
library=${linea[1]}
folder=$(basename $camino)

echo "Transforming $folder"

if [ ! -z $library ]
	then

	cd $camino

	filen=$(ls *.sra)

	if [ $library == "paired" ]
		then
		fastq-dump --split-3 $filen
		tar cvzf $filen.tar $filen
		rm $filen
	else 
		if [ $library == "single" ]
		then
			fastq-dump $filen
			tar cvzf $filen.tar $filen
			rm $filen
		else
			echo "ERROR in $folder: The library strategy provided was not 'paired' nor 'single'. "
		fi
	fi


else
	echo "You need to provide the libary design for each sra folder: paired or single" 

fi

done < $1

fi
