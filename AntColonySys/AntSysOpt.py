import numpy as np
import sys
from io import StringIO
import time

with open("data5.txt", "r") as f:  
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

# print(c)
# print(T)

s=[0 for i in range(n+1)]  #solution

t_i=0   # the time at which the salesman arrived at node i

visited=[ False for i in range(n+1)]    # mark came points

pheromone=np.full((n+1,n+1),0)           # matrix of pheromone at each arc

evaporation= 0.3                        # evaporation rate

def pheromoneUpdate(i,j):
    global pheromone
    pheromone[i][j] = pheromone[i][j] * (1-evaporation) + 

def route_construction():
    pass