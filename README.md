# thesis_mbovis_genomics-part2
:octocat: Scripts developed for the elaboration of the second chapter of my M.S. thesis: "Genómica comparativa de Mycobacterium bovis: aproximaciones epidemiológicas y filogenéticas"

Scripts are presented in suggested order of utilization.

## 1.createBatchFolders.sh -
Create multiple folders from a config file specifying their names and copies files with the same name to their respective folders. 
It will move or copy the files, according to what the user specifies, so they must be removed from the original path if desired.
If no 2nd argument is provided, then the script won't work.

Usage: 
```bash <createBatchFolders.sh> configFile pathToCreateThem mv/cp```

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

Usage: ```bash fastqDump4Batches.sh configFile``` 

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

Usage: ```bash 3.createConfigFile.sh confName -k keyword [folder1 [folder2]...] ```

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

---------------------------------------------------------------------

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


---------------------------------------------------------------------

## 5.0.BWA_samtools.sh -
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

## 5.1.BWA_flagstat_getPercentageOfreadsAligned.sh -
Flagstat and percentage of alignment. Outputs a config.file composed of all of the input strains followed by their alignment status downstream analyses. This is calculated by determining the percentage of alignment against a reference: If it mapped more than 80% of the reads, then the config file will suggest to use all of the original reads. On the contrary, if the mapping covers less than 80% of all the reads, the output config file will indicate to use only the mapped reads for this strain, in order to avoid contamination during the sequencing.

##### It uses: 
* Samtools, version 0.1.18 (r982:295)

Usage: ```bash <5.1.BWA_flagstat_getPercentageOfreadsAligned.sh> <config file>```
  
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

## 5.2.BWA_flagstat_getPercentageOfHUMANreadsAligned.sh -
Flagstat and percentage of alignment against human reference genome. Similar to script 6.1.

##### It uses: 
- Samtools, version 0.1.18 (r982:295)

Usage: ```bash <5.2.BWA_flagstat_getPercentageOfHUMANreadsAligned.sh> <configfile>```

Config example:
```
<pathtofolder1>
<pathtofolder2>
...
<pathtofolderN>
```

## 5.3.countReadsFromBAM.sh -
Count reads from any bam file. Works for batches

##### It uses:
* Samtools

Usage: ```bash 5.3.countReadsFromBAM.sh <config.file>``` 

NOTE:
* Assumes a file structure formed by following the previous steps/scripts. In this case, this script will look for a "2.samtoolsFilter" folder inside the given path.

ConfigFile example:
```
<pathTostrainFolder1>
...
<pathTostrainFolderN>
```

## 5.4.getCoverage_fromBam.sh - 
Calculates the coverage of a standard bam file from a batch of strains for M. bovis.

##### It uses:
- Samtools

Usage: ```bash 5.4.getCoverage_fromBam.sh <config.file> <bam.prefix>```

Tips:
* bam.prefix - the prefix refers to the keyword of the bam file that precedes the name of each strain. It's required as to avoid confusion when more than one bam file is present in the same folder.
* bam files are assumed to be in the folder 2.samtoolsFilter for each strain

ConfigFile example:
```
<path to root for strain 1>
...
<path to root for strain N>
```

---------------------------------------------------------------------

## 6.0.VarScan_SNPcalling.sh -
Automated SNP calling for multiple sequencing projects using VarScan 1 sample per strain (indel + SNP together)
(Optimized version for compression of resulting files)

##### It uses:
* VarScan (v2.3.7)
* bgzip
* GATK (v3.5)

Usage: ```bash 6.0.VarScan_SNPcalling.sh <config.file> <pathToReferenceGenome> <varScan location> <GATK location>```

WARNING:
The reference genome is assumed to have been indexed previously and located in ./00.IndexReferenceGenome

ConfigFile example:
```
<path to root for strain 1> 
...
<path to root for strain N> 
```

## 6.1.runSnpEffect.sh - 
Runs snpEffect for a batch of strains of M. bovis.

##### It uses: 
* snpEffect (version 4.2 (build 2015-12-05))

Usage: ```bash <6.1.runSnpEffect.sh> <1:configFile.conf> <snpEff location> <snpEff.config location>```

