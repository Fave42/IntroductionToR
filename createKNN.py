#!/bin/bash

'''
Create the KNN for every word-pair and calculate the avergae cosine score
'''

import CalculateCosine
import numpy as np

def run(dataDict, wordPairDict, wordList, vectorLength):
    print("\t\tCreating the vectors...")
    for wordLeft in wordList:
        for wordRight in wordList:
            if (wordLeft != wordRight):
                wordPair = wordLeft+"_"+wordRight
                if (wordPair in wordPairDict):
                    dataDict[wordLeft][12].append(float(wordPairDict[wordPair]))
                else:
                    dataDict[wordLeft][12].append(0.0)

    print("\t\tCalculating the cosine scores...")
    for wordLeft in wordList:
        wordLeftLmi = dataDict[wordLeft][12]
        cosineSum = 0
        for wordRight in wordList:
            wordRightLmi = dataDict[wordRight][12]

            cosineSum += CalculateCosine.calculate(wordLeftLmi, wordRightLmi)
            # if np.isnan(cosineSum):
            #     print(wordLeftLmi)
            #     print(wordRightLmi)
            #     exit()
        avgCosine = (cosineSum / 2653.0)
        dataDict[wordLeft][12] = avgCosine

        print(wordLeft, avgCosine)

    for key in dataDict:
        print(key, dataDict[key])
        print(len(dataDict[key][12]))
        break