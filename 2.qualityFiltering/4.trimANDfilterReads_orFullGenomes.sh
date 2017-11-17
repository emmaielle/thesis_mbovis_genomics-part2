#!/bin/bash
# mlasserre@pasteur.edu.uy
# help: Trims and filters reads with overall quality score < 20 and from the remaining reads, calculates the
# coverage. If it is lower than 30x, it rejects the whole sequencing project.

if [ -z "$1" ]
then
 
echo "
Trims and filters reads with overall quality score below <qs> and, from the remaining reads, calculates the 
coverage. If it is lower than <cov>, it rejects the whole sequencing project.
It works for all the selected folders inside the current directory.

--------------- HELP ------------------
It uses:
- NGSQCToolkit

Usage: bash <filterReads_orFullGenomes.sh> qs cov folder1 [folder2 .. folderN]
Example: bash filterReads_orFullGenomes.sh 20 30 *

qs - quality score threshold (int)
cov - coverage threshold (int)

Output:

- accepted.genomes.txt
- rejected.genomes.txt

WARNING: 
-if you're using the * wildcard, make sure you ONLY have folders in it, no loose files
-fastq files must have extension .fastq (not .fq)
"

else
if [ -z "$2" ] && [ -z "$3" ] && [ -z "$4" ]
then
	echo "You have to provide all 3+ parameters. Usage: bash <filterReads_orFullGenomes.sh> qs cov folder1 [folder2 .. folderN]"
 
else
	qs=$1
	cov=$2
	shift 
	shift
	
	acc=$(pwd)/accepted.genomes.txt
	rej=$(pwd)/rejected.genomes.txt
	touch accepted.genomes.txt
	touch rejected.genomes.txt
	
	contador=1
	for i in $@
	do	
		cd $i
		
		echo "$contador - ::::::::: $i :::::::::::"
		fastq1=$(ls *_1.fastq)
		fastq2=$(ls *_2.fastq)
		name=$(echo $fastq1 | cut -d "_" -f1)
		if [ ! -z $fastq1 ] && [ ! -z $fastq2 ] 
		then
			perl ~/Software/NGSQCToolkit_v2.3.3/Trimming/TrimmingReads.pl -i $fastq1 -irev $fastq2 -q $qs
			perl ~/Software/NGSQCToolkit_v2.3.3/QC/IlluQC.pl -pe ${fastq1}_trimmed ${fastq2}_trimmed N A -s $qs -p 6			
			cd IlluQC_Filtered_files
			cat ${name}_1.fastq_trimmed_filtered | awk '{if(NR%4==2) print length($1)}' | sort -n | uniq -c | sort -nk1 > read_length.txt
			readLen=$(awk -v N=2 '{ sum += $N } END { if (NR > 0) print sum / NR }' read_length.txt )
			readLen=$( printf '%.*f\n' 0 $readLen)
			lines=$(wc -l ${name}_1.fastq_trimmed_filtered |cut -d " " -f 1)
			count=$(($lines / 2)) # esto es / 4 primero por el formato del fastq, pero despues es * 2 porque estan los dos pares de archivos
			coverage=$((($count * $readLen) / 4345492))
			echo "Coverage of ${coverage}x"
			echo "Read length (average): $readLen"
			echo "Number of reads: $count"	
			if [ $coverage -ge $cov ]
			then
				echo "Accepted"
				echo $name $coverage >> $acc
			else
				echo "Rejected"
				echo $name $coverage >> $rej
			fi

			cd ..
		fi
		cd ..
		echo "::::::::: $i finalizada ::::::::::"
		contador=$((contador +1))
	done
	echo "

	Se han creado los archivos $acc y $rej satisfactoriamente."

fi

fi




