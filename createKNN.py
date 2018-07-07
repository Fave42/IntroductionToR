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
        # print(dataDict[wordLeft])
    counter = 0
    print("\t\tCalculating the cosine scores...")
    for wordLeft in wordList:
        wordLeftLmi = dataDict[wordLeft][12]
        cosineSum = 0
        cosineList = []
        for wordRight in wordList:
            if (wordLeft != wordRight):
                wordRightLmi = dataDict[wordRight][12]

                # cosineSum += CalculateCosine.calculate(wordLeftLmi, wordRightLmi)
                dataDict[wordLeft][13].append(float(CalculateCosine.calculate(wordLeftLmi, wordRightLmi)))

        windowListSorted = sorted(dataDict[wordLeft][13], reverse=True)
        windowListSorted100 = windowListSorted[:vectorLength]
        lmiSumAvg = sum(windowListSorted100) / vectorLength

        dataDict[wordLeft].append(lmiSumAvg)

        del dataDict[wordLeft][12]  # Delete LMI-score list
        del dataDict[wordLeft][12]  # Delete sorted cosine list

        print("\t\t", counter)
        counter += 1

    return dataDict