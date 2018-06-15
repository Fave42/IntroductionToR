#!/bin/bash

import pickle
from itertools import chain, repeat, islice


# Padding of to few LMI-scores per word
def pad_infinite(iterable, padding=None):
   return chain(iterable, repeat(padding))


def pad(iterable, size, padding=None):
   return islice(pad_infinite(iterable, padding), size)


count51 = 0
count52 = 0
dataDict = {}
lmiDict = {}

dataDict = pickle.load(open("dataDict.pickle", "rb"))

# Ab index 14 (+4) sind die LMI Scores
for key in dataDict:
    # print(key)
    # print(dataDict[key])
    # print(dataDict[key][14])
    # print(dataDict[key][18])

    if (len(dataDict[key]) == 51):
        count51+=1
    elif (len(dataDict[key]) == 52):
        count52+=1

    print(len(dataDict[key]))

    lmiList = []
    lmiList.extend((dataDict[key][14], dataDict[key][18], dataDict[key][22], dataDict[key][26], dataDict[key][30],
                   dataDict[key][34], dataDict[key][38], dataDict[key][42], dataDict[key][46], dataDict[key][50]))
    # print(lmiList)

    lmiDict[key] = lmiList

print(count51)
print(count52)