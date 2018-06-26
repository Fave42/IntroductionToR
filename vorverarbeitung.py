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

Word|Val_N|Val_M|Val_SD|Ar_N|Ar_M|Ar_SD|Con_N|Con_M|Con_SD|length|Cluster|Freq|[W_Context|W_Freq|W_LMI]*10

'''


# import codecs
import pickle
# from itertools import chain, repeat, islice
# import CalculateCosine as cosine
import createKNN

vectorLength = 100

# Laptop
pathNorms = '/home/fabian/Uni-Master/R/Projekt/Data/Norms/Lahl-de/norms_Lahl.csv'
pathFreq = '/home/fabian/Uni-Master/R/Projekt/Data/Freqs/freqs_lemmas_pos.txt'
pathWindows = '/home/fabian/Uni-Master/R/Projekt/Data/Windows/windowShort.txt'

# PC
# pathNorms = 'D:/Uni-Master/R/Projekt/Data/Norms/Lahl-de/norms_Lahl.csv'
# pathFreq = 'D:/Uni-Master/R/Projekt/Data/Freqs/freqs_lemmas_pos.txt'
# pathWindows = 'D:/Uni-Master/R/Projekt/Data/Windows/windowShort.txt'

# Padding of to few LMI-scores per word
# def pad_infinite(iterable, padding=None):
#     return chain(iterable, repeat(padding))
#
#
# def pad(iterable, size, padding=None):
#     return islice(pad_infinite(iterable, padding), size)


def createNormsDict(pathNorms):
    print("\tCreating normsDict and Adding frequency=1 for every word...")
    normsDict = {}
    wordList = []
    # Generate NormsDict
    with open(pathNorms, 'r') as file:
        for _ in range(2):  # Skip first two lines (Headers)
            next(file)

        for line in file:
            tmpList = []
            lineSplit = line.split()

            tmpList.extend((lineSplit[1], lineSplit[2], lineSplit[3], lineSplit[4], lineSplit[5], lineSplit[6],
                           lineSplit[7], lineSplit[8], lineSplit[9], lineSplit[10], lineSplit[11],
                            1,  # Set every Frequency to 1, index=11
                           [],    # Empty list for lmi, index=12
                            []))    # Empty list for tmp cosineScore

            wordList.append(lineSplit[0])
            normsDict[lineSplit[0]] = tmpList

        return normsDict, wordList


def processData(normsDict, pathFreq, pathWindows, wordList):
    print("\tCreating dataDict...")
    print("\t\tAdding Frequencies...")
    # with codecs.open(pathFreq, encoding="utf-8") as file:
    with open(pathFreq) as file:
        for line in file:
            lineSplit = line.split()
            if (lineSplit[0] in normsDict) and (lineSplit[1] == "NN"):
                # Overwrite Frequency if available
                normsDict[lineSplit[0]][11] = lineSplit[2]  # Frequency

    print("\t\tAdding Distributional Information...")
    # with codecs.open(pathWindows, encoding="utf-8") as file:
    with open(pathWindows) as file:
        # Format: target:::pos    context::pos    frequency    lmi score
        wordPairDict = {}
        for line in file:
            line = line.replace(":::", "\t")
            lineSplit = line.split()
            # Format: target pos context pos frequency lmi-score
            # Only add distr. information if it's a NN
            if (lineSplit[0] in normsDict):
                # tmpList = [lineSplit[2], lineSplit[4], lineSplit[5]]

                wordPairDict[lineSplit[0]+"_"+lineSplit[2]] = lineSplit[5]

                # try:
                #     normsDict[lineSplit[0]][12].append(tmpList)
                # except:
                #     print("Something has gone wrong while appending the tmpList!")
                #     print("tmpList:", tmpList)
                #     print("normsDict[lineSplit[0]][12]:", normsDict[lineSplit[0]][12])
                #     break

    # print("\t\t\tSorting and padding the LMI-Scores...")
    # wordList = []
    # for key in normsDict:
    #     wordList.append(key)
    #
    #     windowsListSorted = sorted(normsDict[key][12], key=lambda tup: float(tup[2]), reverse=True)
    #     windowsListSorted100 = windowsListSorted[:vectorLength]
    #     del normsDict[key][12]
    #
    #     # Pad the sorted list to 10 items
    #     # windowsListSorted10Padded = list(pad(windowsListSorted10, 10, ["NA", 0, 0]))
    #     windowsListSorted10Padded = windowsListSorted100
    #     # print(windowsListSorted10Padded)
    #     try:
    #         for item in windowsListSorted10Padded:
    #             # print(item)
    #             for innerItem in item:
    #                 # print(innerItem)
    #                 normsDict[key].append(innerItem)
    #     except:
    #         print("Something went terribly wrong while appending or iterating!")
    #         print("\t", windowsListSorted10Padded)
    #         break

    print("\tCreating the KNN's...")
    tmpDict = {}
    tmpDict = createKNN.run(normsDict, wordPairDict, wordList, vectorLength)

    return tmpDict

# Store the data as tsv
def storeData(dataDict):
    print("\tWriting Output File...")
    with open('outputFile.txt', 'w') as outputFile:
        print("\t\tWriting Header...")
        outputFile.write("Word\tVal_N\tVal_M\tVal_SD\tAr_N\tAr_M\tAr_SD\tCon_N\tCon_M\tCon_SD\tlength\tCluster\tFreq\t"
                         + "\tAvrg_Cosine\n")

        print("\t\tWriting Data...")
        for key in dataDict:
            # print(key)
            # print(dataDict[key])
            tmpString = ""
            try:
                for item in dataDict[key]:
                    tmpString = tmpString + "\t" + str(item)
                # print(tmpString)
            except:
                print("Someting went terribly wrong while joining the data!")
                print(dataDict[key])
                break

            outputFile.write(key + tmpString + "\n")

    return dataDict

normsDict = {}
wordList = []
normsDict, wordList = createNormsDict(pathNorms)

dataDict = {}
dataDict = storeData(processData(normsDict, pathFreq, pathWindows, wordList))

# Dumping dataDict
print("\tDumping dataDict as .pickle...")
pickle.dump(dataDict, open("dataDict.pickle", "wb"))

# Todo: Add commandline parameters
