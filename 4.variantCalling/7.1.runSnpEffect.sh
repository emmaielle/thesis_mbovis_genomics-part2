#!/bin/bash
# mlasserre@pasteur.edu.uy
# help: run SNPeffect for batch strains

if [ -z "$1" ]
then
 
echo "
Runs snpEffect for a batch of strains of M. bovis

--------------- HELP ------------------
It uses: 
- snpEffect (version 4.2 (build 2015-12-05))

Usage: bash <7.1.runSnpEffect.sh> <1:configFile.conf> <snpEff location> <snpEff.config location>

WARNING: 
- Use complete paths 
- snpEff.config local is located in ~/Software/snpEff/snpEff.config. For external use, you need to set up snpEff.

configFile example:
<path_to_folder1>
<path_to_folder2>
...
<path_to_folderN>
"

else

current=$(pwd)

while read i;
do
	linea=( $i )

	path=${linea[0]}
	cd $path
	current2=$(pwd) ##
	cepa=$(basename $path)

	echo "

::::::::: Cepa $cepa :::::::::
"
	
	cd 5.SNPcalling/5.1.VarScan

	vcf=$(echo BOTH.IndelSNP.varScan.$cepa.output)

	cd ..
	mkdir -p 5.4.snpEffect
	cd 5.4.snpEffect

	cp -s ../5.1.VarScan/$vcf ./$vcf.vcf

	chrom=$(tail -1 $vcf.vcf | awk '{print $1}')
	sed "s/^$chrom/Chromosome/" $vcf.vcf > $vcf.sedded.vcf
	java -Xmx4g -jar $2 -ud 0 -v -d -c $3 -s stats.html GCA_000195835.1.29 $vcf.sedded.vcf > $cepa.snpEffect.vcf
	

done < $1

cd $current

fi









