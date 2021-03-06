# -*- coding: utf-8 -*-
"""
Created on Thu Oct 01 10:38:32 2015

@author: dimitris
"""

def create_table(filename):
    ''' This function takes an file path as input and returns 
    the number of file rows and a matrix with the data included in the file'''
    import csv    
    out = open(filename, 'r')
    data = csv.reader(out, delimiter=';')
    fulltable = [row for row in data]
    # count the rows
    row_count = sum(1 for row in fulltable)
    out.close()
    #print row_count
    return row_count, fulltable