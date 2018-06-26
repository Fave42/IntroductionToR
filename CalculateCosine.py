#!/bin/bash

#
# Calculate the average cosine score for every word and it's k nearest neighbours
#
# Word|Val_N|Val_M|Val_SD|Ar_N|Ar_M|Ar_SD|Con_N|Con_M|Con_SD|length|Cluster|Freq|[W_Context|W_Freq|W_LMI]*10

from scipy import spatial
import numpy as np

def calculate(lmiLeft, lmiRight):
    cosineResult = 0
    try:
        cosineResult = 1 - spatial.distance.cosine(lmiLeft, lmiRight)
    except:
        return 0
    if np.isnan(cosineResult):
        return 0
    else:
        return cosineResult
