import re
import numpy as np
import matplotlib.pyplot as plt
from os.path import join
from CONTINWrapper import *
from scipy.signal import argrelmax

testfiledir='./output data for test/'

testfile1=join(testfiledir,'ord_err_abs_blocksample.txt')

testfile2=join(testfiledir,'contin_part1.out')

testfile3=join(testfiledir,'ord_err_abs_blocksample2.txt')

testfile4="./tmpoutput/mySimulatedTest.out"


def testreadblock():
    data=readblock(open(testfile,'r'))
    print data.shape
    plt.semilogx(data[:,2],data[:,0])
    plt.show()

def test_findextrema(templateFile):

    testTemperature=100
    paramList=readInputParamFromFile(templateFile)  

    tp=trapLevel([0.06,0.1])

    xdata,ydata=tp.getTransient(T=testTemperature,plotGraph=True,gridnum=100)

    emRates=tp.emRateT(testTemperature)


    alldata=runCONTINfit(xdata,ydata,templateFile)

    testxdata=alldata[0][1][:,2]

    testydata=alldata[0][1][:,0]

    relMaxIdx=argrelmax(testydata)

    plt.semilogx(testxdata,testydata,hold=True)

    plt.show()

    plt.close()

    print testxdata[relMaxIdx[0]]
    print testydata[relMaxIdx[0]]





def test_runCONFITfit_simData(templateFile,plotMode='each'):
    
    testTemperature=100
    paramList=readInputParamFromFile(templateFile)  

    tp=trapLevel([0.06,0.1])

    xdata,ydata=tp.getTransient(T=testTemperature,plotGraph=True,gridnum=100)

    emRates=tp.emRateT(testTemperature)


    alldata=runCONTINfit(xdata,ydata,templateFile)

    if plotMode=='each':
        for i,data in enumerate(alldata):
            plt.semilogx(data[1][:,2],data[1][:,0],hold=True)
            
            for em in emRates:
                plt.semilogx([em,em],[0,np.amax(data[1])],hold=True,linestyle='--')


            plt.xlabel("emission rate(s^-1)")
            plt.ylabel("amplitude")
            plt.title("alpha %s"%data[0][1])
            
            plt.savefig("./tmpoutput/test"+str(i)+".png")


            plt.close()
    
    elif plotMode=='merge':
        for i,data in enumerate(alldata):
            plt.semilogx(data[1][:,2],data[1][:,0],hold=True)
        for em in emRates:
            maxarr=[np.amax(d[1][:,0]) for d in alldata ]
            plt.semilogx([em,em],[0,np.amax(maxarr)],hold=True,linestyle='--')     
    
        plt.xlabel("emission rate(s^-1)")
        plt.ylabel("amplitude")
        plt.savefig("./tmpoutput/test.pdf")
        plt.show()
        plt.close()




def testgetParamString():
    str1=' GMNMX     1   5.496109E-04'
    str2=' GMNMX         8.573930E-01'
    str3=" IFORMT\n (1E2.3)"

    assert getParamString('GMNMX',1,5.496109E-04)==str1
    assert getParamString('GMNMX',"",8.573930E-01)==str2

    assert getParamString('IFORMT',"",'(1E2.3)')==str3

if __name__=="__main__":

    test_runCONFITfit_simData('paramTemplate.txt',plotMode='merge')
    #test_findextrema('paramTemplate.txt')

