#!/bin/bash
# mlasserre@pasteur.edu.uy
# help: automated BWA alignment for paired end reads & samtools coversion to bam

if [ -z "$1" ]
then
 
echo "
Automated BWA alignment & samtools conversion, filtering out potential human contaminated reads.
(Optimized version to handle size limits)

--------------- HELP ------------------
It uses: 
- BWA (bwa aln -l 15 -k 3 && bwa sampe). For BWA, version 0.7.12-r1039
- Samtools, version 0.1.18 (r982:295)

Usage: bash <pathtoBWA_samtools.sh> <1:configFile.conf> <2:pathtoReferenceToMapIn> <3:pathtoReferenceToMapOut_INDEX>

2 - The second parameter should be the path for the reference genome file if the genome hasn't been indexed, OR
the FOLDER for the previously indexed genome, to save from the process of indexing again. 
NOTE: for M bovis, this is in Tb73 strain, so the only option for you to have an index is if it's in Tb73

3 - Parameter 3 is a directory too, not the actual index file

WARNING: 
-Complete paths please
-fastq files must have extension .fastq (not .fq)
-fastqFolders must be named identical to the fastqFiles

configFile example:
<path_to_folder1>
<path_to_folder2>
...
<path_to_folderN>
"

else
if [ -z $3 ]
then 
	echo "Es necesario agregar el path del index del genoma de referencia humano para eliminar estos reads."
	exit
fi

if [ -z "$2" ]
then 
	echo "Es necesario agregar el path del genoma de referencia con el cual mapear."
	exit
