# mlasserre[at]pasteur[dot]edu[dot]uy
# help: Count reads from any bam file. Works for batches

if [ -z "$1" ]
then

echo "
Count reads from any bam file. Works for batches

-----------------------------   HELP   -----------------------------
It uses:
- Samtools

Usage: 06.3.countReadsFromBAM.sh <config.file> 

---------------------------------------------------------------------
configFile example:
<pathTostrainFolder1>
...
<pathTostrainFolderN>
"

else

current=$(pwd)
echo "Reads mapeados a M. bovis"

while read i
do

linea=( $i )
camino=${linea[0]}
cepa=$(basename $camino)

cd $camino/2.samtoolsFilter

reads=$(samtools view -c onlymappedones.$cepa.bam)

echo "Cepa $cepa - $reads reads"

done < $1

cd $current

fi

