"""
Author: D Jayme Green
Date: 2/15/17
Ostu's Method and One-Dimensional Clustering


This program splits vehicles into two groups: intentionally speeding or 
people who are maximizing safety. It studies traffic volume for road
planning in order to maximize traffic flow. This problem does not 
cause any ethical concerns for me since it is trying to make the road
better for everyone

If this program was computer vision which automatically sends a ticket
to a reckless driver, I would want to know how exactly it would be
implemented and whether it was for safety or money. Also, I would consult
the town/city people themselves if they want it as well as whether the
road they put it on has a good speed limit. Being automatic, I want to
be absolutely sure it is best for the community and everyone agrees.
"""

"""
Matplotlib, csv, numpy imported
Matplotlib is used to generate the graphs
Csv is used to read in the csv data
Numpy is used to allow floats into Matplotlib
"""
import matplotlib.pyplot as mpl
import csv
import numpy as np


"""
Constants are declared below for Histogram
CarSpeedsFromCSV holds all of the numbers from the csv file
which will be used for the histogram and the rest of the program
"""
currCarSpeedsFromCSV = list()

def restartCarSpeedsFromCSV():
    return(list())
#carSpeedsFromCSV = list()



"""
Reading in the .csv file and putting it into carSpeedsFromCSV list
"""
def openCSVFile(fileName, carSpeedsFromCSV):
    with open(fileName, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        rowNum = 0
        for row in reader:
            try:
                currCarSpeedsFromCSV.append(float(row[0]))
            except ValueError:
                print("Not adding row: "+ str(rowNum)) 
            rowNum += 1
    return carSpeedsFromCSV

restartCarSpeedsFromCSV()
currCarSpeedsFromCSV = openCSVFile('MedianWealth.csv', currCarSpeedsFromCSV)
        

"""
Creating a histogram from the data of the csv file
The histogram will have bins starting at 38 and ending at 80 with 2mph difference
"""
counts, bins, patches = mpl.hist(currCarSpeedsFromCSV, bins=np.arange(min(currCarSpeedsFromCSV), 100000 + 5000,5000), linewidth=2, edgecolor='white')
for patch, rightside, leftside in zip(patches, bins[1:], bins[:-1]):
    if rightside < 38000:
        patch.set_facecolor('blue')
    elif leftside > 38000:
        patch.set_facecolor('red')
mpl.xlabel("Median Wealth of Graduates After 10 Years")
mpl.ylabel('Amount of Colleges')
mpl.title('Median Income of Graduates After 10 Years')
mpl.grid(True)
mpl.show()


"""
Ostu's Method for 1D Clustering
Used design from lecture slides in order to do it
"""

"""
Finds the variance of the data in carSpeedsFromCSV which are
over or under the threshold given depending on isOver
@param isOver           Boolean specifying whether to find the variance
                        over or under the threshold
@param currentThreshold Int specifying what the threshold is currently to
                        find the variance over or under it
"""
def findTheVariance(isOver, currentThreshold, carSpeedsFromCSV):
    sumOfAllOverOrUnder = 0
    mu = 0
    sumOfDifferenceSquared = 0
    sizeOfPointsOverOrUnder = 0
    standardDeviation = 0
    if(isOver):
        for speeds in carSpeedsFromCSV:
            if(speeds > currentThreshold):
                sumOfAllOverOrUnder += speeds
                sizeOfPointsOverOrUnder += 1
        
        if(sizeOfPointsOverOrUnder == 0):
            return 0
        mu = float(sumOfAllOverOrUnder)/float(sizeOfPointsOverOrUnder)
        for speeds in carSpeedsFromCSV:
            if(speeds > currentThreshold):
                sumOfDifferenceSquared += pow(speeds-mu,2)
        return (sumOfDifferenceSquared/float(sizeOfPointsOverOrUnder))
    else:
        for speeds in carSpeedsFromCSV:
            if(speeds <= currentThreshold):
                sumOfAllOverOrUnder += speeds
                sizeOfPointsOverOrUnder += 1
        if(sizeOfPointsOverOrUnder == 0):
            return 0
        mu = float(sumOfAllOverOrUnder)/float(sizeOfPointsOverOrUnder)
        for speeds in carSpeedsFromCSV:
            if(speeds <= currentThreshold):
                sumOfDifferenceSquared += pow(speeds-mu,2)
        return (sumOfDifferenceSquared/float(sizeOfPointsOverOrUnder))

"""
Amount of points under or over the current threshold
@param isOver               Boolean determining whether to get the
                            amount of points above (true) or below (false)
@param currentThreshold     The current threshold to find
                            how many points are above or below
"""
def findAmountOfPoints(isOver, currentThreshold, carSpeedsFromCSV):
    amount = 0
    for speeds in carSpeedsFromCSV:
        if(isOver):
            if(speeds > currentThreshold):
                amount += 1
        else:
            if(speeds <= currentThreshold):
                amount += 1
    return amount

"""
Variables used for Ostu's method initialized below
"""
totalThresholdPoints = max(currCarSpeedsFromCSV)-min(currCarSpeedsFromCSV)



"""
Ostu's Method for 1 Clustering
It uses a multitude of functions before this
and returns all of the valuable information to the places below
"""
def doOstuMethod(minRange, maxRange, carSpeedsFromCSV):

    bestMixedVariance = 99999999
    bestThreshold = 0
    allMixedVariances = list()

    for threshold in range(int(minRange),int(maxRange)):
        wtUnder = float(findAmountOfPoints(False, threshold, carSpeedsFromCSV))/float(totalThresholdPoints) if totalThresholdPoints != 0 else 0
        varUnder = findTheVariance(False, threshold, carSpeedsFromCSV)
        wtOver = float(findAmountOfPoints(True, threshold, carSpeedsFromCSV))/float(totalThresholdPoints) if totalThresholdPoints != 0 else 0
        varOver = findTheVariance(True, threshold, carSpeedsFromCSV)
        mixedVariance = (wtUnder * varUnder) + (wtOver * varOver)
        allMixedVariances.append(mixedVariance)
        if(mixedVariance < bestMixedVariance):
            bestMixedVariance = mixedVariance
            bestThreshold = threshold

    print("The best threshold is: " + str(bestThreshold))
    print("The best, smallest variance is: " + str(bestMixedVariance))
    return(bestMixedVariance, bestThreshold, allMixedVariances)


"""
All of the return values for Ostu's method
These include the best variance, best threshold, and allMixedVariances
These values are used later for the graph below
"""
OstuMethodReturn = doOstuMethod(min(currCarSpeedsFromCSV), max(currCarSpeedsFromCSV), currCarSpeedsFromCSV)
bestMixedVariance = OstuMethodReturn[0]
bestThreshold = OstuMethodReturn[1]
allMixedVariances = OstuMethodReturn[2]
"""
Graph for mixed variance for the car data versus the value used to segment the data into two clusters
"""

bestThresholdList = [bestThreshold] * int(totalThresholdPoints)
#for val in range(0,totalThresholdPoints):
 #   bestThresholdList.append(bestThreshold)
mpl.plot(allMixedVariances, bestThresholdList, 'ro')
mpl.xlabel('Mixed Variance')
mpl.ylabel('Best Value to Segment the Cars')
mpl.title('Mixed Variance vs The Best Threshold of 1D Clustering')
mpl.show()


"""
For the mystery data, we reset the list of car data used previous to an empty list
Then we fill that empty list of the data from the Mystery_Data file
Lastly, we do the Ostu's Method on the data which that prints out the best threshold and variance
"""
#currCarSpeedsFromCSV = restartCarSpeedsFromCSV()
#currCarSpeedsFromCSV = openCSVFile('MedianWealth.csv', currCarSpeedsFromCSV)
#doOstuMethod(6,38, currCarSpeedsFromCSV)

