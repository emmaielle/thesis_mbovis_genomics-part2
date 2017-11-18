"""
@author: mlasserre
"""

# usage:

import sys
import argparse
import os
from glob import glob
from argparse import RawTextHelpFormatter

parser = argparse.ArgumentParser(description="Filter snps from a set of vcf, identifying those specific to input groups that will be able to reconstruct the diversity from the original, complete set of SNPs.", formatter_class=RawTextHelpFormatter)
parser.add_argument(dest="vcfinputANN", type=str, nargs=1, metavar="vcf", help="\
vcf multisample input, which has been annotated with SNPeff \n(for SNP filtering by functional groups)")

parser.add_argument(dest="groups", type=str, nargs=1, metavar="groups", help="\
input file with information on which group each sample belongs to. \nThe format of the file is the following:\n\
\n\t>grupo1\n\tsample1\n\tsample23\n\tsample589\n\t...\n\t>grupoN\n\tsample234\n\tsample988")

#example
#Chromosome      289     .       G       A       .       PASS    AC=2;ADP=80;AF=1.00;AN=2;HET=0;HOM=1;NC=0;WT=0;set=SRR1791807;ANN=A|missense_variant|MODERATE|dnaA|Mb0001|transcript|CDO41234.1|protein_coding|1/1|c.289G>A|p.Gly97Arg|289/1524|289/1524|97/507||       GT:ABQ:AD:ADF:ADR:DP:FREQ:GQ:PVAL:RBQ:RD:RDF:RDR:SDP    ./.     ./.     ./.

vcfLines = []
groupsLines = []
aSnpWithSamples = [["##SNPID", "##Samples", "##SNPvalue"]]
aSnpExclusivosDeGrupo = []
aSnpComunGrupos = []
dictSnpExclusivosDeGrupoNomGrupo = {}
aSnpCaracteristicosDeGrupo = []
finalArray = []
functionallyFilteredArray = {}
cellWallLines = []
consHypoLines = []
infoPathLines = []
insertioLines = []
intMetabLines = []
lipidMetLines = []
PEandPPELines = []
regulProLines = []
virulencLines = []

cellWallNames = []
consHypoNames = []
infoPathNames = []
insertioNames = []
intMetabNames = []
lipidMetNames = []
PEandPPENames = []
regulProNames = []
virulencNames = []

def setup():

    if len(sys.argv)== 1:
        parser.print_help()
        sys.exit(1)
    
    arguments = parser.parse_args()
    global groupsLines, vcfLines

    vcf = arguments.vcfinputANN[0]
    groups = arguments.groups[0]
    groupsF = open(groups, "r")
    groupsLines = groupsF.readlines()
    vcfF = open(vcf, "r")
    vcfLines = vcfF.readlines()

    parseFunctionalCategories()
    ## si quiero hacer un filtering by functional categories, tengo q asegurarme que el vcf tiene anotacion 
    ## (snpEff)
    parseVCF()

