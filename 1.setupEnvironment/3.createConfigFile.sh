# mlasserre@pasteur.edu.uy
# help: automatically create config files that havethe entire path and a selected keyword

if [ -z "$1" ]
then
 
echo "
createConfig: Automatically create config files that have the entire path of the folders in the current
directory and a selected keyword next to each.

-----------------------------   HELP   -----------------------------

Usage: 3.createConfigFile.sh confName -k keyword [folder1 [folder2]...]

confName - a key name to identify the config file along with the current date. 
eg.: batches --> conf.batches.Dec2015

-k : keyword - a word that you might want to add next to each path. If you don't want to add a keyword, 
just don't add this argument

folders - you can explicitly specify each desired folders or just select all folders with the * wildcard

WARNINGS: 
- if you may use a keyword, the flag -k must be the first argument of them all, followed by the keyword
itself. Then, you might add the folders of interest

---------------------------------------------------------------------

output example:
<path_to_folder1> <keyword>
<path_to_folder2> <keyword>
...
<path_to_folderN> <keyword>
"

else

if [ -z $2 ]
then

echo "You need to provide at least two arguments
usage: 3.createConfigFile.sh confName [-k keyword] folder1 [folder2...]
"

else

confName=conf.$1.$(formDate)
touch conf.$1.$(formDate)
shift

for i in $@
do	
	if [ "$i" == "-k" ]
	then
		k="true"
	shift
	
	else 
		if [ "$k" == "true" ]
		then
			KEYWORD=$i
			k="false"
		else

			if [ ! -z $KEYWORD ]
			then 
				echo $(pwd)/$i $KEYWORD >> $confName
			else
				echo $(pwd)/$i  >> $confName
			fi
		fi			

	shift
	fi
	
done

fi

fi
