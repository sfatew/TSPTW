import sys
import numpy as np
from io import StringIO
from ortools.sat.python import cp_model
import time

with open("data/data5.txt", "r") as f:  
  data= f.read()

sys.stdin=StringIO(data)
c=[[0,0,0]]
T=[]
n=[int(x) for x in sys.stdin.readline().split()]    #number of city
n=n[0]
for i in range(n):
    time_required=[int(x) for x in sys.stdin.readline().split()]           # e(i)=[0]   l(i)=[1]   d(i)=[2]
    c.append(time_required) 
for i in range(n+1):
    time_travel=[int(x) for x in sys.stdin.readline().split()]             # array r
    T.append(time_travel) 
T=np.array(T)               #time travel matrix

model=cp_model.CpModel()