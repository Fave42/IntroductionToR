#!/bin/bash

'''
Vorverarbeitung der Daten um mir R keine 15+ GB an RAM zu verbrauchen

Usage: python3 vorverarbeitung.py
--------------------------------------
Norms:
Word 	Valence 			Arousal			Concreteness			Length	Cluster
	N,Samp Size	M, Mean	SD,standard dev.	N	M	SD	N	M	SD		
Abbau	23	2,96	2,03	27	2,48	2,74	19	3,79	2,68	5	1
--------------------------------------

Final Output File:

Word|Val_N|Val_M|Val_SD|Ar_N|Ar_M|Ar_SD|Con_N|Con_M|Con_SD|length|Cluster|Freq|[10 biggest LMI-scores]

'''

import time
import numpy as np
import operator
import codecs
import pickle

# Laptop
# pathNorms = '/home/fabian/Uni-Master/R/Projekt/Data/Norms/Lahl-de/norms_Lahl.csv'
# pathFreq = '/home/fabian/Uni-Master/R/Projekt/Data/Freqs/freqs_lemmas_pos.txt'
# pathWindows = '/home/fabian/Uni-Master/R/Projekt/Data/Windows/decow16-window-2_freqs_lmi.txt'

# PC
pathNorms = 'D:/Uni-Master/R/Projekt/Data/Norms/Lahl-de/norms_Lahl.csv'
pathFreq = 'D:/Uni-Master/R/Projekt/Data/Freqs/freqs_lemmas_pos.txt'
pathWindows = 'D:/Uni-Master/R/Projekt/Data/Windows/decow16-window-2_freqs_lmi.txt'


def createNormsDict(pathNorms):
    print("\tCreating normsDict...")
    normsDict = {}
    # Generate NormsDict
    with open(pathNorms, 'r') as file:
        for _ in range(2):  # Skip first two lines (Headers)
            next(file)

        for line in file:
            tmpList = []
            lineSplit = line.split()

            tmpList.extend((lineSplit[1], lineSplit[2], lineSplit[3], lineSplit[4], lineSplit[5], lineSplit[6],
                           lineSplit[7], lineSplit[8], lineSplit[9], lineSplit[10], lineSplit[11],
                           []))  # Empty list for later index=11

            normsDict[lineSplit[0]] = tmpList

        return normsDict


def processData(normsDict, pathFreq, pathWindows):
    print("\tCreating dataDict...")
    print("\t\tAdding Frequencies and Lemmas...")
    with codecs.open(pathFreq, encoding="utf-8") as file:
        for line in file:
            lineSplit = line.split()
            if (lineSplit[0] in normsDict) and (lineSplit[1] == "NN"):
                normsDict[lineSplit[0]].append(lineSplit[2])  # Frequency

    print("\t\tAdding Distributional Information...")
    with codecs.open(pathWindows, encoding="utf-8") as file:
        # Format: target:::pos    context::pos    frequency    lmi score
        for line in file:
            line = line.replace(":::", "\t")
            lineSplit = line.split()
            # Format: target pos context pos frequency lmi-score
            if (lineSplit[0] in normsDict) and (lineSplit[1] == "NN") and (lineSplit[3] == "NN"):
                tmpList = [lineSplit[2], lineSplit[3], lineSplit[4], lineSplit[5]]
                normsDict[lineSplit[0]][11].append(tmpList)

    print("\t\t\tSorting LMI-Scores...")
    for key in normsDict:
        windowsListSorted = sorted(dataDict[key][11], key=lambda tup: tup[3], reverse=True)
        windowsListSorted10 = windowsListSorted[:10]
        del normsDict[key][11]
        for item in windowsListSorted10:
            for innerItem in item:
                normsDict[key].append(innerItem)

    print("\tCalculating cosine scores...")
    for key in normsDict:
        tmpLMI = normsDict[key][11]


    return normsDict

# Sort the windows data and store it
def storeData(dataDict):
    print("\tWriting Output File...")
    with open('outputFileTest.txt', 'w') as outputFile:
        print("\t\tWriting Header...")
        outputFile.write("Word\tVal_N\tVal_M\tVal_SD\tAr_N\tAr_M\tAr_SD\tCon_N\tCon_M\tCon_SD\tlength\tCluster\tFreq\t"
                         + "W_Context\tW_Pos\tW_Freq\tW_LMI\tW_Context\tW_Pos\tW_Freq\tW_LMI\tW_Context\tW_Pos\tW_Freq\tW_LMI\t"
                         + "W_Context\tW_Pos\tW_Freq\tW_LMI\tW_Context\tW_Pos\tW_Freq\tW_LMI\tW_Context\tW_Pos\tW_Freq\tW_LMI\t"
                         + "W_Context\tW_Pos\tW_Freq\tW_LMI\tW_Context\tW_Pos\tW_Freq\tW_LMI\tW_Context\tW_Pos\tW_Freq\tW_LMI\t"
                         + "W_Context\tW_Pos\tW_Freq\tW_LMI\n")

        print("\t\tWriting Data...")
        for key in dataDict:
            tmpString = "\t".join(dataDict[key])
            outputFile.write(key + "\t" + tmpString + "\n")

    return dataDict


dataDict = storeData(processData(createNormsDict(pathNorms), pathFreq, pathWindows))

# Dumping dataDict
# print("\tDumping dataDict as .pickle...")
# pickle.dump(dataDict, open("dataDict.pickel", "wb"))
