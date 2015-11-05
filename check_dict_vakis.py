# -*- coding: utf-8 -*-
"""
Created on Thu Nov 05 15:09:18 2015

@author: dimitris
"""
k = 1.
l = 2.
def calculate(params):
    rparams = {}
    for key, val in params.items:
        print key
        if key == 'a':
            val = val * k
            rparams[key] = val
        if key == 'b':
            val = val * l
            rparams[key] = val
    return rparams
    
    
    
myDict = dict()
myDict['a'] = 54.
myDict['b'] = 21.
myDict['c'] = 5.

