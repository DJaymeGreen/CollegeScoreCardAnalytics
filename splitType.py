"""
Author: D Jayme Green
Date: 4/9/17
K-Means


This program creates a clusters using the given 
Testing data
"""

"""
Csv is used to read in the csv data
Numpy is used to allow floats into Matplotlib
"""
import matplotlib.pyplot as mpl
from mpl_toolkits.mplot3d import Axes3D
import csv
import math
import numpy as np
import sys
import random


"""
Constants are declared below for the program
listOfData holds all of the data given
totalNumberOfVals holds the number of rows there is
numberOfCols holds the number of cols there is
"""
listOfData = list(list())
totalNumberOfVals = 0
numberOfCols = 0
whatCluster = dict()
clusters = list(list())
combinedRows = list()
#euclideanDist = [[]]
#rowsWithClassifier = 0




"""
Reading in the .csv file and putting it into listOfData which
holds all of the rows as lists. It relies on the file to have
a header on the top
"""
def openCSVFile(fileName):
    listOfData = list()
    with open(fileName, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        rowNum = 0
        colNum = len(next(reader))
        #for col in range(0,colNum-1):
         #   listOfData.append(list())
        skipRows = set()
        for row in reader:
            listOfData.append(list())
            for val in range(0,colNum):
                try:
                    listOfData[rowNum].append(float(row[val]))
                except ValueError:
                    listOfData[rowNum].append(row[val])
                    skipRows.add(rowNum)
            rowNum += 1

        # Delete the rows where there is a String
        skipRows = sorted(skipRows)
        for rowRemove in reversed(skipRows):
            listOfData.pop(rowRemove)

    return listOfData, rowNum, colNum

listOfData, totalNumberOfVals, numberOfCols = openCSVFile('typeToSplit.csv')

"""
Splits type into three separate array lists
"""
def splitType():
    public = list()
    private = list()
    forProfit = list()
    for val in listOfData:
        if(val[0] == 1):
            public.append(1)
            private.append(0)
            forProfit.append(0)
        elif(val[0] == 2):
            public.append(0)
            private.append(1)
            forProfit.append(0)
        elif(val[0] == 3):
            public.append(0)
            private.append(0)
            forProfit.append(1)
    #print it all
    for row in range(0,len(public)):
        print(str(public[row]) + " " + str(private[row]) + " " + str(forProfit[row]))

splitType()