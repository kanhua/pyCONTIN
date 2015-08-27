"""This script compares the calcualted time constants by using DISCRETE 
fitting and Fourier coefficients calculated by DLTS software
data: '/Users/kanhua/Dropbox/Experiment data drive/TTI data/20140729 GaAsN DLTS/G240DS.T1A'
Date: Sep, 2014, by K.-H. """


print (__doc__)
import numpy as np;
from capFileUtil import *
import matplotlib.pyplot as plt


filetoprocess=''

cp=capTempScan('/Volumes/KHDISK/S1.T1A',mode='binary')
tau=cp.calcTau()
tau2=cp.calcTau('a1a2')
tau3=cp.calcTau('a2b2')
tau4=cp.calcTau('b1b2')




temperature=cp.PTVMatrix[:,0]
plt.plot(temperature,cp.b1,'o',hold=False)
plt.show()
plt.close()


filedir="/Volumes/KHDISK/S1/"

objlist=readcvindir(filedir,capTime,mode='binary')

temperature=list()
fittedlambda=list()
for oj in objlist:
	oj.fitExp()
	fittedlambda.append(oj.resultSet[0][2][1])
	                                    
	temperature.append(oj.temperature)
	
fittedlambda=np.array(fittedlambda)
t2=np.array(temperature)



temperature=cp.PTVMatrix[:,0]
plt.semilogy(1000/temperature,tau*np.power(temperature,2),'.-',label='a1b1',hold=True);
plt.semilogy(1000/temperature,tau2*np.power(temperature,2),'.-',label='a1a2')
plt.semilogy(1000/temperature,tau3*np.power(temperature,2),'.-',label='a2b2')
plt.semilogy(1000/temperature,tau4*np.power(temperature,2),'.-',label='b1b2')

plt.semilogy(1000/t2,1/fittedlambda*np.power(t2,2),'.',label='1 expfit')

plt.xlabel("1000/T (K^-1)")
plt.ylabel("timeConst*T^2")

plt.legend()

plt.show()