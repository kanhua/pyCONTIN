import re
import numpy as np
import matplotlib.pyplot as plt
from os.path import join
from CONTINWrapper import *

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


def testgenInputFile(templateFile):
	

	paramList=readInputParamFromFile(templateFile)	

	tp=trapLevel([0.1,0.05])

	xdata,ydata=tp.getTransient(T=280,plotGraph=False,gridnum=100)

	print tp.emRateT(280)

	for idx,p in enumerate(paramList):
		if p[0]=='GMNMX':
			if p[1]==1:
				paramList[idx]=(p[0],p[1],defaultGMNMX1(xdata))
			if p[2]==2:
				paramList[idx]=(p[0],p[1],defaultGMNMX2(xdata))


	genInputFile('./tmpoutput/testout',paramList,(xdata,ydata))

	runCONTIN('./tmpoutput/testout','./tmpoutput/mySimulatedTest.out')


def testgetParamString():
	str1=' GMNMX     1   5.496109E-04'
	str2=' GMNMX         8.573930E-01'
	str3=" IFORMT\n (1E2.3)"

	assert getParamString('GMNMX',1,5.496109E-04)==str1
	assert getParamString('GMNMX',"",8.573930E-01)==str2

	assert getParamString('IFORMT',"",'(1E2.3)')==str3

if __name__=="__main__":

	testgenInputFile('paramTemplate.txt')
	alldata=readCONTINoutput(testfile4)

	for i,data in enumerate(alldata):
		plt.semilogx(data[:,2],data[:,0],hold=True)
		
#		plt.savefig("./output/test"+str(i)+".png")
#		plt.close()
	

	plt.xlabel("emission rate(s^-1)")
	plt.ylabel("amplitude")
	plt.savefig("./tmpoutput/test.png")
	

