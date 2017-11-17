# thesis_mbovis_genomics-part2
:octocat: Scripts developed for the elaboration of the second chapter of my M.S. thesis: "Genómica comparativa de Mycobacterium bovis: aproximaciones epidemiológicas y filogenéticas"

Scripts are presented in suggested order of utilization.

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

## 4.trimANDfilterReads_orFullGenomes.sh
Trims and filters reads with overall quality score below <qs> and, from the remaining reads, calculates the coverage. If it is lower than <cov>, it rejects the whole sequencing project. It works for all the selected folders inside the current directory.

##### It uses:
- NGSQCToolkit (v2.3.3)

Usage: ```bash <filterReads_orFullGenomes.sh> qs cov folder1 [folder2 .. folderN]```

Example: ```bash filterReads_orFullGenomes.sh 20 30 *```

Tips:
* qs: quality score threshold (int)
* cov: coverage threshold (int)
* If you're using the * wildcard, make sure you ONLY have folders in it, not loose files
* fastq files must have extension .fastq (not .fq)

Output:
- accepted.genomes.txt
- rejected.genomes.txt

