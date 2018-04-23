## filterSNPs.py - 
Filter snps from a set of vcf, identifying those specific to input groups that will be able to reconstruct the diversity from the original, complete set of SNPs.

usage: ```python filterSNPs.py [-h] vcf groups```

positional arguments:
* vcf - vcf multisample input, which has been annotated with SNPeff (for SNP filtering by SNP type).
* groups - input file with information on which group each sample belongs to.
           The format of the file is the following:

```
>group1
sample1
sample23
sample589
...
>groupN
sample234
sample988
```

Example: 
>  python ./filterSNPs.py 1220W_URY_OUT.snpEffect.vcf groups.txt

### Output files:

Filename | Explanation
 :---: |  :---:
SNPsANDsamples.out | Tab-separated list of all found SNPs and the samples they are present in.

* For all SNPs shared entirely by 3 groups:

Filename | Explanation
 :---: |  :---:
SNPsEn3GruposEnteros.out | Tab-separated list of SNP IDs and their annotation, separated by group sections.
3grupos.filtered.out | Tab-separated list of SNP IDs and their annotation, only the synonymous variants, by group sections.
3grupos.filtered_snps.vcf | VCF file created from the SNPs resulting from 3grupos.filtered.out.

* For all SNPs only present in all individuals of one group:

Filename | Explanation
 :---: |  :---:
SNPsexclusivosDeGrupo.out | Tab-separated list of SNP IDs and their annotation, separated by group sections.
exclusive.filtered.out | Tab-separated list of SNP IDs and their annotation, only the synonymous variants, by group sections.
exclusive.filtered_snps.vcf | VCF file created from the SNPs resulting from exclusive.filtered.out.
exclusive_snps.vcf | VCF file created from the SNPs resulting from SNPsexclusivosDeGrupo.out

* For all SNPs only fully present in one group. If they are present in another group x, not all members of x contain this variant:

Filename | Explanation
 :---: |  :---:
SNPscaracteristicosPorGrupo.out | Tab-separated list of SNP IDs and their annotation, separated by group sections. 
characteristic.filtered.out | Tab-separated list of SNP IDs and their annotation, only the synonymous variants, by group sections.
characteristic.filtered_snps.vcf | VCF file created from the SNPs resulting from characteristic.filtered.out.
characteristic_snps.vcf | VCF file created from the SNPs resulting from SNPscaracteristicosPorGrupo.out

## reduceVCF.py -
Given an input vcf and a list of SNP IDs, reduce the original vcf to contain only the selected SNPS.

Usage: ```reduceVCF.py [-h] vcf snps [snps ...]```

positional arguments:
* vcf - vcf input
* snps - input all the desired SNP IDs (position-REF-ALT) which we want to mantain 

Example: 
> python reduceVCF.py file.vcf '324355-A-T' '8365-T-G' ... '40584345-T-A'

## bovisCode.py - 

Identify M. bovis strains at the sub lineage level

Input should be either VCF of the SNP calling process (-vcf) or the result from SNP typing the SNP barcode described in README (-snp)

optional arguments:
* -h, --help  show this help message and exit
* --vcf vcf   vcf of the strain
* --snp snp   SNP typing results shown in diferent lines and tab separated, as follows:

``` ID          FOUND
    POS-REF-ALT    1
    POS-REF-ALT    0
```
* --s s       name of the studied strain

Usage example: ```while read i; do python bovisCode.py --vcf $i --s $i; done < list```