arrayFilteredSNPs = []
def parseVCF():
    
    first = True;
    ## sampleRow es el array con cada sample location in the vcf. Si un sample se llama Tb75.mbURU-004, me voy a quedar 
    ## con la parte despues del punto (mbURU-004) 
    sampleRowString = "" ##CHROM  POS     ID      REF     ALT     QUAL    FILTER  INFO    FORMAT  6556.mbURU-001 ... etc
    i = 0
    while first and i < len(vcfLines):
        if (vcfLines[i][0] != "#"):
            if (first):
                sampleRowString = vcfLines[i-1]
                first = False;
        i += 1
    
    sampleRowArray = sampleRowString.split('\t')
    # Obtener los nombres de cada sample individual, eliminando los . y los .deAntes. que
    # venian del nombre de los archivos 
    global anotacionString
    newSampleRowArray = []
    for m in xrange(0, len(sampleRowArray)):
        if (m == len(sampleRowArray)-1):
            sampleRowArray[m] = sampleRowArray[m][:-1]
        if ('deAntes' in sampleRowArray[m]):
            temp = sampleRowArray[m].split('.deAntes.')[1]
            newSampleRowArray.append(temp)
        elif ('.' in sampleRowArray[m]):
            temp = sampleRowArray[m].split('.')[1]
            if("mbURU" not in temp):
                newSampleRowArray.append(temp)
            else: 
                newSampleRowArray.append(sampleRowArray[m])

    # Armar un array con dos elementos: 
    # 1) el ID del SNP: Posicion, ref, alt.len
    # 2) Un array con todos los samples que poseen este SNP: [sample23, sample130, sample4957, ..., sample54]
    # esto tambien va a llamar a la funcion setGeneAndFunctionalCategory() para cada linea, 
    # dandole la columna de INFO, la cual va a usar para obtener el impacto de la mutacion y el gen mutando
    # y va a considerar si el SNP es sinonimo o no y, si es, a que categoria funcional pertenece el gen al que afecta     
    global aSnpWithSamples
    printo = 0
    for j in xrange(0, len(vcfLines)):
        if (vcfLines[j][0] != "#"):
            noNewLine = vcfLines[j][:-1]
            aLineTemp = noNewLine.split('\t')
            snpID = aLineTemp[1] + '-' + aLineTemp[3] + '-' + aLineTemp[4] # POS REF ALT
            printo += 1
            snpValue = setGeneAndFunctionalCategory(aLineTemp[7], printo < -10) ##false, make true for debugging
            samples = aLineTemp[9:]
            samplesWSnp = []
            # Ejemplo de samples:
            #['./.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', '1/1:18:199:95:104:199:100%:99:3.8756E-119:0:0:0:0:211', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.', './.\n']
            for sample in xrange(0, len(samples)):
                #solo los que presentan ese SNP se guardan en el array
                if (samples[sample] != './.'):
                    sampleId = newSampleRowArray[sample]
                    samplesWSnp.append(sampleId)

            aSnpWithSamples.append([snpID, samplesWSnp, snpValue])

    findSNPsByGroups()
    filterBySNPFeatures(finalArray, "characteristic.")
    filterBySNPFeatures(dictSnpExclusivosDeGrupoNomGrupo, "exclusive.")
    filterBySNPFeatures(dFinalSnp3Grupos, "3grupos.")
    write_Out()


def write_Out():
    outFile = open("SNPsANDsamples.out", "w")
    outFile.writelines(aSnpWithSamples[0][0] + "\t" + aSnpWithSamples[0][1] + "\n")
    for ij in xrange(1, len(aSnpWithSamples)):
        outFile.writelines(aSnpWithSamples[ij][0] + "\t" + "\t".join(aSnpWithSamples[ij][1]) + "\n")
    outFile.close()

    write_dict("SNPscaracteristicosPorGrupo", finalArray)
    write_dict("SNPsexclusivosDeGrupo", dictSnpExclusivosDeGrupoNomGrupo)
    write_dict("SNPsEn3GruposEnteros", dFinalSnp3Grupos)

