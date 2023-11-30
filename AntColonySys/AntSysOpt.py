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

route=[0 for i in range(n+1)]  #route

visited=[ False for i in range(n+1)]    # mark came points

pheromone=np.full((n+1,n+1),0.2)           # matrix of pheromone at each arc

evaporation= 0.3                        # evaporation rate

prob=np.array([0 for i in range(n+1)])          # prob to go from i to the next node

delta_pheromone=np.zeros((n+1,n+1))

timeTaken=0


def pheromoneUpdate(i,j):
    pheromone = pheromone * (1-evaporation) + delta_pheromone

def route_construction(k,i):        
                                    # 1st k : ant kth  (NOTE: ant k start at node k)
                                    # later k : the current node
                                    # i : interation(for recursion) 
    global timeTaken

    visited[k]=True
    route[i]=k
    timeTaken=timeTaken + T[route[i-1]][route[i]] 
    timeTaken=max(timeTaken,c[k][0])+ c[k][2]           # time that finished service at node k
    
    next=path_chosing(k)
    if i!=n+1:
        route_construction(next,i+1)



def path_chosing(j):            #j : we are at the gth node of the route 
    for i in range(n):
        if visited[i]==False:
            #update the prob of chosing the next node 
            # alpha = 1, beta = 1
            prob[i]= (pheromone**1 * (1/T[j][i])**1)     
    # try:
    prob=prob/sum(prob)
    next=np.random.choice(np.arange(0,(n+1)),p=prob)
    prob=[0 for i in prob]
    # except ZeroDivisionError:
    #     next= route[0]

    return next

def AntSys():


    while:
    
        delta_pheromone=0
        for k in range(n+1):
            route_construction(k,0)