else 
	if [ ! -d $2 -a ! -f $2 ]
	then
		echo "El 2do parametro debe ser un archivo o un directorio"
		exit
	
	else
	current=$(pwd)
	ite=0

	while read i;
	do
		linea=( $i )
		ite=$((ite + 1))

		## hay solo un item que necesito aca, pero por las dudas tomo el primero siempre
		path=${linea[0]}
		cd $path
		current2=$(pwd)
		cepa=$(basename $path)
		fastq1=$(echo $path/*_1.fastq)
		fastq2=$(echo $path/*_2.fastq)


#---------------------------------------- 1: BWA -----------------------------------------
# $1=configfile.conf $2=referenciaMapIn  

		echo "
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:::::::::::::::::::::::: Cepa $cepa :::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::"

## alineamiento contra $3

		mkdir -p 1.BWA.alineamiento
		cd 1.BWA.alineamiento
		pathIndex=$3
		echo $3
		echo "
-----------------------
[BWA]Mapeando reads contra referencia $(basename $3) ...
-----------------------"

		echo "[BWA]Alineando Reads 1..."
		bwa aln -l 15 -k 3 $pathIndex/HumanRef.Index $fastq1 > Human.$cepa.R1.sai
		echo "[BWA]Alineando Reads 2..."
		bwa aln -l 15 -k 3 $pathIndex/HumanRef.Index $fastq2 > Human.$cepa.R2.sai
		bwa sampe $pathIndex/HumanRef.Index Human.$cepa.R1.sai Human.$cepa.R2.sai $fastq1 $fastq2 > Human.alineamiento.$cepa.sam

		echo "-----------------------
[BWA]Alineamiento culminado.
-----------------------
"

#---------------------------------------- 2: Samtools -----------------------------------------

		echo "-----------------------
[Samtools]Creando archivo bam...        
-----------------------"

#terminar de indentar...!!! :(

samtools view -bS Human.alineamiento.$cepa.sam > Human.alineamiento.$cepa.bam
samtools sort -n Human.alineamiento.$cepa.bam Human.alineamiento.$cepa.sort
samtools index Human.alineamiento.$cepa.sort.bam
samtools flagstat Human.alineamiento.$cepa.sort.bam

cd ..

echo "
-----------------------
[Samtools]Guardando reads que NO mapearon a referencia humano...
-----------------------"
mkdir -p 2.samtoolsFilter
cd 2.samtoolsFilter
### cambio de 4 a 12
samtools view -bh -f 12 ../1.BWA.alineamiento/Human.alineamiento.$cepa.sort.bam > NONmappedonesToHuman.$cepa.bam
readsFilt="$(samtools view -c NONmappedonesToHuman.$cepa.bam)"
######## verifico que me haya filtrado bien. Si filtró mal, me salgo del script #######
echo $readsFilt

echo "
-----------------------
[Bedtools]Transformando bam no mapeados a fastq...
-----------------------
"

bamToFastq -i NONmappedonesToHuman.$cepa.bam -fq NONmappedonesToHuman.${cepa}_1.fastq -fq2 NONmappedonesToHuman.${cepa}_2.fastq 

## guardo los nuevos fastq resultantes
nameFQ1=$(echo $(ls *_1.fastq))
nameFQ2=$(echo $(ls *_2.fastq))

#fastq1=$(echo $(pwd)/$nameFQ1)
#fastq2=$(echo $(pwd)/$nameFQ2)

current2=$(pwd)

cd ../1.BWA.alineamiento

if [ $ite -eq 1 ]
then 

echo "
-----------------------
[BWA]Generando índice de genoma referencia $(basename $2) ...
-----------------------"

# if $2 is a file
if [ -d $2 ]
then
	pathIndexBovis=$2
	echo $pathIndexBovis

#si el archivo es el genoma mismo, calculo el index
elif [ -f $2 ]
then
	pathIndexBovis=$(pwd)
	echo $pathIndexBovis
	bwa index -p Bovis.Index $2

else 
	echo "Your second parameter isn't neither a file nor a directory path"
	exit
fi

fi

echo "
-----------------------
[BWA]Mapeando reads a genoma de referencia $(basename $2)...
-----------------------"
echo "
[BWA]Alineando Reads 1..."
bwa aln -l 15 -k 3 $pathIndexBovis/Bovis.Tb73.Index ../2.samtoolsFilter/$nameFQ1 > $cepa.R1.sai
echo "[BWA]Alineando Reads 2..."
bwa aln -l 15 -k 3 $pathIndexBovis/Bovis.Tb73.Index ../2.samtoolsFilter/$nameFQ2 > $cepa.R2.sai 
bwa sampe $pathIndexBovis/Bovis.Tb73.Index $cepa.R1.sai $cepa.R2.sai ../2.samtoolsFilter/$nameFQ1 ../2.samtoolsFilter/$nameFQ2 > alineamiento.$cepa.sam

echo "-----------------------
[BWA]Alineamiento contra $(basename $2) culminado.
-----------------------
"

#---------------------------------------- 2: Samtools -----------------------------------------

echo "-----------------------
[Samtools]Creando archivo bam...	
-----------------------"
samtools view -bS alineamiento.$cepa.sam > alineamiento.$cepa.bam
samtools sort -n alineamiento.$cepa.bam alineamiento.$cepa.sortN
samtools sort alineamiento.$cepa.bam alineamiento.$cepa.sort
samtools index alineamiento.$cepa.sort.bam
samtools flagstat alineamiento.$cepa.sort.bam

# 7249440 + 0 in total (QC-passed reads + QC-failed reads)
# 0 + 0 duplicates
# 4843901 + 0 mapped (66.82%:-nan%)
# 7249440 + 0 paired in sequencing
# 3624720 + 0 read1
# 3624720 + 0 read2
# 4371752 + 0 properly paired (60.30%:-nan%)
# 4780668 + 0 with itself and mate mapped
# 63233 + 0 singletons (0.87%:-nan%)
# 0 + 0 with mate mapped to a different chr
# 0 + 0 with mate mapped to a different chr (mapQ>=5)


## EXTRAER DEL BAM DE BWA LAS SECUENCIAS QUE SOLO ALINEARON DE A PARES EN EL GENOMA DE REFERENCIA

echo "
-----------------------
[Samtools]Guardando reads que mapearon a referencia...
-----------------------"
mkdir -p ../2.samtoolsFilter
cd ../2.samtoolsFilter

reads="$(samtools view -c ../1.BWA.alineamiento/alineamiento.$cepa.sort.bam)"
samtools view -bh -F 12 ../1.BWA.alineamiento/alineamiento.$cepa.sort.bam > onlymappedones.$cepa.bam

readsFilt="$(samtools view -c onlymappedones.$cepa.bam)"

echo -e "Número de reads totales: " $reads "\nNúmero de reads filtrados: " $readsFilt
echo -e "$readsFilt / $reads" | bc -l

## BAM TO FASTQ
# voy a hacer bam to fastq porque velvet pide fastq (tambien acepta fasta, pero por las dudas) Y el SPADES también

echo "
-----------------------
[Bedtools]Transformando bam a fastq...
-----------------------
"

bamToFastq -i onlymappedones.$cepa.bam -fq onlymappedones.$cepa.fastq


echo "
-----------------------
1.BWA.Alineamiento: Comprimiendo sam y sai que no se van a utilizar...
-----------------------
"
cd ../1.BWA.alineamiento

tar cvzf alineamientos.sam.tar *.sam *.sai
rm *.sam 
rm *.sai

cd ../..

echo "
----------------------- Cepa $cepa finalizada ----------------------- 
"

done < $1

cd $current


fi
fi

fi
