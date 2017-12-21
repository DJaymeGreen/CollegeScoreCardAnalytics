"""
Author: D Jayme Green
Date: 4/22/17
Agglomerative


This program creates a classifer using the given 
Testing data
"""

"""
Csv is used to read in the csv data
Numpy is used to allow floats into Matplotlib
"""
import matplotlib.pyplot as mpl
import csv
import math
import numpy as np
import sys;


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

listOfData, totalNumberOfVals, numberOfCols = openCSVFile('collegeDemoIncome.csv')

"""
Creates a what cluster dictionary. Each key holds the cluster id and the
value indicates what row(s) is/are part of that cluster.
When created, every row is its own cluster
"""
def createWhatCluster():
    #whatCluster = dict()
    for row in range(0, len(listOfData)):
        whatCluster[row] = [row]
    return whatCluster

"""
Updates all of the center of masses of the clusters' data structure.
It utilizes whatCluster to look at what clusters are combined
"""
def updateCoM():
    clusters = list(list())
    for cluster in whatCluster.keys():              # Each cluster
        com = [0] * (numberOfCols)
        com[0] = min(whatCluster.get(cluster))
        #com = [min(whatCluster.get(cluster)), 0 *numberOfCols]
        for rows in whatCluster.get(cluster):       # Each row id in cluster
            currColNum = 0
            for rowInfo in listOfData[rows]:        # Each col in the row's id
                if currColNum != 0:
                    com[currColNum] += rowInfo
                currColNum += 1
        currColNum = 0
        for rows in listOfData[0]:       # Divide each value by how many values in mass to get CoM
            if currColNum != 0:
                amountOfPoints = float(len(whatCluster.get(cluster)))
                com[currColNum] /= amountOfPoints
            currColNum += 1
        clusters.append(com)
    return clusters

"""
Creates the original cluster data structure as a list of list
The top level list represents each cluster.
The list in each cluster represents the id and then the center of mass
"""
def createClusters():
    return(updateCoM())

createWhatCluster()
clusters = createClusters()

"""
Finds a given row where the id matches the parameter. Returns null if 
nothing is found (should not happen)
@param          id              The id to find the row of in clusters
"""
def findClusterWithID(id):
    rowIndex = 0
    for row in clusters:
        if (row[0] == id):
            return rowIndex
        rowIndex += 1
    return None


"""
Finds the Euclidean Distance between rowOne and rowTwo
@param      rowOne          The index of the row in clusters
@param      rowTwo          The index of the row in clusters
"""
def findEuclideanDistance(rowOne, rowTwo):
    distance = 0
    rowOneIndex = findClusterWithID(rowOne)
    rowTwoIndex = findClusterWithID(rowTwo)
    for col in range(1, numberOfCols):
        distance += pow(clusters[rowOneIndex][col] - clusters[rowTwoIndex][col], 2)
    return (math.sqrt(distance))


"""
Updates all of the distances of every cluster to each other in a list of list
Both lists contain the clusters with their value's being the distance from each other
It should be symmetrical
"""
def updateAllDistances():
    euclideanDistance = [[sys.float_info.max for x in range(totalNumberOfVals)] for y in range(totalNumberOfVals)]
    for clusterA in whatCluster.keys():
        for clusterB in whatCluster.keys():
            if (clusterA == clusterB):
               euclideanDistance[clusterA][clusterB] = sys.float_info.max
            #elif (euclideanDistance[clusterB][clusterA] != 0):
             #   euclideanDistance[clusterA][clusterB] = euclideanDistance[clusterB][clusterA]
            else:
                if (clusterA in combinedRows or clusterB in combinedRows):
                    print("Should be 13")
                else:
                    euclideanDistance[clusterA][clusterB] = findEuclideanDistance(min(whatCluster.get(clusterA)),min(whatCluster.get(clusterB)))
    return euclideanDistance

euclideanDistance = updateAllDistances()

"""
Finds the two most similar clusters based on euclideanDistance
and returns them 
"""
def findMostSimilar(euclideanDistance):
    clustA = 0
    clustB = 0
    smallestDistance = sys.float_info.max
    for row in range(0, len(euclideanDistance)):
        for col in range(row, len(euclideanDistance)):
            if (euclideanDistance[row][col] < smallestDistance):
                smallestDistance = euclideanDistance[row][col]
                clustA = row
                clustB = col
    print(str(clustA) + " and " + str(clustB) + " are about to be merged!")
    print("Their sizes: " + str(len(whatCluster.get(clustA))) + ", " + str(len(whatCluster.get(clustB))))
    return clustA,clustB

"""
Updates whatCluster given the two clusters being combined
@param      clusterA            One of the clusters being combined
@param      clusterB            The second cluster to be combined
"""
def updateWhatCluster(clusterA, clusterB):
    smallerCluster = min(clusterA,clusterB)
    largerCluster = max(clusterA,clusterB)
    listOfLargerClusterRows = whatCluster.get(largerCluster)
    combinedRows.append(largerCluster)
    whatCluster.pop(largerCluster)
    for row in listOfLargerClusterRows:
        whatCluster[smallerCluster].append(row)


"""
Does the agglomerative clustering algorithm until clustering is complete (dependent on stop var declared at top)
Uses most of the helper functions above to do the algorithm
"""
def agglomerativeClustering():
    # Find the most similar pair
    euclideanDis = euclideanDistance
    while(len(whatCluster.keys()) > 3):
        print("This many keys: " + len(whatCluster.keys()))
        clusterA,clusterB = findMostSimilar(euclideanDis)
        # Merge them into a single cluster
        updateWhatCluster(clusterA,clusterB)
        # Update the cluster prototype
        clusters = updateCoM()
        # Compute the all the distances
        euclideanDis = updateAllDistances()
    printClusters()

"""
Prints every cluster
"""
def printClusters():
    for cluster in whatCluster.keys():
        print("Cluster " + str(cluster) + ":")
        clusterInfo = ""
        for rowsInCluster in whatCluster.get(cluster):
            clusterInfo += " " + str(rowsInCluster+1)
        print(clusterInfo)
        print(clusters[cluster])


agglomerativeClustering()