def findSNPsByGroups():
    grupos = []
    tempNewGroup = []
    isFirstTime = True;
    # extraer nombres de grupos #
    for k in xrange(0, len(groupsLines)):
        trimmedgroup = groupsLines[k].rstrip('\r\n')
        if (groupsLines[k][0] == ">"):
            if (not isFirstTime):
                grupos.append(tempNewGroup)
            else:
                isFirstTime = False;
            tempNewGroup = []
            tempNewGroup.append(trimmedgroup);
        else:
            tempNewGroup.append(trimmedgroup);
        if (k == len(groupsLines) - 1):
            grupos.append(tempNewGroup)
    
    # aSnpCaracteristicosDeGrupo: en todo un grupo en su totalidad pero no en todo otro grupo
    # aSnpComunGrupos: todos los comunes, sin distincion de en donde estan
    # dictSnpExclusivosDeGrupoNomGrupo: en todo un grupo unicamente y en ningun otra cepa fuera de el
    global dictSnpExclusivosDeGrupoNomGrupo, aSnpExclusivosDeGrupo, arrayFilteredSNPs, aSnpComunGrupos
    global aSnpCaracteristicosDeGrupo
    snpsUtilizados = []
    snpsUtilizadosExclus = []
    aSnpEnGruposEnteros = []
    # Ejemplo:
    # ['4344189-G-T', ['SRR1173284', 'SRR1173725'], ['synonymous_variant', 'LOW', 'Mb3953c', 'Mb3953c', 'Virulence, detocification, adaptation']],
    for y, snp in enumerate(aSnpWithSamples):
        samplesEnLineaSNP = snp[1] ## por SNP
        ##### PARA ENCONTRAR LA CATEGORIA 1: EXCLUSIVOS DE GRUPO
        for z, grups in enumerate(grupos):
            lineaGrupo = grups[1:]
            if (len(samplesEnLineaSNP) == len(lineaGrupo)): ## Los grupos dados en input
                identicos = True
                for i, item in enumerate(samplesEnLineaSNP): ## Por cepa en SNP
                    if (item not in lineaGrupo):
                        identicos = False
                        break
                if (identicos):
                    aSnpComunGrupos.append([grups[0], snp[0], snp[1], snp[2]])
                    if (snp[0] in snpsUtilizadosExclus):
                        ind = snpsUtilizadosExclus.index(snp[0])
                        del snpsUtilizadosExclus[ind] ## al haber un id de snp repetido, tengo que eliminar el que ya habia agregado antes
                    else:
                        snpsUtilizadosExclus.append(snp[0])

        ## PARA ENCONTRAR LA CATEGORIA 2: CARACTERISTICOS DE GRUPO
        ## iguales en tamanio pero diferentes en contenido o diferentes en tamanio
        for z, grups in enumerate(grupos): ##grupos de input
            lineaGrupo = grups[1:]
            identicos = True
            for c, cepaDeGrupo in enumerate(lineaGrupo): ## chequear q cada cepa del grupo esta en la linea de SNP/grupos. Sin importar que haya otras cepas
                if (cepaDeGrupo not in samplesEnLineaSNP):
                    identicos = False
                    break
            if(identicos):
                aSnpEnGruposEnteros.append([snp[0], grups, snp[1], snp[2]]) #snpID, grupo y cepas, samplesWSnp, snpValue

    snpsEliminadosComunes = []
    snps3Grupos = []
    cantGrupos = 1
    for s, snpgroup in enumerate(aSnpEnGruposEnteros):
        if (snpgroup[0] in snpsUtilizados):
            ind = snpsUtilizados.index(snpgroup[0])
            snpsEliminadosComunes.append(snpsUtilizados[ind])
            snps3Grupos.append(snpsUtilizados[ind])
            cantGrupos += 1
            del snpsUtilizados[ind] ## al haber un id de snp repetido, tengo que eliminar el que ya habia agregado antes
        elif(snpgroup[0] not in snpsEliminadosComunes):
            snpsUtilizados.append(snpgroup[0])
        elif(snpgroup[0] in snps3Grupos and cantGrupos < 3):
            print("snp2groups de 2 o 3")
            cantGrupos += 1
        elif(snpgroup[0] in snps3Grupos and cantGrupos >= 3):
            print("snp2groups de mas de 2 o 3")
            cantGrupos = 1
            print(snpgroup[0] + "\t" + snpgroup[1][0])
            ind = snps3Grupos.index(snpgroup[0])
            del snps3Grupos[ind]

    ##snps que aparecen en 3 grupos enteros, para los linajes que no tienen snps caracteristicos
    aFinalSnp3Grupos = []
    for s, snp in enumerate(snps3Grupos):
        for i, line in enumerate(aSnpEnGruposEnteros):
            if (snp == line[0]):
                aFinalSnp3Grupos.append(line)

    global dFinalSnp3Grupos
    dFinalSnp3Grupos = {}
    for linea in aFinalSnp3Grupos: #snpID, grupo y cepas, samplesWSnp, snpValue
        tempGroup = linea[1][0]
        if (tempGroup not in dFinalSnp3Grupos):
            dFinalSnp3Grupos[tempGroup] = []
        dFinalSnp3Grupos[tempGroup].append([linea[0], linea[3]])

    # print("\n\nmuestro caracteristicos\n") ## los caracteristicos CONTIENEN a los Exclusivos
    for s, snp in enumerate(snpsUtilizados):
        for i, line in enumerate(aSnpEnGruposEnteros):
            if (snp == line[0]):
                aSnpCaracteristicosDeGrupo.append(line)
                #print([line[0], line[1][0], line[3]])
                #print(line[3])

    # print("\n\nmuestro exclusivos\n")
    for j, comun in enumerate(aSnpComunGrupos):
        if (comun[1] in snpsUtilizados): ## es decir paso el filtro de estar en un solo grupo
            if (comun[0] not in dictSnpExclusivosDeGrupoNomGrupo):
                dictSnpExclusivosDeGrupoNomGrupo[comun[0]] = []
            dictSnpExclusivosDeGrupoNomGrupo[comun[0]].append([comun[1], comun[3]])

    makeVCFQuestionMark("exclusive_", dictSnpExclusivosDeGrupoNomGrupo)

    currentGroup = ""
    global finalArray
    tempArray = []
    finalArray = {}
    for linea in aSnpCaracteristicosDeGrupo: #snpID, grupo y cepas, samplesWSnp, snpValue
        tempGroup = linea[1][0]
        if (tempGroup not in finalArray):
            finalArray[tempGroup] = []
        finalArray[tempGroup].append([linea[0], linea[3]])
        #{"grupo1" : [[snp12323, "caracteristicas de snp"],[[snp12dfdf323, "diferentes caracteristicas"]]}

    makeVCFQuestionMark("characteristic_", finalArray)


