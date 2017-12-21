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

listOfData, totalNumberOfVals, numberOfCols = openCSVFile('dpData.csv')

"""
Opens the file with the clusters. Puts the clusters in the right list
"""
def openClusters(fileName):
    listOfClusters = list()
    with open(fileName, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        rowNum = 0
        colNum = len(next(reader))
        for k in range(0,5):
            listOfClusters.append(list())
        for row in reader:
            for val in range(0,colNum):
                if (val == colNum-1):
                    listOfClusters[int(row[val])].append(listOfData[rowNum])
                    listOfClusters[int(row[val])][len(listOfClusters[int(row[val])])-1].append(1763 + int(row[0]))
            rowNum += 1

    clusterNum = 1
    for cluster in listOfClusters:
        print("\n------------ Cluster " + str(clusterNum) + " -----------------------\n")
        print("Number of points: " + str(len(cluster)) + "\n")
        for point in cluster:
            print(point)
        clusterNum += 1

    #Find the averages per cluster's columns
    colNames = ["MaxTemp","MinTemp", "Precip"]
    clusterNum = 1
    for cluster in listOfClusters:
        print("\n------------ Cluster " + str(clusterNum) + " Statistics -----------------------\n")
        for col in range(0,len(listOfClusters[0][0])-1):
            if (len(cluster) > 0):
                sum = 0
                for row in cluster:
                    sum += row[col]
                print("Cluster " + str(clusterNum) + " " + colNames[col] + ": " + str(float(sum)/float(len(cluster))))
        clusterNum += 1

openClusters('dpClustersYear.csv')