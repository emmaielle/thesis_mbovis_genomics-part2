# BovisCode.py

import sys
import argparse
import os
from glob import glob
from argparse import RawTextHelpFormatter

parser = argparse.ArgumentParser(description="--- Identify M. bovis strains at the sub lineage level ---\n\n" +
	"Input should be either VCF of the SNP calling process (-vcf) or the result from SNP typing the SNP barcode described in README (-typ)",
	formatter_class=RawTextHelpFormatter)
parser.add_argument('--vcf', dest="vcfinputANN", type=str,
                    nargs=1, metavar="vcf", help="vcf of the strain")
parser.add_argument('--snp', dest="typing", type=str, nargs=1, metavar="snp",
                    help="SNP typing results in diferent linea and tab separated, as follows:\n #ID          FOUND\nPOS-REF-ALT    1\nPOS-REF-ALT    0")
parser.add_argument('--s', dest="strain", type=str, nargs=1, metavar="s", help="\
name of the studied strain")

snpsItHas = []
vcfLines = []
snpArray = []
snpLines = []

# Lineages
identities = {"1": 4, "1.1": 0, "1.2": 6,  "1.3": 2,
                "2": 7, "2.2": 5, "2.3": 4, "2.4": 11, # 2 tiene extre
                "3": 3, "3.1": 2, "3.3": 4, # 3 tiene extra
                "4": 0, "4.1": 7, "4.2": 3, "4.3": 2,
                "5": 0, "5.1": 0, "5.2": 2, "5.3": 2}


# SNP BARCODE USED FOR THE ANALYSIS:
barcode = {"4077846-C-A": ["1", "Exclusive" ],
            "1048294-T-C": ["1", "Exclusive" ],
            "3467191-C-A": ["1", "Exclusive"],
            "1779047-C-T": ["1.2", "Distinctive"],
            "222939-A-G": ["1.2", "Distinctive"],
            "2670247-G-A": ["1.2", "Distinctive"],
            "2973577-C-T": ["1.2", "Distinctive"],
            "566174-A-C": ["1.2", "Distinctive"],
            "321009-T-C": ["1.2", "Distinctive"],
            "359494-C-T": ["1.3", "Exclusive"],
            "4043145-G-A": ["1.3", "Exclusive"],
            "3265769-A-G": ["1", "2", "Shared"],
            "1513457-C-T": ["2", "Exclusive"],
            "4227214-G-A": ["2", "Exclusive"],
            "299636-A-G": ["2", "Exclusive"],
            "3448807-C-T": ["2", 'Exclusive'],
            "1475059-A-AC": [ "2.4", 'Shared'],  
            "802338-C-T": ["2.2", 'Exclusive'],
            "904074-C-T": ["2.2", 'Exclusive'],
            "2662983-G-A": ["2.2", 'Exclusive'],
            "232188-G-C": ["2.4", 'Shared'],         
            "4299984-A-G": ["2.3", 'Distinctive'],
            "2363358-G-A": ["2.4", 'Exclusive'],
            "3856175-T-C": ["2.4", 'Exclusive'],
            "699173-C-T": ["2.4", 'Exclusive'],
            "1998304-G-A": ["2.4", 'Distinctive'],
            "824300-T-C": ["2.4", 'Distinctive'],
            "402355-T-C": ["2.2", "2,4", 'Shared'],
            "2278824-G-A": ["2.2", "2.4", 'Shared'],
            "265675-T-C": ["2.3", "2.4", 'Shared'],
            "547559-A-G": ["2.3", "2.4", 'Shared'],
            "2471336-G-A": ["2.3", "2.4", 'Shared'],
            "1828921-A-G": ["3", 'Distinctive'],    
            "130237-T-C": ["3", 'Distinctive'],
            "2373913-C-T": ["3", 'Distinctive'],
            "240616-C-T": ["3.1", 'Exclusive'],
            "2742170-G-A": ["3.1", "Exclusive"],
            "3618489-C-T": ["3.3", 'Distinctive'],
            "854043-G-A": ["3.3", 'Distinctive'],
            "483845-T-C": ["3.3", 'Distinctive'],
            "1295429-C-T": ["3.3", 'Distinctive'],
            "1226368-C-T": ["4.1", 'Exclusive'],
            "4077342-G-A": ["4.1", 'Exclusive'],
            "3579879-G-C": ["4.1", 'Exclusive'],
            "3901971-G-A": ["4.1", 'Exclusive'],
            "804997-T-C": ["4.1", "Distinctive"],
            "3619791-G-A": ["4.1", 'Distinctive'],
            "1493708-G-A": ["4.1", 'Distinctive'],
            "1527223-A-G": ["4.2", 'Exclusive'],
            "3278284-G-A": ["4.2", 'Distinctive'],
            "1530862-A-T": ["4.3", 'Distinctive'],
            "1597426-G-A": ["4.2", "4.3", 'Shared'],
            "236518-C-T": ["5.2", 'Exclusive'],
            "2989417-C-T": ["5.2", 'Exclusive'],
            "2202679-G-A": ["5.3", 'Exclusive'],
            "3210746-G-A": ["5.3", 'Exclusive'] 
            }


