## Commands used for the phylogenetical reconstructions (RAxML)

## requires bcftools to call vcf-to-tab 

#:::::::: SETUP 
cat filtered_snps.vcf | vcf-to-tab > snp.tab
perl ~/scripts/perl/vcf_tab_to_fasta_alignment_CHANGEhETERO.pl --output_ref -i snp.tab > concatenatedChangeHeteroToFirstSNP.fasta
python ~/scripts/__moira/python/extractVariableSites_aln.py -i concatenatedChangeHeteroToFirstSNP.fasta -o concatenatedChangeHeteroToFirstSNPonlyvars.fasta


#:::::::: RAxML
nohup raxmlHPC-PTHREADS-SSE3 -T 3 -f d -p 32454 -m ASC_GTRGAMMA -s concatenatedChangeHeteroToFirstSNPonlyvars.fasta -# 10 -n MultipleOriginal --asc-corr=lewis &
nohup raxmlHPC-PTHREADS-SSE3 -T 3  -f d -p 32454 -m ASC_GTRGAMMA -s concatenatedChangeHeteroToFirstSNPonlyvars.fasta -# 100 -b 435345 -n MultipleBootstrap --asc-corr=lewis &
nohup raxmlHPC -f b -m ASC_GTRGAMMA -z RAxML_bootstrap.MultipleBootstrap -t RAxML_bestTree.MultipleOriginal -n BestTree --asc-corr=lewis &