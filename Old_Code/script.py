import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas import Series, DataFrame

arr=arr=pd.read_csv("knosab.csv",encoding="utf-8-sig")
#arr=arr=pd.read_csv("kwithsab.csv",encoding="utf-8-sig")
df=arr
df.sort(columns=' Avg E',ascending=1)

#df.to_csv('knosab_org.csv')
#df.to_csv('kwithsab_org.csv')

#arr=np.fromfile("knosab.csv",dtype=float,count=-1,sep=',')


#x=np.reshape(arr[:,0],(-1,1))
#c1=np.reshape(arr[:,1],(-1,1))
#c9=np.reshape(arr[:,5],(-1,1))


#np.savetxt('test.txt', c1, delimiter=',')
#poop=np.vstack([x,c1])
#poop=np.concatenate((x,c9),axis=1)
#np.savetxt('test.txt', poop, fmt='%1.6E', delimiter=' , ')
#arr.to_csv()
