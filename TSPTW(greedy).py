import sys
import numpy as np
from io import StringIO
import time

def greedy(T,c):
    '''travel from i to a node j
    node j define by choseing the node with the lowest start serving time'''

    global time_taken

    visited=[ 0 for i in range(n+1)]    # mark came points

    t_i=0   # the time at which the salesman arrived at node i

    t1_i=0           # the time at which the salesman start service at node i

    counter = 0        # number of city we have visited

    next=0          # the next node chosen by greedy

    # Starting from the 0th indexed city i.e., the first city
    visited[0] = 1

    while True:
        min = np.inf

        counter+=1
        a=[0]
        if counter > n:
            break

        for j in range(1,n+1):
            # print(t1_i) 
            a[0]=t1_i
            if visited[j]==0:       
                t_i= a[0]+ c[route[counter-1]][2]+ T[route[counter-1]][j]   
                a[0]= max(c[j][0], t_i)     
                # print(a[0])
                if a[0] > c[j][1]:
                    raise ValueError('exceed time limit at node',j)

                if a[0] < min:
                    min = a[0]
                    next=j
                    # print(next)
   
        visited[next] = 1
        route[counter] = next
        t1_i = min
        time_taken = t1_i

    time_taken = time_taken + c[route[-1]][2] + T[route[-1]][0]

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

    route = [0 for i in range(n+1)]
    time_taken = 0

    begin=time.time()
    greedy(T,c)
    print(route)
    print(time_taken)
    finish=time.time()

    print('time taken', finish-begin)