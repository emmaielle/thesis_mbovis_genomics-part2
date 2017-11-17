## mlasserre@pasteur.edu.uy

if [ -z "$1" ]
then

echo "
Merge vcfs from multiple independent files into one with many samples
from ALL the vcfs in the directory. Careful

---------------------------------

Usage: bash <%prog%> <outputFile.vcf> <GATK location> <pathToReference>

- outputFile.vcf: Name desired for the output file  
"

else
if [ -z $2 ]
then

echo "You need to provide the path where GATK is located as a 2nd argument"

else
if [ -z $3 ]
then

echo "You need to provide the path reference genome (.fasta) is located as a 3rd argument"

else
current=$(pwd)

vars=""

for i in $(pwd)/* 
do 
	type=$( echo $i | cut -d "." -f2 )
	if [ "$type" == "vcf" ]
	then
		vars=$vars" -V $i"
	fi
done

#para cada item en el directorio, que tiene que estar previamente vacio
echo "$vars"
rm *.idx
java -jar $2 -R $3 -T CombineVariants $vars -o $1 -genotypeMergeOptions UNIQUIFY

cd $current


fi
