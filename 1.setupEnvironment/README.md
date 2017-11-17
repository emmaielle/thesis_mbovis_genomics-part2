# Scripts for downloading all the sra files and locating them in their corresponding folders for downstream analysis 

## 1.createBatchFolders.sh -
Create multiple folders from a config file specifying their names and copies files with the same name to their respective folders. 
It will move or copy the files, according to what the user specifies, so they must be removed from the original path if desired.
If no 2nd argument is provided, then the script won't work.

Usage: 
``` <createBatchFolders.sh> configFile pathToCreateThem mv/cp```

### Tips:
* pathToCreateThem: Absolute paths are recommended 
* mv: move
* cp: copy
* You must be placed at the directory that contains all the files mentioned in the config file.
* Files must have an extension (eg., 'this.file.txt'/'thisFile.txt' YES --> 'this.File' NO)

Config File example:
```
<filename1>
<filename2>
...
<filenameN>
``` 

## 2.fastqDump4Batches.sh -
Apply command ```fastq-dump --split-3``` for a batch of .sra files within folders, compress the .sra file using tar and remove the original to save space.
##### It uses:
* fastq-dump (from **SRAtoolkit** version 2.5.2)
* tar

Usage: ```fastqDump4Batches.sh configFile``` 

### Tips:
* paired/single - 'paired' for paired end library, 'single' for single end library
* Only one .sra file must exist inside each of the provided folders

Config file example:
```
<pathtofolder1_thatHas.sra_files> paired/single
<pathtofolder2_thatHas.sra_files> paired/single
..
<pathtofolderN_thatHas.sra_files> paired/single
```

## 3.createConfigFile.sh -
Automatically create config files that have the entire path of the folders in the current directory and a selected keyword next to each.

Usage: ```3.createConfigFile.sh confName -k keyword [folder1 [folder2]...] ```

### Tips:
* confName - a key name to identify the config file along with the current date, eg.: conf.batches.Dec2015
* k : keyword - a word that you might want to add next to each path. If you don't want to add a keyword, just don't add this argument
* folders - you can explicitly specify each desired folders or just select all folders in the current directory with the * wildcard
* if you may use a keyword, the flag -k must be the first argument of them all, followed by the keyword
itself. Then, you might add the folders of interest

Output example:
```
<path_to_folder1> <keyword>
<path_to_folder2> <keyword>
...
<path_to_folderN> <keyword>
```