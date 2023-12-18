import sys
import numpy as np
from io import StringIO
import time

def greedy(T,c):
   # find min route
    sum = 0
    counter = 0
    j = 0
    i = 0
    min = 
 
    # Starting from the 0th indexed
    # city i.e., the first city
    visited[0] = 1
    route = [0] * len(tsp)
 
    # Traverse the adjacency
    # matrix tsp[][]
    while i < len(tsp) and j < len(tsp[i]):
 
        # Corner of the Matrix
        if counter >= len(tsp[i]) - 1:
            break
 
        # If this path is unvisited then
        # and if the cost is less then
        # update the cost
        if j != i and (visited[j] == 0):
            if tsp[i][j] < min:
                min = tsp[i][j]
                route[counter] = j + 1
 
        j += 1
 
        # Check all paths from the
        # ith indexed city
        if j == len(tsp[i]):
            sum += min
            min = INT_MAX
            visited[route[counter] - 1] = 1
            j = 0
            i = route[counter] - 1
            counter += 1
 
    # Update the ending city in array
    # from city which was last visited
    i = route[counter - 1] - 1
 
    for j in range(len(tsp)):
 
        if (i != j) and tsp[i][j] < min:
            min = tsp[i][j]
            route[counter] = j + 1
 
    sum += min
 
    # Started from the node where
    # we finished as well.
    print("Minimum Cost is :", sum)
 


if __name__ == '__main__':
    with open("data/data5.txt", "r") as f:  
        data= f.read()

    sys.stdin=StringIO(data)
    c=[[0,0,0]]
    T=[]
    n=[int(x) for x in sys.stdin.readline().split()]    #number of city
    n=n[0]
    for i in range(n):
        time_required=[int(x) for x in sys.stdin.readline().split()]           # start=[0]   end=[1]   service=[2]
        c.append(time_required) 
    for i in range(n+1):
        time_travel=[int(x) for x in sys.stdin.readline().split()]             # array r
        T.append(time_travel) 
    T=np.array(T)               #time travel matrix


    visited=[ 0 for i in range(n+1)]    # mark came points