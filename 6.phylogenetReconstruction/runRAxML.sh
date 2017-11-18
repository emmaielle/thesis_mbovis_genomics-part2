## Commands used for the phylogenetical reconstructions (RAxML)
## requires bcftools to call vcf-to-tab 

#:::::::: SETUP 
cat filtered_snps.vcf | vcf-to-tab > snp.tab
## PARSE SNP IN TAB FORMAT, AND OUTPUT AN ALIGNMENT FROM IT FOR EACH SAMPLE
## (modified from https://code.google.com/archive/p/vcf-tab-to-fasta/ to support haploid organisms)
perl ./vcf_tab_to_fasta_alignment_CHANGEhETERO.pl --output_ref -i snp.tab > concatenatedChangeHeteroToFirstSNP.fasta
## Remove from an alignment the sites that are identical but made it to this point from being erroneously called as heterozygous
python ./extractVariableSites_aln.py -i concatenatedChangeHeteroToFirstSNP.fasta -o concatenatedChangeHeteroToFirstSNPonlyvars.fasta

#:::::::: RAxML
## Using 3 threads, random seed, Ascertainment bias correction, gamma model. Then, 100 bootstrap iterations.
## Nohup &, for remote console calling
nohup raxmlHPC-PTHREADS-SSE3 -T 3 -f d -p 32454 -m ASC_GTRGAMMA -s concatenatedChangeHeteroToFirstSNPonlyvars.fasta -# 10 -n MultipleOriginal --asc-corr=lewis &
nohup raxmlHPC-PTHREADS-SSE3 -T 3  -f d -p 32454 -m ASC_GTRGAMMA -s concatenatedChangeHeteroToFirstSNPonlyvars.fasta -# 100 -b 435345 -n MultipleBootstrap --asc-corr=lewis &
nohup raxmlHPC -f b -m ASC_GTRGAMMA -z RAxML_bootstrap.MultipleBootstrap -t RAxML_bestTree.MultipleOriginal -n BestTree --asc-corr=lewis &