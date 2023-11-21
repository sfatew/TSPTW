import numpy as np
import sys
from io import StringIO
import json

with open("data.json", "r") as read_file:
    data = json.loads(read_file)

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

pheromone=np.zeros((n+1,n+1))           # matrix of pheromone at each arc

evaporation= 0.5                        # evaporation rate



def route_construction():
    pass