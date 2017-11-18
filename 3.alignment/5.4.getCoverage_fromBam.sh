#!/bin/bash
# mlasserre[at]pasteur[dot]edu[dot]uy
# help: calculates the coverage of a standard bam file in a batch of strains for M. bovis

if [ -z "$1" ]
then

echo "
Calculates the coverage of a standard bam file in a batch of strains for M. bovis

-----------------------------   HELP   -----------------------------
It uses:
- Samtools

Usage: 06.4.getCoverage_fromBam.sh <config.file> <bam.prefix>

-bam.prefix : the prefix refers to the keyword of the bam file that precedes 
the name of each strain. It's required as to avoid confusion when more
than one bam file is present in the same folder.

WARNING:
- bam files are assumed to be in the folder 2.samtoolsFilter for each 
strain

---------------------------------------------------------------------
configFile example:
<path to reads for strain 1>
...
<path to reads for strain N>
"

else
if [ -z $2 ]
then 
	echo "You need to provide a prefix for the bam file"
else
current=$(pwd)

acc=$(pwd)/accepted.genomes_part2.txt
rej=$(pwd)/rejected.genomes_part2.txt
touch accepted.genomes_part2.txt
touch rejected.genomes_part2.txt


while read i
do

	linea=( $i )
	camino=${linea[0]}
	cepa=$(basename $camino)

	cd $camino/2.samtoolsFilter

	count=$(samtools view -c ${2}.${cepa}.bam)

	cat ${2}.${cepa}.fastq | awk '{if(NR%4==2) print length($1)}' | sort -n | uniq -c | sort -nk1 > read_length.txt
        readLen=$(tail -1 read_length.txt | awk '{print $2}')
	rm read_length.txt
        coverage=$((($count * $readLen) / 4345492))

	if [ $coverage -ge 30 ]
        then
	        echo "Cepa $cepa: ${coverage}x Accepted"
        	echo $cepa ${coverage}x >> $acc
        else
                echo "Cepa $cepa: ${coverage}x Rejected"
		echo $cepa ${coverage}x >> $rej
        fi

	cd ../..

done < $1

cd $current

fi

fi











