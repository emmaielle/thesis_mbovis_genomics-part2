# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 15:34:12 2016
@author: mlasserre
"""
## Version: 2.0
##TODO: Agregar opcion verbose

import sys, argparse
import pdb
from operator import itemgetter
from argparse import RawTextHelpFormatter
import itertools
import multiprocessing

parser = argparse.ArgumentParser(description="Parse multiple RD.out file to obtain regular RD IDs.\n\nOutputs: \n- input.unidosMenor_100.out \n\
    (Original gaps parsed to join together when the diference in position is 100 pb or less (size 1 + diff + size 2)). Saved in each file's location folder", formatter_class=RawTextHelpFormatter)
parser.add_argument(dest="inputFiles", type=str, nargs=1, metavar="i", help="config file with the path locations of each RD.out files to analyze")
parser.add_argument(dest="len", type=str, nargs=1, default=75, metavar="l", help="Length of the smallest desired RD (default 75)")
# ./ERR017792/bedtools_RD/RDs01.out

filesLocation = []
length = 500
aRD_Storage = []
aGaps_Storage = []
bedFileLines = []
currentLine = 0
maxLine = 0
arrayRDinputSize_WithID = []
minDiffGap = 100 ## diferencia utilizada para unir o no dos gaps 
arrayTempBiggerThanX = []

def setup():
    if len(sys.argv)== 1:
        parser.print_help()
        sys.exit(1)
    
    arguments = parser.parse_args()
    inputFile = arguments.inputFiles[0]
    
    global length, bedOut, currentLine, arrayRDinputSize_WithID, arrayTempBiggerThanX
    length = arguments.len[0]
            
    inputF = open(inputFile, "r")
    filesLocation = inputF.readlines()
    for x in range (0, len(filesLocation)):
        parseBedtoolsOutput(filesLocation[x][:-1])
        currentLine = 0
    
    for i in arrayTempBiggerThanX:
        for j, jotaCol in enumerate(i):
            if (j == 0):
                jotaCol = int(jotaCol)
                i[j] = jotaCol

    arrayTempBiggerThanX = sorted(arrayTempBiggerThanX, key=itemgetter(0)) ## ordeno por inicio de gaps entre todas las cepas
    for i in arrayTempBiggerThanX:
        print i
    finalRDs = searchForCommonRDs(arrayTempBiggerThanX)
    writeRDFull(finalRDs)

# Esto funciona para cada archivo
def parseBedtoolsOutput(file):
    # por cada linea de RD.out, guardo las lineas con tamanos mayores a 500pb.
    # Miro linea anterior y siguiente a i para ver si la posicion de ambos es muy cercana a \
    # la posiion en i. Si pos(i -1 || i + 1) - (-) pos i < 100pb, 
    # uno todo el gap en un unico RD que tiene tamano = tamano en pos i + tamano en pos (i +- 1) + diferencia entre 
    # posicion i e i +- 1 correspondiente.
    # Les asigno un ID unico a cada uno "RD{POS}".
    # guardo en un nuevo archivo.
    bedFile = open(file, "r")
    fileNoExtension = file.split('.out')[0]
    strain = file.split("/")[1] ## strain name
    outFileWrite = open(fileNoExtension + ".unidosMenor_" + str(minDiffGap) + ".out" , "w")
    global bedFileLines, aRD_Storage, maxLine, currentLine, arrayRDinputSize_WithID
    bedFileLines = bedFile.readlines()
    aRD_Storage.append(file) ## array que se guarda por archivo separado
    aRD_Storage.append("")
    
    i = 2
    while i < len(bedFileLines):
        linea = bedFileLines[i]
        splitActual = linea.split('\t')
        # mientras no sea el ultimo
        if (i != len(bedFileLines) - 1):
            ultimoEncontradoEnRow = calculaTamanoFinalREC(splitActual, i) ## es el tamano final
            if (i == currentLine):
                tamanoUnido = ultimoEncontradoEnRow + int(splitActual[2]) ## agrego el tamano de la primera linea
                if (maxLine > currentLine):
                    currentLine = maxLine
                i = currentLine ### me salteo todas las lineas que ya use
            else: 
                tamanoUnido = ultimoEncontradoEnRow
            lineaAGuardar = splitActual[0] + "\t" + bedFileLines[i].split('\t')[1] + "\t" + str(tamanoUnido) ## comienzo, final unido, tamano total
            aRD_Storage.append(lineaAGuardar) 
            writeRDstorage(outFileWrite, lineaAGuardar)
            if (tamanoUnido >= int(length)):
                arrayTempBiggerThanX.append([splitActual[0], bedFileLines[i].split('\t')[1], str(tamanoUnido), strain])
        i += 1
    maxLine = 0
    outFileWrite.close()

def calculaTamanoFinalREC(splitLinea, n):
    # print(":::::::::::::::: LINEA "+ str(n) + "::::::::::::::::")
    # si tiene dos lineas consecutivas con diferencia de 100 o menos pb
    # calculo el tamano entre ambas
    if (len(bedFileLines) > (n + 1)):
        lineaSiguiente = bedFileLines[n+1]
        splitSiguiente = lineaSiguiente.split('\t')
        startSiguente = splitSiguiente[0]
        endSiguente = splitSiguiente[1]
        tamanoSiguiente = splitSiguiente[2]
        global currentLine, maxLine
        #diferencia de actual con siguiente es 100 o menos
        if (int(startSiguente) - int(splitLinea[1]) <= minDiffGap): # splitLinea[1] = endActual
            tamano = int(tamanoSiguiente) + (int(startSiguente) - int(splitLinea[1]))
            if (len(bedFileLines) > n + 1):
                llamadaAREC = calculaTamanoFinalREC(bedFileLines[n+1].split('\t'), n+1)
            if (currentLine == n + 1):
                tamano = tamano + int(llamadaAREC)
            currentLine = n
            return tamano
        else:
            if (n > maxLine):
                maxLine = n
            return int(splitLinea[2]) ## tamano de la linea
    else:
        if (n > maxLine):
                maxLine = n
        return int(splitLinea[2]) ## tamano de la linea

def readRDstorage():
    for i, line in enumerate(aRD_Storage):
        print (line)

def writeRDstorage(file, line):
    file.writelines(line + "\n")     

def writeRDFull(array):
    print("write...")
    file1 = open("RDsets.byStrain.output" , "w")
    file2 = open("RDsets.byRD.output", "w")
    for i, arr in enumerate(array):
        print(arr[2])
        file2.writelines(arr[0] + "\t" + arr[1] + "\t" + str(len(arr[2])) + "\t" + "\t".join(arr[2]) + "\n")
        for j, cepa in enumerate(arr[2]):
            file1.writelines(arr[1] + "\t" + cepa + "\n")
        print(len(arr[2]))
        print (arr) 
    file1.close()
    file2.close()

def searchForCommonRDs(array):
    # nested loop linea vs all remaining
    i = 0
    finalRD_strain = []
    nuevoI_onFindRDcommon = 0 ## para ir modificando el i a medida que se encuentran bloques solapados
    solapantesPotenciales = []
    arrayToModify = array[:]
    for i, linea in enumerate(array):
        if (linea in arrayToModify):
            ## si la lista es len == 0 es porque pasa por primera vez por este i (porque sino al menos tiene len == 1)
            if (len(solapantesPotenciales) == 0):
                solapantesPotenciales = obtenerSolapantes(array, i, arrayToModify)                            
            ## voy a revisar cada uno de los solapantes
            line = array[solapantesPotenciales[0]]
            inicioSolapado = int(line[0]) ## al principio vale lo mismo que la linea madre antes de entrar al nuevo loop
            finSolapado = int(line[1])
            tamanoSolapado = int(line[2])
            indiceEnArray = 0
            tempCoordenadasToSave = [inicioSolapado, finSolapado, tamanoSolapado, indiceEnArray]
            maxIndexFromBlock = -1

            solapanteI = 0
            while solapanteI < len(solapantesPotenciales): 
                if (array[solapantesPotenciales[solapanteI]] in arrayToModify):
                    print("len solapantespotenciales " + str(len(solapantesPotenciales)))
                    print(solapanteI)
                    lineIntern = array[solapantesPotenciales[solapanteI]]
                    inicioIntern = int(lineIntern[0]) 
                    finIntern = int(lineIntern[1])
                    tamanoIntern = int(lineIntern[2])
                    cepaIntern = lineIntern[3]
                    devolverAarrayPadre = []
                    solapanteAceptado = -1
                    if ((tamanoIntern*1.0 / tamanoSolapado) > 0.95 and (tamanoIntern*1.0 / tamanoSolapado) < 1.05):
                        solapanteAceptado = solapanteI
                        if (tempCoordenadasToSave[0] <= inicioIntern and tempCoordenadasToSave[1] <= finIntern and tempCoordenadasToSave[0] < finIntern and tempCoordenadasToSave[1] > inicioIntern):
                            ## fin - inicioInterno
                            #print("A")
                            tamanoSolapado = finSolapado - inicioIntern
                            inicioSolapado = inicioIntern
                            finSolapado = finSolapado ## no cambia
                        elif (tempCoordenadasToSave[0] >= inicioIntern and tempCoordenadasToSave[0] < finIntern and tempCoordenadasToSave[1] > inicioIntern and tempCoordenadasToSave[1] >= finIntern):
                            ## finInterno - inicio
                            #print("B")
                            tamanoSolapado = finIntern - inicioSolapado
                            inicioSolapado = inicioSolapado # no cambia
                            finSolapado = finIntern
                        elif (tempCoordenadasToSave[0] >= inicioIntern and tempCoordenadasToSave[0] < finIntern and tempCoordenadasToSave[1] > inicioIntern and tempCoordenadasToSave[1] <= finIntern):
                            ## tamano total de linea actual (tamano - line[2])
                            #print("C")
                            tamanoSolapado = tamanoSolapado ## no cambia nadaaa
                            inicioSolapado = inicioSolapado
                            finSolapado = finSolapado
                        elif (tempCoordenadasToSave[0] < inicioIntern and tempCoordenadasToSave[1] > finIntern):
                            ## tamano interno de linea sig (tamanoIntern = array[m][2])
                            #print("D")
                            tamanoSolapado = tamanoIntern
                            inicioSolapado = inicioIntern 
                            finSolapado = finIntern
                        elif(tempCoordenadasToSave[0] == inicioIntern and tempCoordenadasToSave[1] == finIntern):
                            #print("E")
                            pass
                        else:
                            pass
                    else:
                        print(array[solapantesPotenciales[solapanteI]])
                        del solapantesPotenciales[solapanteI]
                        solapanteI = solapanteI - 1
                    for li in solapantesPotenciales:
                        if (maxIndexFromBlock < li): ## el indice en array original
                            maxIndexFromBlock = li
                    if (tamanoSolapado >= int(length)):
                        tempCoordenadasToSave = [inicioSolapado, finSolapado, tamanoSolapado, indiceEnArray]
                    else:
                        if (solapanteAceptado == maxIndexFromBlock): #**
                            del solapantesPotenciales[solapanteAceptado] ## me parece que esto no esta bien
                else:
                    print("Ya usado en otra vuelta de solapping bunch y eliminado de arrayToModify")
                    print("--")
                    print(array[solapantesPotenciales[solapanteI]])
                    del solapantesPotenciales[solapanteI]
                solapanteI += 1 
            
        tempCoordenadasToSave = [inicioSolapado, finSolapado, tamanoSolapado, indiceEnArray]
        ## cuando termino de ver todas las permutaciones, voy a tener una que es la mejor.
        ## Entonces la recorro de nuevo para actualizar el porcentaje de cobertura que el solapado tiene con
        ## cada linea analizada. si hay alguna < 1000 bp se elimina
        ## esta diferencia nunca va a poder ser mayor a (solo menor o igual)
        p = 0
        arrayFinalRD_temp = [] ## va a tener las cepas que tienen a este RD
        while p < len(solapantesPotenciales):
            if (tempCoordenadasToSave[2] >= 1000):
                arrayFinalRD_temp.append(array[solapantesPotenciales[p]][3]) ## 3 tiene el ID de la cepa
            p += 1 

        for o in solapantesPotenciales:
            arrayToModify[o] = ''
        solapantesPotenciales = [] ## reset la lista asi solo la crea de nuevo cuando realmente entra a un nuevo i al que no entro antes
        if (len(arrayFinalRD_temp) > 1):
            finalRD_strain.append([str(inicioSolapado) + "_" + str(finSolapado) + "_" + str(tamanoSolapado) + "_RD", "RD" + str(inicioSolapado) + "_" + str(finSolapado), arrayFinalRD_temp]) ### IDRD, [cepas que lo tienen]

    return finalRD_strain

def obtenerSolapantes(inArray, i, inArrayModified):
    ########################################
    ### Lista de bloque de solapantes actual
    solapantesPotenciales = []
    solapantesPotenciales.append(i) # incluye a i
    j = i + 1
    while j < len(inArray):
        inicioIntern = int(inArray[j][0]) 
        fin = int(inArray[i][1])
        if (fin > inicioIntern):
            if (inArray[j] in inArrayModified):
                solapantesPotenciales.append(j)
        else: 
            break
        j += 1
    return solapantesPotenciales

setup()