WARNING: 
* Use complete paths 
* snpEff.config local is located in ~/Software/snpEff/snpEff.config. For external use, you need to set up snpEff.
* Assumes a file structure formed by following the previous steps/scripts. In this case, this script will look for a "5.SNPcalling/5.1.VarScan" folder inside the given path.

ConfigFile example:
```
<path_to_folder1>
<path_to_folder2>
...
<path_to_folderN>
```

## 6.2.mergeMultipleVCF_CombineVariants.sh - 
Merge vcfs from multiple independent files into one with many samples from ALL the vcfs in the directory (Careful)

Usage: ```bash 6.2.mergeMultipleVCF_CombineVariants.sh <outputFile.vcf> <GATK location> <pathToReference>```

* outputFile.vcf - Name desired for the output file  


---------------------------------------------------------------------

Tools for genotyping. This included both spoligotyping in silico through SpoTyping and a custom-made pipeline for identification of Regions of Diference.

## 7.0.runSpoTyping_batch.sh -
Automated SpoTyping run for multiple strains of *M. bovis*

##### It uses:
- SpoTyping (v2.0)

Usage: ```bash 7.0.runSpotyping_batch.sh <config.file> <SpoTyping location folder> ```

configFile example:
```
<path to reads for strain 1>
...
<path to reads for strain N>
```

## 7.1.spolPattern_to_SB.sh -
Conversion of known spoligotype patterns to SB numbers

##### It uses:
- mbovis info (SpoligotypePatterns.txt, located in current directory)

Usage: ```bash 7.1.spolPattern_to_SB.sh <input.file>```

input.file example:
```
<spoligotype binary pattern 1>
...
<spoligotype binary pattern N>
```

## 8.0.RD_discovery.sh -
Run coverage analysis for a batch of files and find Regions of Difference

##### It uses: 
* parseRD.py
* bedtools genomecov v2.17.0

Usage: ```bash <8.0.RD_discovery.sh> <1:configFile.conf> <referencegenome.fasta>```

WARNING: 
* Config with absolute paths
* fastq files in the config must have extension .bam (aligned)
* Assumes a file structure formed by following the previous steps/scripts. In this case, this script will look for a 1.BWA.alineamiento/' folder inside the given path. 


configFile example:
```
<path_to_folder1>
<path_to_folder2>
...
<path_to_folderN>
```

## 8.1.parseRD_forUniqIDs.py -
Parse multiple RD.out files to obtain common RDs.

Outputs:
* input.unidosMenor_100.out - Original gaps parsed to join together when the diference in position is 100 pb or less (size 1 + diff + size 2). Saved in each strain's location folder.
* RDsets.byStrain.output - File with all strains and the RDs found for each. 
* RDsets.byRD.output - File with all RDs found, their ID, number and identity of the strains that have it.

Usage: ```python 8.1.parseRD_forUniqIDs.py [-h] i l```

Positional arguments:
  * i - config file with the path locations of each RD.out files to analyze
  * l - Length of the smallest desired RD (default 75)

---------------------------------------------------------------------

