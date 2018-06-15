#!/bin/bash

import pickle

dataDict = {}
dataDict = pickle.load(open("dataDict.pickle", "rb"))

# Ab index 14 (+3) sind die LMI Scores
for key in dataDict:
    #print(dataDict[key])

    print(dataDict[key])
    #print(dataDict[key][15])
    # if (dataDict[key][42]):
    #     lmiList = []
    #     lmiList.extend((dataDict[key][15], dataDict[key][18], dataDict[key][21], dataDict[key][24], dataDict[key][27],
    #                    dataDict[key][30], dataDict[key][33], dataDict[key][36], dataDict[key][39], dataDict[key][42]))
    #
    # else:
    #     lmiList = []
    #     lmiList.extend((0, 0, 0, 0, 0, 0, 0, 0, 0, 0))

    try:
        lmiList = []
        lmiList.extend((dataDict[key][15], dataDict[key][18], dataDict[key][21], dataDict[key][24], dataDict[key][27],
                       dataDict[key][30], dataDict[key][33], dataDict[key][36], dataDict[key][39], dataDict[key][42]))

    except:
        lmiList = []
        lmiList.extend((0, 0, 0, 0, 0, 0, 0, 0, 0, 0))

    print (lmiList)