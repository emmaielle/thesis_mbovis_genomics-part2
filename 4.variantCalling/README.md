Scripts for variant calling, annotation and VCF manipulation.

## 7.0.VarScan_SNPcalling.sh -
Automated SNP calling for multiple sequencing projects using VarScan 1 sample per strain (indel + SNP together)
(Optimized version for compression of resulting files)

##### It uses:
* VarScan (v2.3.7)
* bgzip
* GATK (v3.5)

Usage: ```7.0.VarScan_SNPcalling.sh <config.file> <pathToReferenceGenome> <varScan location> <GATK location>```

WARNING:
The reference genome is assumed to have been indexed previously and located in ./00.IndexReferenceGenome

ConfigFile example:
```
<path to root for strain 1> 
...
<path to root for strain N> 
```

## 7.1.runSnpEffect.sh - 
Runs snpEffect for a batch of strains of M. bovis.

##### It uses: 
* snpEffect (version 4.2 (build 2015-12-05))

Usage: ```bash <7.1.runSnpEffect.sh> <1:configFile.conf> <snpEff location> <snpEff.config location>```

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

## 7.2.mergeMultipleVCF_CombineVariants.sh - 
Merge vcfs from multiple independent files into one with many samples from ALL the vcfs in the directory (Careful)

Usage: ```bash 7.2.mergeMultipleVCF_CombineVariants.sh <outputFile.vcf> <GATK location> <pathToReference>```

* outputFile.vcf - Name desired for the output file  