plotTree.py and plotTree_backbone.py have been forked and modifyed from @katholt repository (https://github.com/katholt/plotTree)
For more information on usage, visit their repo and website (https://holtlab.net/2016/10/12/global-picture-typhoid/). 

Dependencies: ete2 (ETE Toolkit 2), pyqt4

Modified their script to suit the particular needs of my anaysis.

## plotTree.py - 
It has added functionalities such as ```delete_branches``` in order to hide certain branches without modiying the resulting topology, and styling decisions. 

Example usage 1: 
> python ./plotTree.py --tree tree.nwk --info info.csv --outpdf outfile.pdf

Example usage 2 (full): 
> xvfb-run python ./plotTree.py --tree RAxML_bipartitions.BestTree.tre --info ./genotypes.csv --output test.png --width 750 --font_size 18 --fan --tags --labels Spoligotype Continent Cluster2_10_1 Cluster2_10_2 RD1009519_1010918 RD1209296_1210923 --outgroup SRR1792164 --colour_tags Cluster2_10_1 --branch_thickness 11 --line_width 2 --show_leaf_names --delete_branches SRR1173725 SRR1173284 --colour_backgrounds_by Cluster2_10_1 --print_colour_dict --colour_dict '{"NA":"White", "SB0145": "Gold", "SB0130":"MediumTurquoise", "SB0274":"Sienna", "SB1072":"LightSkyBlue", "SB0140":"Indigo","Not_found":"White", "SB1041": "OliveDrab","SB0265":"LimeGreen", "SB0673":"Orange", "SB1499":"Tan", "SB0121":"LightCoral", "SB1750":"Violet", "SB1040":"Red", "SB1757":"Coral", "SB0307":"Teal","SB0986":"DarkBlue", "SB1812":"#78c679", "SB0943":"#31a354", "SB1071":"#006837", "SB1033":"#fe9929", "SB2020":"#c2e699", "SB1308":"#ce1256", "SB0971":"#31a354", "SB1345":"#a1dab4", "SB0327":"#b2e2e2", "SB0484":"#238b45", "SB0292":"#fbb4b9", "SB1751":"#feebe2", "SB1758":"#ae017e", "SB1502":"#bae4bc", "SB2014":"#88419d", "SB1745":"#8c96c6", "SB0271":"#b3cde3", "SB1216":"#edf8fb","SB0815":"#fef0d9", "SB1069":"#ffffcc", "SB1348":"#cccccc", "SB2011":"#fed98e", "SB0267":"#fdae61", "SB2007":"#2b83ba", "SB1039":"#c2a5cf", "SB0120":"#7b3294", "SB2100":"#b8e186", "SB1031":"#d01c8b", "SB1504":"#dfc27d", "SB1446":"#a6611a", "SB0273":"#80cdc1", "SB0980":"#018571""}'

For the automatic (and random) assertion of colours to attributes from the metadata file (set in the --info parameter), you can use parseString.py and/or numberedPrefix_toColor.py 

## plotTree_backbone.py - 
Simplified version for the attainment of a rectangular, pruned tree. Hardcoded at it's best to fit my own data. Therefore, for flexibility, you should use plotTree.py

Example:
> xvfb-run python ../plotTree_backbone.py --tree RAxML_bipartitions.BestTree.sindeAntes.uniq --info genotipos3.csv --output backbone.png --width 200 --font_size 16 --branch_thickness 3 --line_width 2 --show_leaf_names --no_guiding_lines --colour_backgrounds_by Cluster3_10_2 --colour_dict '{"NA":"White", "Lineage2 5": "#946DA3", "Lineage2 4": "#540D6E","Lineage2 7": "#6F5196", "Lineage2 6": "#8D80AD", "Lineage2 1": "#d7191c",  "Lineage2 3": "#F49CBB", "Lineage2 2": "#EE4266", "Lineage2 9": "#6D9DC5", "Lineage2 8":"#53599A", "Lineage2 11": "#46ACC2", "Lineage2 10": "#496DDB", "Lineage2 13": "#679436", "Lineage2 12": "#5FAD41", "Lineage2 15": "#aecf8e", "Lineage2 14": "#8ecf8f", "Lineage2 17": "#E2EB98", "Lineage2 16": "#95BF74", "Lineage2 19": "#EE964B", "Lineage2 18": "#FFD23F", "Lineage 4": "#046614", "Lineage 5": "#877c02", "Lineage 2": "#490163", "Lineage 3": "#1c0496", "Lineage 1": "#960303", "NA":"White"}' --colour_branches_by Cluster3_10_1 --length_scale 7500 --tags --outgroup SRR1792164 --delete_branches SRR1792164

## parseString_toColor.py - 
Parse string to output a dictionary of random colours that adjust to plotTree.py colour format. Separator: space.

Usage: ```parseString.py [-h] str```

positional arguments:
  * str - String space-separated

Example:
```python ./parseString.py "uno dos"```

Output:
> {"uno": "#FFC81D", "dos": "#3A7BB4"}

## numberedPrefix_toColor.py - 
Given a prefix and an int, appends the prefix to the int from 0 to int and assigns each a random colour, to output a dictionary that adjust to plotTree.py format. Separator: space

usage: ```python ./numberedPrefix_toColor.py [-h] m p```

positional arguments:
  * m - Max num of items
  * p - Desired prefix

Example:
> python ./numberedPrefix_toColor.py 8 prefix

Output:
> {"prefix 1": "MediumTurquoise", "prefix 2": "OliveDrab", "prefix 3": "Teal", "prefix 4": "#E41A1C", "prefix 5": "#3A85A8", "prefix 6": "#FFDD25", "prefix 7": "Violet", "prefix 8": "MediumTurquoise"}
