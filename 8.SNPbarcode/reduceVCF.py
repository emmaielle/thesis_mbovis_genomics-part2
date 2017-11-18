"""
@author: mlasserre
"""

# usage:

import sys
import argparse
import os
from glob import glob
from argparse import RawTextHelpFormatter

parser = argparse.ArgumentParser(description="Given an input vcf and a list of SNP IDs, reduce the original vcf to contain only the selected SNPS")
parser.add_argument(dest="vcfinputANN", type=str, nargs=1, metavar="vcf", help="vcf input")
parser.add_argument(dest="SNPS", nargs='+', metavar="snps", help="\
input all the desired SNP IDs (position-REF-ALT) which we want to mantain (eg.: python  reduceVCF.py file.vcf '324355-A-T' '8365-T-G' ... '40584345-T-A')")

def setup():

    if len(sys.argv)== 1:
        parser.print_help()
        sys.exit(1)
    
    arguments = parser.parse_args()
    global snps, vcfLines

    vcf = arguments.vcfinputANN[0]
    snps = arguments.SNPS
    print(snps)
    vcfF = open(vcf, "r")
    vcfLines = vcfF.readlines()

    makeVCFQuestionMark(snps)


def makeVCFQuestionMark(snps):
    outFilevcf = open("selected_snps.vcf", "w")
    contador = 0
    for j in xrange(0, len(vcfLines)):
        if (vcfLines[j][0] == "#"):
            outFilevcf.writelines(vcfLines[j])
        else:
            noNewLine = vcfLines[j][:-1] ## delete \n newline
            aLineTemp = noNewLine.split('\t') ## temporary current line
            snpID = aLineTemp[1] + '-' + aLineTemp[3] + '-' + aLineTemp[4] # POS REF ALT
            if (snpID in snps):
                outFilevcf.writelines(vcfLines[j])
                print(snpID +" found")
                contador += 1
    print("Found " + str(contador) + " snps of all the " + str(len(snps)))
    outFilevcf.close()

setup()