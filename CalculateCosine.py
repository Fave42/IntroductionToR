#!/bin/bash

#
# Calculate the average cosine score for every word and it's k nearest neighbours
#
# Word|Val_N|Val_M|Val_SD|Ar_N|Ar_M|Ar_SD|Con_N|Con_M|Con_SD|length|Cluster|Freq|[W_Context|W_Freq|W_LMI]*10

import pickle
from scipy import spatial

def calculate(dataDict):
    # dataDict = {}
    # dataDict = pickle.load(open("dataDict.pickle", "rb"))

    # Ab index 14 (+4) sind die LMI Scores
    for key in dataDict:
        neighbourList = []
        neighbourList.extend((dataDict[key][12], dataDict[key][15], dataDict[key][18], dataDict[key][21], dataDict[key][24],
                              dataDict[key][27], dataDict[key][30], dataDict[key][33], dataDict[key][36], dataDict[key][39]))

        currentWordLmiList = []
        currentWordLmiList.extend((float(dataDict[key][14]), float(dataDict[key][17]), float(dataDict[key][20]),
                                   float(dataDict[key][23]), float(dataDict[key][26]), float(dataDict[key][29]),
                                   float(dataDict[key][32]), float(dataDict[key][35]), float(dataDict[key][38]),
                                   float(dataDict[key][41])))

        cosineAverage = 0
        cosineSum = 0

        for word in neighbourList:
            if ("NA" not in neighbourList): # Discard every word with less than 10 nearest neighbours

                tmpLmiList = []
                tmpLmiList.extend((float(dataDict[word][14]), float(dataDict[word][17]), float(dataDict[word][20]),
                                   float(dataDict[word][23]), float(dataDict[word][26]), float(dataDict[word][29]),
                                   float(dataDict[word][32]), float(dataDict[word][35]), float(dataDict[word][38]),
                                   float(dataDict[word][41])))

                cosineResult = 1 - spatial.distance.cosine(currentWordLmiList, tmpLmiList)

                cosineSum = cosineSum + cosineResult
            else:
                break

        cosineAverage = cosineSum / 10

        dataDict[key].append(cosineAverage)

    return dataDict
    # Test output
    # for key in dataDict:
    #     print(key, dataDict[key])
