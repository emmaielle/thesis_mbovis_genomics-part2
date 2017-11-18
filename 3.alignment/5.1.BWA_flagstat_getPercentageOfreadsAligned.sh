#!/bin/bash
# mlasserre[at]pasteur[dot]edu[dot]uy
# help: automated BWA alignment for paired end reads & samtools coversion to bam

if [ -z "$1" ]
then

echo "
Flagstat and % of alignment.
Outputs a config.file of all the input strains followed by their alignment status
for the following steps.

Example output:

<pathtostrain1> <ALL/MAPPED>
...
<pathtostrainN> <ALL/MAPPED>

--------------- HELP ------------------
It uses: 
- Samtools, version 0.1.18 (r982:295)

Usage: bash <6.1.BWA_flagstat_getPercentageOfreadsAligned.sh> <config file>

Example: bash 6.1.BWA_flagstat_getPercentageOfreadsAligned.sh conf.folders

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
dat=$(date +%d%b%Y_%H.%M)
config=$(pwd)/conf.OutputFromAlignment.$dat
touch $config

while read i;
do

linea=( $i )
camino=${linea[0]}
folder=$(basename $camino)

echo "
$folder"
cd $folder/1.BWA.alineamiento

samtools flagstat alineamiento.$folder.sort.bam

cd ../2.samtoolsFilter
reads="$(samtools view -c ../1.BWA.alineamiento/alineamiento.$folder.sort.bam)"
readsFilt="$(samtools view -c onlymappedones.$folder.bam)"

echo -e "Número de reads totales: " $reads "\nNúmero de reads filtrados: " $readsFilt

if [ "$reads" -eq 0 ]
then
	echo -e 0
	echo "$folder Alineamiento < 80%"
        echo "$camino   MAPPED" >> $config
else

percent=$(($((readsFilt*100))/reads))
echo -e $percent"%"

if [ $percent -ge 80 ]
then
	echo "$folder Alineamiento > 80%"
	echo "$camino	ALL" >> $config
else
	echo "$folder Alineamiento < 80%"
	echo "$camino	MAPPED" >> $config
fi

fi

cd $current

done < $1

fi

fi