def makeVCFQuestionMark(prefix, inArray):
    #snps = [i for i in finalArray]
    finalArrayGroups = inArray.keys()
    snps = [value[0] for key in finalArrayGroups for value in inArray[key]]

    outFilevcf = open(prefix + "snps.vcf", "w")
    #print(snps)
    for j in xrange(0, len(vcfLines)):
        if (vcfLines[j][0] == "#"):
            outFilevcf.writelines(vcfLines[j])
        else:
            noNewLine = vcfLines[j][:-1] ## delete \n newline
            aLineTemp = noNewLine.split('\t') ## temporary current line
            snpID = aLineTemp[1] + '-' + aLineTemp[3] + '-' + aLineTemp[4] # POS REF ALT
            if (snpID in snps):
                outFilevcf.writelines(vcfLines[j])

    outFilevcf.close()

def setGeneAndFunctionalCategory(info, booleano):
    # ANN=T|intergenic_region|MODIFIER|Mb0049c-Mb0050|Mb0049c-Mb0050|intergenic_region|Mb0049c-Mb0050|||n.52756C>T||||||
    # Siempre son 15 "|"
    # INFO field [7]
    aInfo = info.split(";")
    aInfoANN = [s for s in aInfo if "ANN=" in s]
    if (booleano):
        print(aInfoANN)
    aSplitInfoANN = aInfoANN[0].split("|")
    tipodevariante = aSplitInfoANN[1]
    impacto = aSplitInfoANN[2]
    geneName = aSplitInfoANN[3] 
    geneID = aSplitInfoANN[4]

    returnInfo = []
    for i, name in enumerate(cellWallNames):
        if (geneName == name or geneID == name):
            returnInfo.append("Cell wall and cell processes")
            break
    for i, name in enumerate(consHypoNames):
        if (geneName == name or geneID == name):
            returnInfo.append("Conserved hypotheticals")
            break
    for i, name in enumerate(infoPathNames):
        if (geneName == name or geneID == name):
            returnInfo.append("Information pathways")
            break
    for i, name in enumerate(insertioNames):
        if (geneName == name or geneID == name):
            returnInfo.append("Insertion sequences and phages")
            break
    for i, name in enumerate(intMetabNames):
        if (geneName == name or geneID == name):
            returnInfo.append("Intermediary metabolism and respiration")
            break
    for i, name in enumerate(lipidMetNames):
        if (geneName == name or geneID == name):
            returnInfo.append("Lipid metabolism")
            break
    for i, name in enumerate(PEandPPENames):
        if (geneName == name or geneID == name):
            returnInfo.append("PE-PPE")
            break
    for i, name in enumerate(regulProNames):
        if (geneName == name or geneID == name):
            returnInfo.append("Regulatory proteins")
            break
    for i, name in enumerate(virulencNames):
        if (geneName == name or geneID == name):
            returnInfo.append("Virulence, detocification, adaptation")
            break
    if (len(returnInfo) <= 0): ## else agrega None en su lugar.
        returnInfo = ["None"]
    returnArray = aSplitInfoANN[1:5]
    returnArray.append(returnInfo[0])
    # print(returnArray)
    return returnArray
    
