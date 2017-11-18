#!/bin/bash

if [ -z "$1" ]
then
 
echo "
Run coverage analysis for a batch of files
and find Regions of Difference

--------------- HELP ------------------
It uses: 
- parseRD.py
- bedtools genomecov v2.17.0

Usage: bash <14.RD_discovery.sh> <1:configFile.conf> <referencegenome.fasta>

WARNING: 
- Config w/ complete paths
- fastq files in the config must have extension .bam (aligned)
- Assumes a file structure formed by following the previous steps/scripts. In this case, this script will look for a '1.BWA.alineamiento/' folder inside the given path. 

configFile example:
<path_to_folder1>
<path_to_folder2>
...
<path_to_folderN>
"


else
if [ -z $2 ]
then 
	echo "You need to provide the reference genome as a 2nd argument"
else

current=$(pwd)

while read i
do

dir=( $i )
cepa=$(basename $dir)

echo "::::::::::::: Cepa $cepa :::::::::::::::::"

cd $dir
## asumo que el bam se encuentra en el directorio "1.BWA.alineamiento"

mkdir -p bedtools_RD
cd bedtools_RD

ln -s $dir/1.BWA.alineamiento/alineamiento.$cepa.bam
echo "Sorting bam..."
samtools sort alineamiento.$cepa.bam alineamiento.$cepa.sort
echo "Cov analysis running bedtools genomecov..."
bedtools genomecov -ibam  alineamiento.$cepa.sort.bam -g $2 -d > bedtools_genomeCov

python ./parseRD.py bedtools_genomeCov 100


done < $1

cd $current

fi

fi







