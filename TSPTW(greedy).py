import sys
import numpy as np
from io import StringIO
import time

def greedy(T,c):
    '''travel from i to a node j
    node j define by choseing the node with the lowest start serving time'''

    global time_taken

    visited=[ 0 for i in range(cities+1)]    # mark came points

    arrived = 0   # the time at which the salesman arrived at node i

    start_service=0           # the time at which the salesman start service at node i

    counter = 0        # number of city we have visited

    next=0          # the next node chosen by greedy

    # Starting from the 0th indexed city i.e., the first city
    visited[0] = 1

    while True:
        min = np.inf

        counter+=1
        a=[0]
        if counter > cities:
            break

        for city in range(1,cities+1):
            # print(start_service) 
            a[0]=start_service
            if visited[city]==0:     
                arrived = a[0]+ c[route[counter-1]][2]+ T[route[counter-1]][city]   
                # slack = c[city][1] - arrived

                a[0]= max(c[city][0], arrived)    # start service time 
                # # print(a[0])
                if a[0] > c[city][1]:
                    raise ValueError('exceed time limit at node',city)
                # hold = a[0]

                if a[0] < min and a[0] > 0:
                    min = a[0]
                    # save = hold
                    next = city
                    # print(next)
   
        # print('.')
        visited[next] = 1
        route[counter] = next
        start_service = min
        time_taken = start_service

    time_taken = time_taken + c[route[-1]][2] + T[route[-1]][0]

if __name__ == '__main__':
    with open("data/data10.txt", "r") as f:  
        data= f.read()

    sys.stdin=StringIO(data)
    c=[[0,0,0]]
    T=[]
    cities=[int(x) for x in sys.stdin.readline().split()]    #number of city
    cities=cities[0]
    for i in range(cities):
        time_required=[int(x) for x in sys.stdin.readline().split()]           # start=[0]   end=[1]   service=[2]
        c.append(time_required) 
    for i in range(cities+1):
        time_travel=[int(x) for x in sys.stdin.readline().split()]             # array r
        T.append(time_travel) 
    T=np.array(T)               #time travel matrix

    route = [0 for i in range(cities+1)]
    time_taken = 0

    begin=time.time()
    greedy(T,c)
    print(route)
    print(time_taken)
    finish=time.time()

    print('time taken', finish-begin)