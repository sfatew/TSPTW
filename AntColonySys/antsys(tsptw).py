import random as rn
import numpy as np
from numpy.random import choice as np_choice, rand
import sys
from io import StringIO
from time import process_time

class AntColony(object):

    def __init__(self, time_travel, time_window, n_ants, n_best, n_iterations, decay, alpha=1, beta=1,gamma=1, qo=0.5):
        """
        Args:
            time_travel (2D numpy.array): Square matrix of time_travel. Diagonal is assumed to be np.inf.
            n_ants (int): Number of ants running per iteration
            n_best (int): Number of best ants who deposit pheromone
            n_iteration (int): Number of iterations
            decay (float): Rate it which pheromone decays. The pheromone value is multiplied by decay, so 0.95 will lead to decay, 0.5 to much faster decay.
            alpha (int or float): exponenet on pheromone, higher alpha gives pheromone more weight. Default=1
            beta (int or float): exponent on distance, higher beta give distance more weight. Default=1

        Example:
            ant_colony = AntColony(german_time_travel, 100, 20, 2000, 0.95, alpha=1, beta=2)          
        """
        self.time_travel  = time_travel
        self.time_window = time_window
        self.pheromone = np.ones(self.time_travel.shape) / len(time_travel)
        self.all_inds = range(len(time_travel))
        self.n_ants = n_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta
        self.gamma=gamma
        self.qo= qo
        self.maxpheromone = 0
        self.minpheromone = 0
        # self.numconvergence = 0
        self.time=0     #current travel time

    def run(self):
        shortest_path = None
        all_time_shortest_path = ("placeholder", np.inf)

        
        for i in range(self.n_iterations):
            all_paths = self.gen_all_paths()
            shortest_path = min(all_paths, key=lambda x: x[1])
            self.spread_pheronome(all_paths, self.n_best, shortest_path=shortest_path)
            if shortest_path[1] < all_time_shortest_path[1]:
                all_time_shortest_path = shortest_path            
            self.pheromone = self.pheromone * self.decay            
        return all_time_shortest_path


    def spread_pheronome(self, all_paths, n_best, shortest_path):
        sorted_paths = sorted(all_paths, key=lambda x: x[1])
        for path, time in sorted_paths[:n_best]:
            for move in path:
                self.pheromone[move] += 1.0 / time

    def gen_time_taken(self, i):     
        #i=(prev, move)
        #caculate time finish service at node that we move to
        self.time +=self.time_travel[i]
        if self.time < self.time_window[i[1]][0]:
            self.time=self.time_window[i[1]][0]
            self.time+=self.time_window[i[1]][2]
        else:
            self.time+=self.time_window[i[1]][2]
        return self.time

    def gen_all_paths(self):
        all_paths = []
        for i in range(self.n_ants):
            self.time=0
            path = self.gen_path(0)
            all_paths.append((path, self.time))
        return all_paths

    def gen_path(self, start):
        path = []
        start=start%(len(self.time_travel))
        visited = set()
        visited.add(start)
        prev = start
        for i in range(len(self.time_travel) - 1):
            move = self.pick_move(self.pheromone[prev], self.time_travel[prev], visited)
            path.append((prev, move))
            self.gen_time_taken((prev, move))
            prev = move
            visited.add(move)
            
        path.append((prev, start)) # going back to where we started    
        return path

    def pick_move(self, pheromone, time, visited):
        q=rand()
        pheromone = np.copy(pheromone)
        pheromone[list(visited)] = 0

        row = pheromone ** self.alpha * (( 1.0 / time) ** self.beta)
        if q>self.qo:
            norm_row = row / row.sum()
            move = np_choice(self.all_inds, 1, p=norm_row)[0]
        else:
            move=np.argmax(row)
        return move

    def Local_heuristic():
        pass

with open("data/data10.txt", "r") as f:  
  data= f.read()

sys.stdin=StringIO(data)
T=[]
c=[[0,0,0]]
n=[int(x) for x in sys.stdin.readline().split()]    #number of city
n=n[0]
for i in range(n):
    time_required=[int(x) for x in sys.stdin.readline().split()]           # start=[0]   end=[1]   service=[2]
    c.append(time_required) #time window matrix
for i in range(n):
    d=[int(x) for x in sys.stdin.readline().split()]    
    d[i]=np.inf
    T.append(d) 

time_travel=np.array(T)   
time_window=np.array(c)

begin=process_time()
ant_colony = AntColony(time_travel,time_window, 10, 1, 100, 0.6, alpha=1, beta=3, gamma=3, qo=0)
shortest_path = ant_colony.run()
print ("shorted_path: {}".format(shortest_path))
finish=process_time()

print('time taken', finish-begin)