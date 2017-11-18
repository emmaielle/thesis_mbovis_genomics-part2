#!/bin/bash
# mlasserre[at]pasteur[dot]edu[dot]uy
# help: run SpoTyping for a batch of strains

if [ -z "$1" ]
then

echo "
Automated SpoTyping run for multiple strains
-----------------------------   HELP   -----------------------------
It uses:
- SpoTyping

Usage: bash 7.0.runSpotyping_batch.sh <config.file> <SpoTyping location folder>

Warning:
- Strain folder names can have up to 1 (one) dot ('.') character 

---------------------------------------------------------------------
configFile example:
<path to reads for strain 1>
...
<path to reads for strain N>
"

else
if [ -z $2 ]
then

echo "You need to provide the path where SpoTyping is located as a 2nd argument"

else
current=$(pwd)

while read i
do

linea=( $i )
camino=${linea[0]}
cepa=$(basename $camino)
cepa=$( echo $cepa | cut -f1 -d "." )

cd $camino

mkdir -p SpoTyping
cd SpoTyping

ln -s ../${cepa}_1.fastq
ln -s ../${cepa}_2.fastq

python $2 ${cepa}_1.fastq ${cepa}_2.fastq -o out.SpoTypingCATTED.txt

head out.SpoTypingCATTED.txt

done < $1

cd $current

fi

fi