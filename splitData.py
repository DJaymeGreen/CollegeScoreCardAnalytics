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
        oneNum = 0
        twoNum = 0
        oneCluster = list()
        twoCluster = list()
        tempList = list()
        for row in reader:
            try:
                if(float(row[colNum-1]) < 38000):
                    oneCluster.append(list())
                    clusterOne = True
                else:
                    twoCluster.append(list())
                    clusterOne = False
                for val in range(0,colNum):
                    try:
                        if(val == 0):
                            goodRow = True
                            tempList = list()
                        if(goodRow):
                            tempList.append(float(row[val]))
                            if(val == colNum-1):
                                if(clusterOne):
                                    oneCluster[oneNum] = tempList
                                    oneNum += 1
                                else:
                                    twoCluster[twoNum] = tempList
                                    twoNum += 1
                                tempList = list()
                    except:
                        goodRow = False
                    
            except ValueError:
                #listOfData[rowNum].append(row[val])
                skipRows.add(rowNum)
            rowNum += 1

        # Delete the rows where there is a String
        #skipRows = sorted(skipRows)
        #for rowRemove in reversed(skipRows):
        #    listOfData.pop(rowRemove)

    return oneCluster,twoCluster

oneCluster,twoCluster = openCSVFile('DataRound3.csv')

"""
Prints out of the clusters into an Excel file
"""
def toExcelFile(cluster, description):
    #newNormal = transposeDataset(normal)
    with open(description + '.csv', 'w', newline='') as csvfile:
        #spamwriter = csv.writer(csvfile, dialect='excel', delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        #for row in range(0,totalNumberOfVals-1):
         #   spamwriter.writerow(newNormal[row].encode("utf-8"))
         writer = csv.writer(csvfile)
         writer.writerows(cluster)

toExcelFile(oneCluster,"clusterA")
toExcelFile(twoCluster,"clusterB")