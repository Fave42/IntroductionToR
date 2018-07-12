#!/bin/bash

'''
Create the KNN for every word-pair and calculate the avergae cosine score
'''

import CalculateCosine
import numpy as np

def run(dataDict, wordPairDict, wordList, vectorLength):
    print("\t\tCreating the vectors...")
    seenWordsDict = {}

    for wordLeft in wordList:
        for wordRight in wordList:
            if (wordLeft != wordRight):
                wordPair = wordLeft+"_"+wordRight
                if (wordPair in wordPairDict):
                    dataDict[wordLeft][12].append(float(wordPairDict[wordPair]))
                else:
                    dataDict[wordLeft][12].append(0.0)

    counterC = 0
    print("\t\tCalculating the cosine scores...")
    for wordLeft in wordList:
        wordLeftLmi = dataDict[wordLeft][12]
        cosineSum = 0
        cosineList = []
        for wordRight in wordList:
            ignoreIndex = 2654 - (2654 - counterC)

            # if (wordLeft in seenWordsDict) and (seenWordsDict[wordLeft] == wordRight):
            #     dataDict[wordLeft][13][wordList.index(wordRight)].append(float(dataDict[leftTmp][13]))

            if (wordLeft != wordRight):

                wordRightLmi = dataDict[wordRight][12]

                # cosineSum += CalculateCosine.calculate(wordLeftLmi, wordRightLmi)
                dataDict[wordLeft][13].append(float(CalculateCosine.calculate(wordLeftLmi, wordRightLmi)))

            # if (wordRight not in seenWordsDict):
            #     seenWordsDict[wordRight] = wordLeft

        windowListSorted = sorted(dataDict[wordLeft][13], reverse=True)
        windowListSorted100 = windowListSorted[:vectorLength]
        lmiSumAvg = sum(windowListSorted100) / vectorLength

        dataDict[wordLeft].append(lmiSumAvg)

        del dataDict[wordLeft][12]  # Delete LMI-score list
        del dataDict[wordLeft][12]  # Delete sorted cosine list

        print("\t\t", counterC)
        counterC += 1

    return dataDict


"""
               0  1  2  Index
  a  b  c  |   1  2  3
a x  ab ac | 1 x  12 13  n-(n-1) = Index 0 faellt weg
b ba x  bc | 2 21 x  23  n-(n-2) = Index 0,1 faellt weg
c ca cb x  | 3 31 32 x   n-(n-3) = Index 0,1,2 faellt weg

n=3x3, n=2654x2654
c=n=2654

n-(n-1)
n-(n-2)
n-(n-3)
.
.
n-(n-c)
----------
ab, ac, ba, bc, ca, cb
ab, ac, ab, bc, ac, bc
ab, ac, bc

12, 13, 21, 23, 31, 32
12, 13, 12, 23, 13, 23
12, 13, 23
"""