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
Trims and filters reads with overall quality score below ```qs``` and, from the remaining reads, calculates the coverage. If it is lower than ```cov```, it rejects the whole sequencing project. It works for all the selected folders inside the current directory.

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


Scripts for the automation of alignment tasks against a reference using BWA and posterior calculations.

## 6.0.BWA_samtools.sh -
Automated BWA alignment & samtools conversion, filtering out potential human contaminated reads (Optimized version to handle size limits)

##### It uses: 
* BWA (bwa aln -l 15 -k 3 && bwa sampe). For BWA, version 0.7.12-r1039
* Samtools, version 0.1.18 (r982:295)

Usage: ```bash <pathtoBWA_samtools.sh> <1:configFile.conf> <2:pathtoReferenceToMapIn> <3:pathtoReferenceToMapOut_INDEX>```

Tips:
* 2 - The second parameter should be the path for the reference genome file if the genome hasn't been indexed, OR the FOLDER for the previously indexed genome, to elude from the process of indexing again. NOTE: for M bovis, the index is located in Tb73 strain, so the only option for you to have an index is if it's in Tb73.
* 3 - Parameter 3 is a directory too, not the actual index file. 
* Absolute paths are needed
* fastq files must have extension .fastq (not .fq)
* fastqFolders must be named identical to the fastqFiles

configFile example:
```
<path_to_folder1>
<path_to_folder2>
...
<path_to_folderN>
```

## 6.1.BWA_flagstat_getPercentageOfreadsAligned.sh -
Flagstat and percentage of alignment. Outputs a config.file composed of all of the input strains followed by their alignment status downstream analyses. This is calculated by determining the percentage of alignment against a reference: If it mapped more than 80% of the reads, then the config file will suggest to use all of the original reads. On the contrary, if the mapping covers less than 80% of all the reads, the output config file will indicate to use only the mapped reads for this strain, in order to avoid contamination during the sequencing.

##### It uses: 
* Samtools, version 0.1.18 (r982:295)

Usage: ```bash <6.1.BWA_flagstat_getPercentageOfreadsAligned.sh> <config file>```
  
Config example:
```
<pathtostrain1>
<pathtostrain2>
..
<pathtostrainN>
```

Example output:
```
<pathtostrain1> <ALL/MAPPED>
...
<pathtostrainN> <ALL/MAPPED>
```

## 6.2.BWA_flagstat_getPercentageOfHUMANreadsAligned.sh -
Flagstat and percentage of alignment against human reference genome. Similar to script 6.1.

##### It uses: 
- Samtools, version 0.1.18 (r982:295)

Usage: ```bash <6.2.BWA_flagstat_getPercentageOfHUMANreadsAligned.sh> <configfile>```

Config example:
```
<pathtofolder1>
<pathtofolder2>
...
<pathtofolderN>
```

## 6.3.countReadsFromBAM.sh -
Count reads from any bam file. Works for batches

##### It uses:
* Samtools

Usage: ```6.3.countReadsFromBAM.sh <config.file>``` 

NOTE:
* Assumes a file structure formed by following the previous steps/scripts. In this case, this script will look for a "2.samtoolsFilter" folder inside the given path.

ConfigFile example:
```
<pathTostrainFolder1>
...
<pathTostrainFolderN>
```

## 6.4.getCoverage_fromBam.sh - 
Calculates the coverage of a standard bam file from a batch of strains for M. bovis.

##### It uses:
- Samtools

Usage: 6.4.getCoverage_fromBam.sh <config.file> <bam.prefix>

Tips:
* bam.prefix - the prefix refers to the keyword of the bam file that precedes the name of each strain. It's required as to avoid confusion when more than one bam file is present in the same folder.
* bam files are assumed to be in the folder 2.samtoolsFilter for each strain

ConfigFile example:
```
<path to root for strain 1>
...
<path to root for strain N>
```
