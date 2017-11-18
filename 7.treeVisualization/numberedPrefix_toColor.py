import sys, argparse
import pdb
from operator import itemgetter
from argparse import RawTextHelpFormatter
from random import randint

parser = argparse.ArgumentParser(description="Parse strings to create Lineage colouring to plotTree.py colour format. Separator: space")
parser.add_argument(dest="max", type=int, nargs=1, metavar="m", help="Max num of lineages")
parser.add_argument(dest="prefix", type=str, nargs=1, metavar="p", help="Prefix for lineages")

def setup():
    if len(sys.argv)== 1:
        parser.print_help()
        sys.exit(1)
    
    arguments = parser.parse_args()
    maxim = arguments.max[0]
    prefix = arguments.prefix[0]      
    
    parseString(prefix, maxim)

def parseString(prefix, maxim):
    arrayOut = []
    #colours_50 = ["#E41A1C","#C72A35","#AB3A4E","#8F4A68","#735B81","#566B9B","#3A7BB4","#3A85A8","#3D8D96","#419584","#449D72","#48A460","#4CAD4E","#56A354","#629363","#6E8371","#7A7380","#87638F","#93539D","#A25392","#B35A77","#C4625D","#D46A42","#E57227","#F67A0D","#FF8904","#FF9E0C","#FFB314","#FFC81D","#FFDD25","#FFF12D","#F9F432","#EBD930","#DCBD2E","#CDA12C","#BF862B","#B06A29","#A9572E","#B65E46","#C3655F","#D06C78","#DE7390","#EB7AA9","#F581BE","#E585B8","#D689B1","#C78DAB","#B791A5","#A8959F","#999999"]
    colours_50 = ["Red", "DarkBlue", "Gold", "LimeGreen","Violet","MediumTurquoise", "LimeGreen", "LimeGreen", "Sienna","LightCoral","LightSkyBlue","Indigo","Tan","Coral","OliveDrab","Teal", "#E41A1C","#C72A35","#AB3A4E","#8F4A68","#735B81","#566B9B","#3A7BB4","#3A85A8","#3D8D96","#419584", "#FF8904","#FF9E0C","#FFB314","#FFC81D","#FFDD25","#FFF12D","#F9F432","#EBD930","#DCBD2E","DarkBlue", "Gold", "LimeGreen","Violet","MediumTurquoise","Sienna","LightCoral","LightSkyBlue","Indigo","Tan","Coral","OliveDrab","Teal", "#E41A1C","#C72A35"]
    for i in xrange(1, maxim+1):
        print(i)
        colours_50, chosen = randomColour(colours_50)
        temp = "\""+ prefix + " " + str(i) +"\": \""+ chosen +"\""
        arrayOut.append(temp)
    stringed = ", ".join(arrayOut)
    stringed = "{" + stringed + "}"
    print(stringed)


def randomColour(arrayRemainingColours):
    size = len(arrayRemainingColours)
    random = randint(0, size-1)
    chosen = arrayRemainingColours[random]
    del arrayRemainingColours[random]
    return arrayRemainingColours, chosen

setup()


