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

