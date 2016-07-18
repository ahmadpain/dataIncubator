#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
"""
Author:     Ahmad Paintdakhi
Copyright:  2016
"""
"""
The import routines import outside libraries
for code efficiency and transparency
"""
import numpy as np
import pandas as pd
from scipy import stats
''' Data is read using a nice API provided by the pandas library
    The data can be read as chunks of memory for future high-throughput
    analysis such as HPC clusters.  The different chunks of data can be
    processed on the different nodes to streamline the parallelization routine
'''
data = pd.read_csv(inputFileName,engine='c')
headers = data.columns.format(formater='%S')
classCode = data.loc[:,'Property Class Code']
fraction = (classCode.value_counts().max())/len(classCode)


years = data.loc[:,'Closed Roll Fiscal Year']
sortedYears=years.sort_values()
indexSortedYears=sortedYears.index
blockNum = data.loc[:,'Block and Lot Number']
blockNumSortedByYear=blockNum[indexSortedYears]
uniqueBlockNum,indexToUniqueBlockNum=np.unique(blockNumSortedByYear,return_index=True)
improvementValue = data.loc[:,'Closed Roll Assessed Improvement Value']
improvementValueTemp = improvementValue[indexToUniqueBlockNum]
improvementValueTempNonzero = improvementValueTemp.replace(0,np.NaN)
median = improvementValueTemp.median()

improvementValueNonzero = improvementValue.replace(0,np.NaN)
neighborhoodCode = (data.loc[:,'Neighborhood Code']).dropna()
uniqueNeighborhoodCode = neighborhoodCode.unique()
tempArray = []
tempArray = [0]*len(uniqueNeighborhoodCode)
for ii in range(0,len(uniqueNeighborhoodCode)):
    xx = neighborhoodCode[neighborhoodCode==uniqueNeighborhoodCode[ii]]
    temp=improvementValueNonzero[xx.index]
    tempArray[ii]=temp.mean()
diffValue = np.max(tempArray)-np.min(tempArray)

landValue = data.loc[:,'Closed Roll Assessed Land Value']
landValueNonZero = (landValue[landValue.nonzero()[0][:]]).dropna()
years = years[landValueNonZero.index]
slop,intercept, r_value, p_value, std_err = stats.linregress(years,landValueNonZero)


units = data.loc[:,'Number of Units']
yearBuilt = data.loc[:,'Year Property Built']
blockNum = data.loc[:,'Block and Lot Number']
sortedYears=yearBuilt.sort_values()
indexSortedYears=sortedYears.index
blockNumSortedByYear=blockNum[indexSortedYears]
uniqueBlockNum,indexToUniqueBlockNum=np.unique(blockNumSortedByYear,return_index=True)
yearTemp = yearBuilt[indexToUniqueBlockNum]
after1950 = yearTemp[yearBuilt>= 1950]
before1950 = yearTemp[yearBuilt< 1950]
indexBefore1950 = before1950.index
unitsBefore1950 = units[indexBefore1950]
indexAfter1950 = after1950.index
unitsAfter1950 = units[indexAfter1950]
a = unitsBefore1950[unitsBefore1950!=0]
b = unitsAfter1950[unitsAfter1950!=0]
b.mean() - a.mean()

zipcode = data.loc[:,'Zipcode of Parcel']
zipcode = zipcode.dropna()
bedrooms = data.loc[:,'Number of Bedrooms']
bedroomsNonzero = bedrooms[bedrooms!=0]
bedroomsNonzero = bedroomsNonzero[units.index]
bedroomsNonzero = bedroomsNonzero[~np.isnan(bedroomsNonzero)]
zipcode = zipcode[bedroomsNonzero.index]
uniqueZipcode = zipcode.unique()
tempArray = []
tempArray = [0]*len(uniqueZipcode)
for ii in range(0,len(uniqueZipcode)):
    xx = zipcode[zipcode==uniqueZipcode[ii]]
    temp=bedroomsNonzero[xx.index]
    tempArray[ii]=temp.mean()
aa = np.asanyarray(tempArray)
aa = aa[~np.isnan(aa)]
aa.max()

propertyArea = data.loc[:,'Property Area in Square Feet']
lotArea = data.loc[:,'Lot Area']
zipcode = zipcode.dropna()
uniqueZipcode = zipcode.unique()
lotArea = lotArea[lotArea!=0]
propertyArea = propertyArea[lotArea.index]
tempArray = []
tempArray = [0]*len(uniqueZipcode)
for ii in range(0,len(uniqueZipcode)):
    xx = zipcode[zipcode==uniqueZipcode[ii]]
    temp1=lotArea[xx.index].sum()
    if temp1 != 0:
        temp2=propertyArea[xx.index].sum()
        temp3 = temp2/temp1
        tempArray[ii]=temp3
tempArray=np.asanyarray(tempArray)
tempArray.max()
"""All nan values are treated as zero values in this case"""
data = data.fillna(0) 







