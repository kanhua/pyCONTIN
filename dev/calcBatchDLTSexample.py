"""
This script do the inverse Lapalce transform of some simulated capcitance transients
with the following steps:
    1. simulate the capacitance transients
    2. plot the individual capacitance transients at each temperature
    3. plot the spectrum of inverse Laplace transform of each simulated capacitance transient
    (In this expample, we only select the first set (the one with smallest alpha) of the Laplace transients)
    4. Plot the fitted emission rates and simulated emission rates in a single Arrehnius plot

Date created: 2014/09/23 by K. H. Lee
"""


import numpy as np
import matplotlib.pyplot as plt
from CONTINWrapper import *
from capFileUtil import capTime
from scipy.signal import argrelmax


templateFile='paramTemplate.txt'
testTemperature=100
paramList=readInputParamFromFile(templateFile)  

tp=trapLevel([0.08,0.1])

temperaturesForGrpahOutput=np.linspace(100,300,10)

result=[]
for testTemperature in np.linspace(100,300,10):
    xdata,ydata=tp.getTransient(T=testTemperature,plotGraph=False,gridnum=100)

    emRates=tp.emRateT(testTemperature)

    alldata=runCONTINfit(xdata,ydata,templateFile)

    testxdata=alldata[0][1][:,2]

    testydata=alldata[0][1][:,0]

    testErrBar=alldata[0][1][:,1]

    relMaxIdx=argrelmax(testydata)

    # plot graphs of transients
    if testTemperature in temperaturesForGrpahOutput:
        fig, axs = plt.subplots(nrows=2, ncols=1, sharex=False)
        ax=axs[0]
        ax.plot(xdata,ydata)
        ax.legend(['transient at %s K'%testTemperature],loc='best')
        ax.set_xlabel('time (s)')
        ax.set_ylabel('simulated capacitance')

        ax=axs[1]
        ax.semilogx(testxdata,testydata)
        ax.legend(['Laplace spectrum'],loc='best')
        ax.set_xlabel('emission rate(s^-1)')
        ax.set_ylabel('amplitude')
        plt.savefig('./tmpoutput/trans_and_spectrum_%s_K.pdf'%testTemperature)
        plt.close()



    if len(relMaxIdx[0])!=len(emRates):
        print "warning: the number of fitted emission rates do not match the number of the theoretical one"


    result.append(np.concatenate(([testTemperature],
        testxdata[relMaxIdx[0]],testErrBar[relMaxIdx[0]],
        emRates)))


# Plot the emission rates in a single Arrehnius plot

result=np.array(result)

plt.semilogy(1/result[:,0],result[:,1],'o',scaley='log',hold=True,label="fitted em 1")
plt.semilogy(1/result[:,0],result[:,2],'o',scaley='log',hold=True,label="fitted em 2")
plt.semilogy(1/result[:,0],result[:,5],'--',hold=True,label='theoretical em 1')
plt.semilogy(1/result[:,0],result[:,6],'--',hold=True,label='theoretical em 2')
plt.xlabel("1/T")
plt.legend(loc='lower left')
plt.ylabel("emission rate(s^-1)")

plt.savefig("./tmpoutput/arrplot.pdf")
plt.show()


plt.close()


