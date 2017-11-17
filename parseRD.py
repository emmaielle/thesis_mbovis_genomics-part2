# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 15:34:12 2016

@author: mlasserre
"""

# usage:

import sys, argparse

parser = argparse.ArgumentParser(description="Parse regions of difference from a bedtools genomecov output")
parser.add_argument(dest="inputFile", type=str, nargs=1, metavar="i", help="bedtools genomecov output file")
parser.add_argument(dest="len", type=str, nargs=1, default=75, metavar="l", help="Length of the smallest desired RD (default 75)")

#parser.add_argument(dest="end", type=str, nargs=1, metavar="end", help="Pattern at the end of the sequence")
#parser.add_argument("-N", type=int, nargs="?", default=0, help="Number of mismatches allowed (default: 0)")

bedOut = []
length = 75
aRD_Storage = []
aGaps_Storage = []

def setup():
    if len(sys.argv)== 1:
        parser.print_help()
        sys.exit(1)
    
    arguments = parser.parse_args()
    
    inputFile = arguments.inputFile[0]
    extension = inputFile.split(".")
    extension = extension[-1]
    
    global length, bedOut
    length = arguments.len[0]
        
    #end = arguments.end[0]
    
    inputF = open(inputFile, "r")
    
    bedOut = inputF.readlines()
    
    #mismatches = arguments.N
    parseBedtoolsOutput()



def parseBedtoolsOutput():
    bContinuum = False
    iBeginningRD = 0
    iEndRD = 0
    iLengthTemp = 0
    RD = ''
    global aRD_Storage, aGaps_Storage
    aRD_Storage = [] # here you save the RDs
    aGaps_Storage = [] # here you save all the gaps regardless of their size
    for i in xrange(0, len(bedOut)):
        splitLine = bedOut[i].split("\t")
        coverage = splitLine[2][:-1]
        if (coverage == "0" or coverage == "1"):
            if (bContinuum == False):
                bContinuum = True
                iBeginningRD = i+1 #Save the beginning of the RD at the first occurrence of a cov = 0 (+1 -- 0coord-based)
            else:
                iLengthTemp = iLengthTemp + 1
        else:
            if (bContinuum == True):
                bContinuum = False
                iEndRD = i ## because it's the previous position of the current
                RD = str(iBeginningRD) + "\t" + str(iEndRD) + "\t" + str(iLengthTemp+1) ## length has to be inclusive
        
        if (RD != ''):
            if (iLengthTemp+1 > int(length)):
                aRD_Storage.append(RD)
            aGaps_Storage.append(RD)
            iLengthTemp = 0
            RD = ''
            iBeginningRD = 0
            iEndRD = 0
        

def printOut():
    print("RD")
    for i in xrange(0, len(aRD_Storage)):
        print(aRD_Storage[i])
    
    print("Gaps")
    for i in xrange(0, len(aGaps_Storage)):
        print(aGaps_Storage[i])    


def writeRD_Out():
    outFile = open("RDs01.out", "w")
    outFile.writelines("Regions of difference found larger than " + str(length) + ":\n")
    outFile.writelines("Start(inc)" + "\tEnd(inc)" + "\tLength\n")
    for i in xrange(0, len(aRD_Storage)):
        outFile.writelines(aRD_Storage[i] + "\n")
        
    outFile.close()
    
    outFileGap = open("GAPs01.out", "w")
    outFileGap.writelines("Gaps found:\n")
    outFileGap.writelines("Start(inc)" + "\tEnd(inc)" + "\tLength\n")
    for i in xrange(0, len(aGaps_Storage)):
        outFileGap.writelines(aGaps_Storage[i] + "\n")
        
    outFileGap.close()


setup()
printOut()
writeRD_Out()