def parseFunctionalCategories():
    cellWall = open("BoviList_cellwallandcellprocesses.txt", "r")
    consHypo = open("BoviList_conserved-hypotheticals.txt", "r")
    infoPath = open("BoviList_information-pathways.txt", "r")
    insertio = open("BoviList_insertion-seqs-and-phages.txt", "r")
    intMetab = open("BoviList_intermediary-metabolism-and-respiration.txt", "r")
    lipidMet = open("BoviList_lipid-metabolism.txt", "r")
    PEandPPE = open("BoviList_PE-PPE.txt", "r")
    regulPro = open("BoviList_regulatory-proteins.txt", "r")
    virulenc = open("BoviList_virulence-detoxification-adaptation.txt", "r")

    global cellWallLines, consHypoLines, infoPathLines, insertioLines, intMetabLines, lipidMetLines, PEandPPELines, regulProLines, virulencLines, cellWallNames, consHypoNames, infoPathNames, insertioNames, intMetabNames, lipidMetNames, PEandPPENames, regulProLines, virulencNames

    cellWallLines = cellWall.readlines()
    for i, name in enumerate(cellWallLines):
        if (i != 0):
            tempName = name.split("\t")[0]
            cellWallNames.append(tempName)

    consHypoLines = consHypo.readlines()
    for i, name in enumerate(consHypoLines):
        if (i != 0):
            tempName = name.split("\t")[0]
            consHypoNames.append(tempName)

    infoPathLines = infoPath.readlines()
    for i, name in enumerate(infoPathLines):
        if (i != 0):
            tempName = name.split("\t")[0]
            infoPathNames.append(tempName)

    insertioLines = insertio.readlines()
    for i, name in enumerate(insertioLines):
            if (i != 0):
                tempName = name.split("\t")[0]
                insertioNames.append(tempName)

    intMetabLines = intMetab.readlines()
    for i, name in enumerate(intMetabLines):
            if (i != 0):
                tempName = name.split("\t")[0]
                intMetabNames.append(tempName)

    lipidMetLines = lipidMet.readlines()
    for i, name in enumerate(lipidMetLines):
            if (i != 0):
                tempName = name.split("\t")[0]
                lipidMetNames.append(tempName)

    PEandPPELines = PEandPPE.readlines()
    for i, name in enumerate(PEandPPELines):
            if (i != 0):
                tempName = name.split("\t")[0]
                PEandPPENames.append(tempName)

    regulProLines = regulPro.readlines()
    for i, name in enumerate(regulProLines):
            if (i != 0):
                tempName = name.split("\t")[0]
                regulProNames.append(tempName)

    virulencLines = virulenc.readlines() ## primer item [0] tiene el header
    for i, name in enumerate(virulencLines):
            if (i != 0):
                tempName = name.split("\t")[0]
                virulencNames.append(tempName)

    # print("cellwall ---")
    # print(cellWallNames[0:3])
    # print("intmetab ---")
    # print(intMetabNames[0:3])

def filterBySNPFeatures(inDict, prefix):
    functionallyFilteredArray = {}
    finalArrayGroups = inDict.keys()

    for key in finalArrayGroups:
        for value in inDict[key]:
            # if (tipodevariante == "synonymous_variant"):
            ## una vez que tengo SNP sinonimos, veo si el gen
            ## es esencial o no.
            if ("synonymous_variant" in value[1]):
                if (key not in functionallyFilteredArray):
                    functionallyFilteredArray[key] = []
                functionallyFilteredArray[key].append(value) 

    #print(functionallyFilteredArray)

    makeVCFQuestionMark(prefix + "filtered_", functionallyFilteredArray)
    write_dict(prefix + "filtered", functionallyFilteredArray)

def write_dict(namefile, inDict):
    outFile = open(namefile + ".out", "w")
    groups = inDict.keys()
    groups.sort()
    #print(finalArray)
    for key in inDict:
        outFile.writelines(key + "\n")
        for value in inDict[key]:
            outFile.writelines(value[0] + "\t" + "\t".join(value[1]) + "\n")
    outFile.close()

setup()


