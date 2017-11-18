#!/bin/bash
# mlasserre[at]pasteur[dot]edu[dot]uy
# help: automated BWA alignment for paired end reads & samtools coversion to bam

if [ -z "$1" ]
then

echo "
Flagstat and % of alignment 

--------------- HELP ------------------
It uses: 
- Samtools, version 0.1.18 (r982:295)

Usage: bash <6.2.BWA_flagstat_getPercentageOfHUMANreadsAligned.sh> <configfile>

Example: bash 6.2.BWA_flagstat_getPercentageOfreadsAligned.sh conf.folders

Config example:
<pathtofolder1>
<pathtofolder2>
..
<pathtofolderN>
"

else
if [ -z $1 ]
then
echo "You must provide at least one folder"
else

current=$(pwd)

while read i;
do

linea=( $i )
camino=${linea[0]}
folder=$(basename $camino)

echo "
$folder"
cd $folder/1.BWA.alineamiento

samtools flagstat Human.alineamiento.$folder.sort.bam

cd $current

done < $1

fi

fi
