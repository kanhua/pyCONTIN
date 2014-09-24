import re
import numpy as np
import matplotlib.pyplot as plt
from os.path import join
from CONTINWrapper import *
from capFileUtil import capTime



def testExperimentFile(templateFile):
    filepath='/Users/kanhua/Dropbox/Experiment data drive/TTI data/20140910 GaAsN test DLTS/OMARS1'
    filepath2='/Users/kanhua/Dropbox/Experiment data drive/TTI data/20140910 GaAsN test DLTS/'

    cp=capTime(join(filepath,'T012.Y1A'))

    xdata=cp.time
    ydata=-cp.capTrans

    plt.plot(xdata,ydata)
    plt.show()

    alldata=runCONTINfit(xdata,ydata,templateFile)

    for i,data in enumerate(alldata):
        plt.semilogx(data[1][:,2],data[1][:,0],hold=True)

        plt.xlabel("emission rate(s^-1)")
        plt.ylabel("amplitude")
        plt.title("alpha %s"%data[0][1])
        
        plt.savefig("./tmpoutput/test"+str(i)+".png")


        plt.close()



if __name__=="__main__":
    #testgenInputFile('paramTemplate.txt')
    testExperimentFile('paramTemplate.txt');
