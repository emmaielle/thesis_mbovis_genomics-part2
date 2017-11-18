

# filterSNPs.py - 
Filter snps from a set of vcf, identifying those specific to input groups that will be able to reconstruct the diversity from the original, complete set of SNPs.

usage: ```python filterSNPs.py [-h] vcf groups```

positional arguments:
* vcf - vcf multisample input, which has been annotated with SNPeff (for SNP filtering by SNP type).
* groups - input file with information on which group each sample belongs to.
           The format of the file is the following:

			\>group1
            sample1
            sample23
            sample589
            ...
            \>groupN
            sample234
            sample988
