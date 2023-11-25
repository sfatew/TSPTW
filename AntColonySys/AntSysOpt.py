import numpy as np
import sys
from io import StringIO
import random
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

s=[0 for i in range(n+1)]  #route

t_i=0   # the time at which the salesman arrived at node i

visited=[ False for i in range(n+1)]    # mark came points

pheromone=np.full((n+1,n+1),0.2)           # matrix of pheromone at each arc

evaporation= 0.3                        # evaporation rate

prob=np.array([0 for i in range(n+1)])          # prob to go from i to the next node

def pheromoneUpdate(i,j):

    pheromone[i][j] = pheromone[i][j] * (1-evaporation) + delta_pheromone[i][j]

def route_construction(k):        
                                    #k : ant kth  (NOTE: ant k start at node k)
    s[0]=k
    visited[k]=True
    for i in range(n):
        if visited[i]==False:
            pass

def path_chosing(j):            #j : we are at the gth node of the route 
    for i in range(n):
        if visited[i]==False:
            #update the prob of chosing the next node 
            # alpha = 1, beta = 1
            prob[i]= (pheromone**1 + (1/T[j][i])**1)     

    prob=prob/sum(prob)
    a=random.random()
    


