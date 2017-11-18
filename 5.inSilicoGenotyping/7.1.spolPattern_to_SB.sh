#!/bin/bash
# mlasserre[at]pasteur[dot]edu[dot]uy
# help: conversion of known spoligotype patterns to SB numbers

if [ -z "$1" ]
then

echo "
Conversion of known spoligotype patterns to SB numbers

-----------------------------   HELP   -----------------------------
It uses:
- mbovis info

Usage: 7.1.spolPattern_to_SB.sh <input.file>

---------------------------------------------------------------------
input.file example:
<spoligotype binary pattern 1>
...
<spoligotype binary pattern N>
"

else

current=$(pwd)

echo "
Conversion...
"
### por cada linea de los patrones que quiero identificar
while read i
do
	iSB_found="false"
	linea=( $i )
	cepa=${linea[0]}
	patron=${linea[1]}

	## por cada patron conocido
	while read j
	do

	lineaSpol=( $j )
	jSBnumber=${lineaSpol[0]}
	jBinary=${lineaSpol[1]}
	
	if [ "$jBinary" == "$patron" ]
	then
		iSB_found=$jSBnumber
		echo $cepa ":" $iSB_found
	fi

	if [ "$iSB_found" != "false" ]
	then
		break
	fi

	done < "./SpoligotypePatterns.txt"
	
	if [ "$iSB_found" == "false" ]
	then
		echo $cepa ": Not found"
	fi

done < $1
cd $current


fi
