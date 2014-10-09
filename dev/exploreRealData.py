"""This file for exploratory analysis of read experiment transient data"""


import numpy as np
import matplotlib.pyplot as plt
from CONTINWrapper import *
from capFileUtil import *
from scipy.signal import argrelmax


filedir3="/Users/kanhua/Dropbox/Experiment data drive/TTI data/20141003 GaAsN DLTS/S2/"

objlist=readcvindir(filedir3,capTime,mode='binary')


temperature=list()
fittedlambda=list()


testobj=objlist[1]

templateFile='paramTemplateForRealData.txt'

xdata=testobj.time
ydata=testobj.capTrans

alldata=runCONTINfit(xdata,ydata,templateFile)


for i,data in enumerate(alldata):
    plt.semilogx(data[1][:,2],data[1][:,0],hold=True)
    


    plt.xlabel("emission rate(s^-1)")
    plt.ylabel("amplitude")
    plt.title("alpha %s"%data[0][1])
    
    plt.savefig("./tmpoutput/test"+str(i)+".png")


    plt.close()

	