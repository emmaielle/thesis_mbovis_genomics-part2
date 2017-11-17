Scripts for the automation of alignment tasks against a reference using BWA and posterior calculations.

## 6.0.BWA_samtools.sh
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
