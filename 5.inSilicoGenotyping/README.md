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




