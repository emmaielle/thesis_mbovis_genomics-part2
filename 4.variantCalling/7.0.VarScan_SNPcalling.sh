#!/bin/bash
# mlasserre@pasteur.edu.uy
# help: automatically run batch files for SNP calling with GATK and VarScan

if [ -z "$1" ]
then
 
echo "
Automated SNP calling for multiple sequencing projects using VarScan
1 sample per strain (indel + SNP together)
(Optimized version for compression of resulting files)

-----------------------------   HELP   -----------------------------
It uses:
- VarScan (v2.3.7)
- bgzip
- GATK (v3.5)

Usage: VarScan_SNPcalling_OPTIMIZE.SIZES.sh <config.file> <pathToReferenceGenome> <varScan location> <GATK location>

PRECONDITION:
The reference genome is assumed to have been indexed previously and located in ./00.IndexReferenceGenome
---------------------------------------------------------------------
configFile example:
<path to root for strain 1> 
...
<path to root for strain N> 
"

else

if [ -z $2 ]
then

echo "You need to provide the path for a reference genome as a 2nd argument"

else
if [ -z $3 ]
then

echo "You need to provide the path where VarScan is located as a 3rd argument"

else
if [ -z $4 ]
then

echo "You need to provide the path where GATK is located as a 4th argument"

else
#~/Software/_viejos/VarScan.v2.3.7.jar
current=$(pwd)

echo "
[Samtools] Index reference genome for first use...
"
## ya tenia el indice de antes
mkdir -p 00.IndexReferenceGenome
cd 00.IndexReferenceGenome
refGen=$(pwd)

ln -fs $2
refname=$(basename $2)
#bwa index -a is $refname
#samtools faidx $refname

cd $current

while read i
do

linea=( $i )
camino=${linea[0]}
cepa=$(basename $camino)

opcion=${linea[1]}

cd $camino
mkdir -p 5.SNPcalling
##rm -r 5.SNPcalling/5.1.VarScan0_2-1sample
mkdir -p 5.SNPcalling/5.1.VarScan
cd 5.SNPcalling/5.1.VarScan

echo "
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:::::::::::::::::::::::: Cepa $cepa :::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

### (A) run mpileup (Samtools)
"
# - Align reference genome with my strain (ya tengo alineados del paso 1.BWA.alineamiento)

ln -s ../../1.BWA.alineamiento/alineamiento.$cepa.sort.bam
#samtools sort ../../1.BWA.alineamiento/alineamiento.$cepa.sort.bam ./alineamiento.$cepa.sort


# *.fai capaz que está mal
samtools mpileup -f $refGen/$refname alineamiento.*.sort.bam > output.$cepa.vcf

echo "
### (B) run VarScan. Basic filtering.	

[VarScan] SNP calling... "

echo "$cepa" > sampleName.txt
java -jar $3 mpileup2snp output.$cepa.vcf --min-reads2 20 --vcf-sample-list sampleName.txt --min-var-freq 0.2 --output-vcf 1 > SNP.varScan.$cepa.output

#Output example:
#Only SNPs will be reported
#Warning: No p-value threshold provided, so p-values will not be calculated
#Min coverage:	8
#Min reads2:	20
#Min var freq:	0.35
#Min avg qual:	15
#P-value thresh:	0.01
#Reading input from output.vcf
#4328664 bases in pileup file
#595 variant positions (556 SNP, 39 indel)
#2 were failed by the strand-filter
#555 variant positions reported (555 SNP, 0 indel)

echo "[VarScan] INDEL calling..."

java -jar $3 mpileup2indel output.$cepa.vcf --min-reads2 20 --vcf-sample-list sampleName.txt --min-var-freq 0.2 --output-vcf 1 > INDEL.varScan.$cepa.output

echo "[bgzip] Merging variants in one file..."
## Uno los archivos de VarScan (INDEL + SNPs) en un solo archivo:

bgzip -c SNP.varScan.$cepa.output > SNP.varScan.$cepa.output.gz
bgzip -c INDEL.varScan.$cepa.output > INDEL.varScan.$cepa.output.gz
bcftools index -f SNP.varScan.$cepa.output.gz
bcftools index -f INDEL.varScan.$cepa.output.gz
java -jar $4 -T CombineVariants -R ~/Maestría/GenomasReferenciaMTC/REFERENCIA/versiones_Anteriores_a_8-Jul-16/NC_002945.fasta --variant:snp SNP.varScan.$cepa.output --variant:indel INDEL.varScan.$cepa.output -o BOTH.IndelSNP.varScan.$cepa.output --assumeIdenticalSamples
#bcftools merge --force-samples INDEL.varScan.$cepa.output.gz SNP.varScan.$cepa.output.gz -o BOTH.IndelSNP.varScan.$cepa.output
bgzip -c BOTH.IndelSNP.varScan.$cepa.output > BOTH.IndelSNP.varScan.$cepa.output.gz

#compressss
tar cvzf output.$cepa.tar output.$cepa.vcf
rm output.$cepa.vcf

echo "
Cepa $cepa finalizada!!"


done < $1

cd $current 

fi

fi



