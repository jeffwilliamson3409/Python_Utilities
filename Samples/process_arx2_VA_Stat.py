#!/opt/cloudera/parcels/Anaconda-4.0.0/bin/python

import re
import pandas as pd
from collections import OrderedDict as od
import sys
import os
import logging
from datetime import datetime as dt

#Assumptions
#1) Each file will contain 1 report with one file header (1 page)

#cmd console args from sys
#argv[1] = arx2 file to execute
#argv[2] = csv landing folder
#argv[3] = .log file landing folder

#global variables
trackerDict = {}
dateStamp = dt.now().strftime("%Y%m%d%H%M%S")  
logFileName = 'log_creation_timestamp_'+dateStamp+'.log'
logFileRoot = sys.argv[3]
logFileFullPath = logFileRoot+logFileName
logging.basicConfig(filename=logFileFullPath,level=logging.DEBUG)
            
#VA Stat specific arx2 rawline parse function
def parse_Arx2_RawLine(rawLine, sectionHeader, quarterlyCashFlowList, Reset):
    #initialize secNum & rowNum
    if sectionHeader in trackerDict.keys():
        secNum = list(trackerDict[sectionHeader].keys())[0]
    else:
        secNum = 1
    rowNum = 1
    #handle trackerDict reset branching logic
    if Reset == True:
        if sectionHeader not in trackerDict.keys():
            trackerDict.update({sectionHeader: {1: {}}})
            secNum = list(trackerDict[sectionHeader].keys())[0]
        else:
            l = list(trackerDict[sectionHeader].keys())
            trackerDict[sectionHeader][l[0] + 1] = trackerDict[sectionHeader].pop(l[0])
            l2 = list(trackerDict[sectionHeader].keys())
            trackerDict[sectionHeader][l2[0]] = {}
            secNum = list(trackerDict[sectionHeader].keys())[0]   
    #clean ( from rawLine to avoid escape issues
    rawClenseParenRight = rawLine.replace("(", "")
    #clean ) from rawLine to avoid escape issues
    rawClenseParenLeft = rawClenseParenRight.replace(")", "")
    #cast fixed width empty string and string of stars to NULL
    stagedRawLineForNullQuarters_1 = rawClenseParenLeft.replace("                     ", "NULL")
    stagedRawLineForNullQuarters = stagedRawLineForNullQuarters_1.replace("********************", "NULL")
    #regex any string search variable
    rowHeaderSearch = r'\"(.+?)\"'
    #stage variable for extracting index spans
    specifiedHeaderSpanObj = re.search(rowHeaderSearch, rawLine)
    #use span to isolate the headerRow
    specifiedHeaderRaw = rawLine[specifiedHeaderSpanObj.span()[0]: specifiedHeaderSpanObj.span()[1]]
    #clean out the double quotes from the headerRow
    specifiedHeader = specifiedHeaderRaw.replace('"', '')
    if specifiedHeader not in trackerDict[sectionHeader][list(trackerDict[sectionHeader].keys())[0]]:
        trackerDict[sectionHeader][list(trackerDict[sectionHeader].keys())[0]].update({specifiedHeader:1})
        rowNum = 1
    else:
         trackerDict[sectionHeader][list(trackerDict[sectionHeader].keys())[0]][specifiedHeader] = trackerDict[sectionHeader][list(trackerDict[sectionHeader].keys())[0]][specifiedHeader] + 1
         rowNum = trackerDict[sectionHeader][list(trackerDict[sectionHeader].keys())[0]][specifiedHeader]
    #regex floating point raw string search variable
    floatSearch = r'[-+]?[0-9]*\.?[0-9]+|"NULL"'
    #span()[1] locates the index position at the end of the specified header string
    lineAfterHeader = stagedRawLineForNullQuarters[re.search(specifiedHeader, stagedRawLineForNullQuarters).span()[1]:]
    floatsOnlyAfterHeader = re.search(floatSearch, lineAfterHeader)
    #span()[0] finds the beginning index position of the first float after the specified header
    allFloatsIndexBeg = floatsOnlyAfterHeader.span()[0]
    #\s+ is regex white space delimiter of arbitrary length
    delimiiter = '\s+'
    #split float values into a list
    all_floats_in_list = re.split(delimiiter, lineAfterHeader[allFloatsIndexBeg:])
    #list for clean field returns (converts NULL to None)
    returnClean = od()
    #eliminate blank value that is appended to end of list
    floatInListNoBlank = all_floats_in_list[:-1]
    #loop through and append clean fields as floats NULL fields as None
    for index, i in enumerate(floatInListNoBlank):
        if i == '"NULL"':
            returnClean.update({quarterlyCashFlowList[index]:od({rowNum:od({secNum: od({index: None})})})})
        else:
            returnClean.update({quarterlyCashFlowList[index]:od({rowNum:od({secNum: od({index: float(i)})})})})
    #final return dictionary has rowHeader as key and list of floats and None as values
    finalDict = {sectionHeader.replace('\n', '') : od({specifiedHeader: returnClean})}
    return finalDict

#returns bool checking if the row possesses a section header
def is_SectionHeader(rawLine):
    rawClenseParenRight = rawLine.replace("(", "")
    rawClenseParenLeft = rawClenseParenRight.replace(")", "")
    stagedRawLineForNullQuarters = rawClenseParenLeft.replace("                     ", "NULL")
    sectionHeaderSearch = r'\"(.+?)\"'
    floatSearch = r'[-+]?[0-9]*\.?[0-9]+|"NULL"'
    s = re.findall(sectionHeaderSearch, stagedRawLineForNullQuarters)
    if s.__len__() == 0:
        return False
    else:
        ss = re.search(sectionHeaderSearch, stagedRawLineForNullQuarters)
        endOfHeader = ss.span()[1]
        f = re.findall(floatSearch, stagedRawLineForNullQuarters[endOfHeader:])
        if f.__len__() == 0:
            return True
        else:
            return False

