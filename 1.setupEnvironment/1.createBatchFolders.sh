#!/bin/bash
# mlasserre@pasteur.edu.uy
# help: Create multiple folders from a config file specifying their names and copies files with the same name to their respective folders.

if [ -z "$1" ]
then

echo "
Create multiple folders from a config file specifying their names and copies files with the same name to their respective folders. 
It will move or copy the files, according to what the user specify, so they must be removed from the original path if desired.
If no 2nd argument is provided, then the script won't work.

-----------------------------   HELP   -----------------------------

Usage: <createBatchFolders.sh> configFile pathToCreateThem mv/cp

WARNING: 
-You must be placed at the directory that contains all the files mentioned in the config file.
-Files must have an extension (eg., 'this.file.txt'/'thisFile.txt' YES --> 'this.File' NO)

Config File example:
<filename1>
<filename2>
...
<filenameN> 

---------------------------------------------------------------------
"

else

if [ -z $2 ]
then 

echo "You didn't provide a path to create the folders. The program will exit."

else

camino=$2

if [ -z $3 ]
then
echo "You didn't provide an action (cp/mv). The program will exit."

else

action=$3
while read i;
do 

linea=( $i )
filenm=${linea[0]}

folder=${filenm%.*}
mkdir $camino/$folder
if [ "$action" == "cp" ]
then
cp ./$filenm $camino/$folder
else
if [ "$action" == "mv" ]
then 
mv ./$filenm $camino/$folder
else 
echo "The action provided must be mv (move) or cp (copy)"
fi
fi

done < $1

fi
fi
fi
