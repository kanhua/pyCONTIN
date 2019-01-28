from __future__ import print_function
import numpy as np
import os
import re

CONTINPath = '/Users/kanhua/Dropbox/Programming/pyCONTIN/exec/contin.out'


def runCONTINfit(xdata, ydata, parameterFile, continInputFile=None, continOutputFile=None):
    """
    Run the CONTIN fitting in one go. This function packages the small functions and do all the work.
        parameterFile: the csv parameter file to be transformed into part of continInputFile
        continInputFile: input file for CONTIN main program, set None if use default dummpy input file
        continOutputFile: input file for CONTIN main program, set None if use default dummpy output file
    """

    # Retrieve the current directory
    thisDir = os.path.split(__file__)[0]

    originalDir = os.getcwd()

    os.chdir(thisDir)

    if continInputFile == None:
        continInputFile = "CONTINInput.txt"
        print("continInputFile", continInputFile)
    if continOutputFile == None:
        continOutputFile = "CONTINOutput.txt"

    paramList = readInputParamFromFile(parameterFile)

    for idx, p in enumerate(paramList):
        if p[0] == 'GMNMX' and p[2] == -1:
            if p[1] == 1:
                paramList[idx] = (p[0], p[1], defaultGMNMX1(xdata))
            if p[1] == 2:
                paramList[idx] = (p[0], p[1], defaultGMNMX2(xdata))

    genInputFile(continInputFile, paramList, (xdata, ydata))

    runCONTIN(continInputFile, continOutputFile)

    alldata = readCONTINoutput(continOutputFile)

    os.chdir(originalDir)
    return alldata


def writeData(outputDev, xdata=None, ydata=None):
    """
    Write the x(time) and y(signal) data into outputDev

    outputDev: the object that the data writes into 
    """

    if xdata is None and ydata is None:
        tp = trapLevel([0.05, 0.1])

        xdata, ydata = tp.getTransient(T=200, plotGraph=True, gridnum=40)

    tt = np.concatenate((xdata, ydata))

    for i, c in enumerate(tt):
        outputDev.write("{:>11.4E}".format(c) + '\n')
        # if (i+1)%5==0:
        #    print "\n",


#   spec3="{:>15.6E}"
#   print "suggest gamma1", spec3.format(0.1/np.max(t))
#   print "suggest gamma2", spec3.format(4/(t[1]-t[0]))

def getParamString(paramName, arrayIndex, paramValue):
    """Prepare the parameter names, index, and values to a string"""

    printGauge = False
    spec1 = "{:6}"
    spec2 = "{:5}"
    spec3 = "{:>15.6E}"

    formatSpecParam = ('IFORMT', 'IFORMY')

    if paramName in formatSpecParam:
        fullStr = " " + spec1.format(paramName) + '\n' + " " + paramValue

    else:
        fullStr = " " + spec1.format(paramName) + spec2.format(arrayIndex) + spec3.format(paramValue)

    if printGauge == True:
        print("12345612345123456789012345")

    return fullStr


def genInputFile(fileForCONTINInput, paramList, data):
    """
    Put all the parameters and xy-data into the file as the input for CONTIN
    fileForCONTINInput: the input file for CONTIN
    paramList: a list of user-defined parameters [(parmeterName1, paramIndex1, paramValue1),
    (paramName2, paramIndex2, paramValue2,...)] 
    data: a tuple of (xdata, ydata)

    """

    of = open(fileForCONTINInput, 'w')

    of.write(' Interface input file\n')

    for param in paramList:
        of.write(getParamString(param[0], param[1], param[2]) + "\n")

    of.write(" END\n")

    # write data
    xdata, ydata = data

    assert xdata.shape == ydata.shape

    NYstr = " " + "{:6}".format("NY") + "{:5}".format(len(xdata))

    of.write(NYstr + "\n")

    writeData(of, xdata, ydata)


def defaultGMNMX1(t):
    return 0.1 / np.max(t)


def defaultGMNMX2(t):
    return 4 / (t[1] - t[0])


def readInputParamFromFile(templateFile):
    """
    Read a parameter setting file and return a list of parameters
    in the form of [(parmeterName1, paramIndex1, paramValue1),
    (paramName2, paramIndex2, paramValue2,...)] 
    This function also converts read-in values to appropriate data types.
    """

    infile = open(templateFile, 'r')

    titleLine = next(infile)

    formatSpecParam = ('IFORMT', 'IFORMY')

    paramList = []
    for line in infile:
        tmpParam = line.split(",")
        if tmpParam[1] is not "":
            tmpParam[1] = int(tmpParam[1])
        if tmpParam[0] not in formatSpecParam:
            tmpParam[2] = float(tmpParam[2])
        else:
            tmpParam[2] = tmpParam[2].strip()
        paramList.append(tmpParam)

    return paramList


def readblock(fileObj):
    """
    parse the block of data like below
        ORDINATE    ERROR  ABSCISSA
   2.930E-06  1.8D-07  5.00E+02      X.
   8.066E-06  4.8D-07  6.80E+02                 .X.
   1.468E-05  8.3D-07  9.24E+02                               ..X. 
   2.204E-05  1.2D-06  1.26E+03                                              ...X...

    """
    data = []

    p = re.compile('ORDINATE')
    q = re.compile('0LINEAR COEFFICIENTS')
    for line in fileObj:
        if q.search(line) is not None:
            break
        if p.search(line) is None:
            dataContent = line[0:31]
            dataContent = dataContent.replace('D', 'E')
            datarow = list(map(float, dataContent.split()))
            data.append(datarow)

    return np.array(data)


def readCONTINoutput(filename):
    """
    Read in the output file generated by CONTIN, 
    find the blocks that contains the fitted results,
    then return a list of data:
    [[(alphaArray1, dataArray1), (alphaArray2,dataArray2),....]

    each numpy array has three columns, recording ORDINATE, ERROR and ABSCISSA, respectively
    alphaArray1, alphaArray2... stores the values under the column ALPHA, ALPHA/S(1)... etc.

    """

    chunkTitle = re.compile('OBJ. FCTN.       VARIANCE      STD. DEV. ')

    fileObj = open(filename, 'r')

    alldata = []

    for line in fileObj:
        if chunkTitle.search(line) is not None:
            alphaLine = next(fileObj)
            alphaLine = alphaLine.replace('*', '')
            alphaParam = np.fromstring(alphaLine, sep=' ')

            next(fileObj)
            alldata.append((alphaParam, readblock(fileObj)))

    return alldata


def runCONTIN(inputFile, outputFile):
    execFile = CONTINPath

    fullcommand = execFile + " < " + inputFile + " > " + outputFile;

    os.system(fullcommand)
