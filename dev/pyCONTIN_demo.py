# ## This example file demonstrates how to use pyCONTIN wrapper

# Load the required packages
import numpy as np
import matplotlib.pyplot as plt
from CONTINWrapper import *

# #### Load example transient file

trans_data=np.loadtxt("demo_input.csv")

# #### Assign template file

template_file="paramTemplate.txt"


fp=open("paramTemplate.txt",'r')


alldata=runCONTINfit(trans_data[:,0],trans_data[:,1],template_file)

testxdata=alldata[0][1][:,2]

testydata=alldata[0][1][:,0]

plt.plot(testxdata,testydata)

plt.show()