#cleans the section header of double quotes
def cleanSectionHeader(rawLine):
    rawLineClean = rawLine.replace('"', '')
    rawLineClean2 = rawLineClean.replace('\n', '')
    return rawLineClean2

#***********************************************************
#Functions to extract metadata from file header
#***********************************************************

#extract Cycle Count from the file header
def findCycleCount(rawLine):
    try:
        cycleFind = 'Cycles:'
        cSpan = re.search(cycleFind, rawLine)
        cycleLine = rawLine[cSpan.span()[1]:]
        cycleLine_c1 = cycleLine.replace('"', '')
        cycleLine_c2 = cycleLine_c1.replace(' ', '')
        cycles = int(cycleLine_c2)
        return (True, cycles)
    except Exception as e:
        return (False, e)

#extract ValDate from the file header
def findValDate(rawLine):
    try:
        valFind = 'Val Date:'
        vspan = re.search(valFind, rawLine)
        valLine = rawLine[vspan.span()[1]:]
        valLine_c1 = valLine.replace('"', '')
        valLine_c2 = valLine_c1.replace(' ', '')
        valLine_c3 = valLine_c2.replace('\n', '')
        valDate = valLine_c3
        return (True, valDate)
    except Exception as e:
        return (False, e)

#returns bool indicating if the rawLine is the final row of the file header
def isFileHeaderFinalRow(rawLine):
    headdrFinalRowFind = '"" "--------------------" "--------------------"'
    frSearch = re.findall(headdrFinalRowFind, rawLine)
    if frSearch.__len__() > 0:
        return True
    else:
        return False

#construct the quarterly cashflow date list
def quarterlyCashFlowConstructor(cycles, valDate):
    valDateFormatted = ('0' + valDate)[-7:]
    returnList= []
    m = valDateFormatted[:2]
    sep = '/'
    y = valDateFormatted[-4:]
    objAppend = m+sep+y
    returnList.append(objAppend)
    for i in range(cycles):
        if m == '12':
            m ='03'
            y = str(int(y) + 1)
        else:
            mStage = int(m) + 3
            m = ('0' + str(mStage))[-2:]
        objAppend = m+sep+y
        returnList.append(objAppend)
    return returnList

def main(*args, **kwargs):

    data = []
    secHeaderData = ''
    cycles = 0
    valDate = ''
    headerFinalRow = 0
    Reset = False
    targetFileNameStage = os.path.basename(args[0])
    targetFileNameStage2 = targetFileNameStage.replace('.Arx2', '.csv')
    targetFileNameStage3 = targetFileNameStage2.replace('.arx2', '.csv')
    targetFileNameStage4 = targetFileNameStage3.replace('.ARX2', '.csv')
    targetFileName = targetFileNameStage4 
    isPrevRowSectionHeader = False
  
    with open(args[0]) as f:

        rl = f.readlines()

        for index, i in enumerate(rl):
            z = isFileHeaderFinalRow(i)
            if z == True:
                headerFinalRow = index
                break

        for index, i in enumerate(rl):
            z = findCycleCount(i)
            if z[0] == True:
                cycles = z[1]
                break

        for index, i in enumerate(rl):
            z = findValDate(i)
            if z[0] == True:
                valDate = z[1]
                break

        quarterlyCashFlowList = quarterlyCashFlowConstructor(cycles, valDate)

        for index, i in enumerate(rl):
            
            if index > headerFinalRow:
                try:
                    if is_SectionHeader(i) == True and isPrevRowSectionHeader == False:
                        z = cleanSectionHeader(i)
                        secHeaderData = z
                        isPrevRowSectionHeader = True
                        Reset = True
                    else:
                        isPrevRowSectionHeader = False
                        Reset = False
                    ap = parse_Arx2_RawLine(i, secHeaderData, quarterlyCashFlowList, Reset)
                    data.append(ap)
                    logging.debug('Successful data capture at file index ' + str(index))
                except Exception as e:
                    logging.exception(str(e) + ' at index ' + str(index))
                    
    #pivot the data for DataFrame consumption
    pivotedData = []

    #iterate through the list and dicts to pivot the data
    for index, record in enumerate(data):
        for k1, v1 in record.items():
            for k2, v2 in v1.items():
                for k3, v3 in v2.items():
                    for k4, v4 in v3.items():
                        for k5, v5 in v4.items():
                            for k6, v6 in v5.items():
                                pivotedData.append(od({'Section':k1, 'Row': k2, 'ValDate': k3, 'Section_Row_Occurrence': k4, 'Section_Occurrence': k5, 'CashFlowIndex': k6, 'CashFlow': v6}))

    #create DataFrame and csv output example
    pivotedDataFrame = pd.DataFrame.from_records(pivotedData, columns=['Section', 'Row', 'ValDate', 'CashFlow', 'CashFlowIndex', 'Section_Occurrence', 'Section_Row_Occurrence'])
    #print(pivotedDataFrame)
    targetPath = args[1]
    pd.DataFrame.to_csv(pivotedDataFrame, targetPath+targetFileName)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
   



