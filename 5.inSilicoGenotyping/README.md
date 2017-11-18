Tools for genotyping. This included both spoligotyping in silico through SpoTyping and a custom-made pipeline for identification of Regions of Diference.

## 7.0.runSpoTyping_batch.sh
Automated SpoTyping run for multiple strains of *M. bovis*

##### It uses:
- SpoTyping (v2.0)

Usage: ```bash 7.0.runSpotyping_batch.sh <config.file> ```

---------------------------------------------------------------------
configFile example:
```
<path to reads for strain 1>
...
<path to reads for strain N>
```

## 7.1.spolPattern_to_SB.sh
Conversion of known spoligotype patterns to SB numbers

##### It uses:
- mbovis info (SpoligotypePatterns.txt, located in current directory)

Usage: ```7.1.spolPattern_to_SB.sh <input.file>```

---------------------------------------------------------------------
input.file example:
```
<spoligotype binary pattern 1>
...
<spoligotype binary pattern N>
```