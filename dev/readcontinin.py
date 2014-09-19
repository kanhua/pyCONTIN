"""The file analyses contin.in"""
import numpy as np
import matplotlib.pyplot as plt

testfile="./CONTINplugin/contin_part1.in"



def readContinFile(filename):
   """Quick and dirty implementation
   Note that python does not support strint to 
   numercial conversion like float(1.) or float(-1.)"""
   fileobj=open(filename,'r');
   yk=list()
   
   readYFlag=False
   
   tarr=None;
   yarr=None;
   
   for lineNum, line in enumerate(fileobj):
      if readYFlag==False:
         if str.strip(line)=='END':
            readYFlag=True
            continue;
         
         items=line.split()
         if len(items) >1:
            if items[0]=='NINTT':
               NINTT=int(items[1])

            if items[0]=='END':
               readYFlag=True
      elif readYFlag==True:
         items=line.split()
         
         if items[0]=='NSTEND':
            readinArray=map(float, items[1:])
            nums,start,end=readinArray;
            if tarr is None:
               tarr=np.linspace(start, end, num=nums)
            else:
               tarr=np.concatenate((tarr,np.linspace(start,end,num=nums)))
               
         else:
 
            convItems=map(float,items)
            
            if yarr==None:
               yarr=np.array(convItems)
            else:
               yarr=np.concatenate((yarr,np.array(convItems)))
   
   
   print tarr
   print yarr
   
   assert tarr.shape==yarr.shape
   return tarr,yarr



if __name__=="__main__":
   t,y=readContinFile(testfile)
   
   plt.plot(t,y)
   plt.show()
   
   
   
      