def setup():
    global vcfLines, snpArray, snpLines, strain
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    arguments = parser.parse_args()
    if(arguments.vcfinputANN):
        vcf = arguments.vcfinputANN[0]
        vcfF = open(vcf, "r")
        vcfLines = vcfF.readlines()
        parseVCF()

    if (arguments.strain):
        strain = arguments.strain[0]
    if (arguments.typing):
        snp = arguments.typing[0]
        snpF = open(snp, "r")
        snpLines = snpF.readlines()
        parseSNPtyping()

    obtainLineages()


def parseVCF():
    global snpsItHas
    for j in xrange(0, len(vcfLines)):
        if (vcfLines[j][0] != "#"):
            noNewLine = vcfLines[j][:-1]
            aLineTemp = noNewLine.split('\t')
            # POSREFALT
            snpID = aLineTemp[1] + '-' + aLineTemp[3] + '-' + aLineTemp[4]
            snpsItHas.append(snpID)


def parseSNPtyping():
    global snpsItHas
    #    ID          FOUND
    # POS-REF-ALT    1
    # POS-REF-ALT    0
    for i in xrange(0, len(snpLines)):
        if (snpLines[i][0] != "#"):
            lineArr = snpLines[i].split('\t')
            if (lineArr[1] == 1):
                snpsItHas.append(lineArr[0])


def obtainLineages():
    barcodeInStrain = []
    possibleIdentity = identities
    strainLineage = ""
    strainSublineage = ""
    error = False
    for i in barcode:
        found = False
        lineage = barcode[i][0:-1]
        snpCategory = barcode[i][-1]
        # First Search for Exclusive SNPs to retain ID but still go through all SNPs to get those not Found
        for j in snpsItHas:
            if (i == j):
                found = True
                barcodeInStrain.append([i, barcode[i], "1"])
                break
            else:
                found = False
        if (not found):
            barcodeInStrain.append([i, barcode[i], "0"])

    yesSNP = {}
    for item in barcodeInStrain:
        if (item[2] == '1'):
            for lin in xrange(0, len(item[1]) - 1):
                if (item[1][lin] not in yesSNP):
                    yesSNP[item[1][lin]] = 1

                else:
                    yesSNP[item[1][lin]] += 1
    matches = []
    for key in identities:
        # the num of snps pointing to key is the same
        if (key in yesSNP and identities[key] == yesSNP[key]):
            matches.append(key)

    # Si el lin no es 1 o 5 (que tienen 1 c/u sublin sin SNP)
    # tienen que tener sublin
    # para cada item en matches
    # hay alguno q sea sublinaje?
    sublin = []
    lin = []
    for item in matches:
        if (len(item) == 3):
            sublin.append(item)
        if (len(item) == 1):
            lin.append(item)
    
    if (strain):
        print "Cepa " + strain

    if(len(sublin) > 1):
        print "There is more than one predicted sublineage: " + str(sublin) + "\n"
    elif (len(sublin) == 1):
        if (sublin[0][0] in lin):
            print "The predicted sublineage for this strain is " + str(sublin) + "\n"
        else:
            print "The predicted sublineage for this strain is " + str(sublin) + "\nNot all of the SNPs of the main lineage were found for this strain\n"
    else:
        if (len(lin) == 1):
            print "The predicted lineage for this strain is " + str(lin) + "\nIt was not possible to predict the sublineage\n"
        elif (len(lin) > 1):
            for l in lin:
                if (l == "1"):
                    print "The predicted sublineage for this strain is 1.1\n"
                    break
                elif (l == '5'):
                    print "The predicted sublineage for this strain is 5.1\n"
                    break
                else:
                    print "There is more than one predicted lineage: " + str(lin) + "\n"
        else:
            print "It was not possible to predict the lineage or sublineage for this strain.\n"



    for num in matches:
        if (len(num) == 1):
            for n in identities:
                if (n[0] == num):
                    pass


setup()
