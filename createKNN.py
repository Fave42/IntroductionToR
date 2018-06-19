#!/bin/bash

'''
Create the KNN for every word-pair and calculate the avergae cosine score
'''
#
# import CalculateCosine
#
#
# def run(dataDict, wordList, vectorLength):
#     lmiDict = {}
#
#     for wordLeft in wordList:
#         for wordRight in wordList:
#             if (wordLeft != wordRight):
#                 lmiLeft = []
#                 lmiRight = []
#
#                 index = 14
#                 cosineScore = 0
#                 wordPair = wordLeft + "-" + wordRight
#
#                 for i in range(0, vectorLength):
#                     # Index LMI: 14, 17, 20
#                     lmiLeft.append(float(dataDict[wordLeft][index]))
#                     lmiRight.append(float(dataDict[wordRight][index]))
#                     index += 3
#
#                 cosineScore = CalculateCosine.calculate(lmiLeft, lmiRight)
#
#                 lmiDict[wordPair] = cosineScore
#
#     return dataDict


######
# Testing
######
import pickle
import CalculateCosine

dataDict = pickle.load(open("dataDict.pickle", "rb"))

wordList = []
lmiDict = {}
vectorLength = 10

for key in dataDict:
    wordList.append(key)

for wordLeft in wordList:
    for wordRight in wordList:
        if (wordLeft != wordRight):
            lmiLeft = []
            lmiRight = []

            index = 14
            cosineScore = 0
            wordPair = wordLeft+"-"+wordRight

            for i in range(0,vectorLength):
                # Index LMI: 14, 17, 20
                lmiLeft.append(float(dataDict[wordLeft][index]))
                lmiRight.append(float(dataDict[wordRight][index]))
                index += 3

            cosineScore = CalculateCosine.calculate(lmiLeft, lmiRight)
            # if (cosineScore < 0.5):
            #     print(cosineScore)
            # print(lmiLeft)
            # print(lmiRight)

            lmiDict[wordPair] = cosineScore

            # print(lmiLeft)

# print(lmiDict)