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
