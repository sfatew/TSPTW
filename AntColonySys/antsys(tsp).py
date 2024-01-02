import random as rn
import numpy as np
from numpy.random import choice as np_choice, rand
import sys
from io import StringIO
from collections import deque
from time import process_time, sleep

class AntColony(object):

    def __init__(self, distances, n_ants, n_best, n_iterations, persistence, alpha=1, beta=1, qo=0.5):
        """
        Args:
            distances (2D numpy.array): Square matrix of distances. Diagonal is assumed to be np.inf.
            n_ants (int): Number of ants running per iteration
            n_best (int): Number of best ants who deposit pheromone
            n_iteration (int): Number of iterations
            persistence (float): Rate it which pheromone persistences. The pheromone value is multiplied by persistence, persistence=(1-decay).
            alpha (int or float): exponenet on pheromone, higher alpha gives pheromone more weight. Default=1
            beta (int or float): exponent on distance, higher beta give distance more weight. Default=1
            max,min pheromone : pheromone is bounded in the interval (min,max)
            numconvergence : number of convergence (convergence is when 1 of the fesible edge is max pheromone while the rest is min)
            
        Example:
            ant_colony = AntColony(german_distances, 100, 20, 2000, 0.95, alpha=1, beta=2)          
        """
        self.distances  = distances
        self.pheromone = np.full(self.distances.shape, 9999)
        self.all_inds = range(len(distances))
        self.n_ants = n_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.persistence = persistence
        self.alpha = alpha
        self.beta = beta
        self.qo = qo
        self.maxpheromone = 0
        self.minpheromone = 0
        # self.numconvergence = 0

    def run(self):
        shortest_path = None
        all_time_shortest_path = ("placeholder", np.inf)

        interations = self.n_iterations
        i=0

        q=rand()

        while i < interations:
        # while self.numconvergence < len(self.distances):
        #     self.numconvergence = 0
            all_paths = self.gen_all_paths()

            shortest_path = min(all_paths, key=lambda x: x[1])
            print(shortest_path)
            sleep(0.1)
            if shortest_path[1] < all_time_shortest_path[1]:
                all_time_shortest_path = shortest_path  

                interations += self.n_iterations
                print(interations)

                # self.maxpheromone = (1/(1-self.persistence)) * (1/all_time_shortest_path[1])
                # self.minpheromone = self.maxpheromone/(2* len(self.distances))
                print(all_time_shortest_path[1])

            self.pheromone = self.pheromone * self.persistence  
            if q>self.qo:
                self._spread_pheronome(all_paths, self.n_best)
            else:
                self._spread_pheronome_gb(all_time_shortest_path)

            i+=1

            # print(self.numconvergence)
        return all_time_shortest_path

    def _spread_pheronome(self,all_paths, n_best):
        sorted_paths = sorted(all_paths, key=lambda x: x[1])
        for path, dist in sorted_paths[:n_best]:
            for move in path:
                self.pheromone[move] += 1.0 / dist
                # if self.pheromone[move] > self.maxpheromone:
                #     self.pheromone[move] = self.maxpheromone
                # if self.pheromone[move] < self.minpheromone:
                #     self.pheromone[move] = self.minpheromone

    def _spread_pheronome_gb(self,all_time_shortest_path):
        path, dist = all_time_shortest_path
        for move in path:
                self.pheromone[move] += 1.0 / dist
                # if self.pheromone[move] > self.maxpheromone:
                #     self.pheromone[move] = self.maxpheromone
                # if self.pheromone[move] < self.minpheromone:
                #     self.pheromone[move] = self.minpheromone


    def gen_path_dist(self, path):
        total_dist = 0
        for ele in path:
            total_dist += self.distances[ele]
        return total_dist

    def gen_all_paths(self):
        all_paths = []
        # for i in range(self.n_ants):
        path = self.gen_path(0)
        all_paths.append((path, self.gen_path_dist(path)))
        return all_paths


    def gen_path(self, start):
        path = []
        start=start%(len(self.distances))
        visited = set()
        visited.add(start)
        prev = start
        for _ in range(len(self.distances) - 1):
            move = self.pick_move(self.pheromone[prev], self.distances[prev], visited)
            path.append((prev, move))
            prev = move
            visited.add(move)
        path.append((prev, start)) # going back to where we started    
        return path

    def pick_move(self, pheromone, dist, visited):

        pheromone = np.copy(pheromone)
        pheromone[list(visited)] = 0

        # minnode=0
        # maxnode=0
        # pheromone = list(pheromone)
        # for node in range(len(pheromone)):
        #     if pheromone[node] != 0:
        #         if pheromone[node] == self.minpheromone:
        #             minnode += 1
        #         if pheromone[node] == self.maxpheromone:
        #             maxnode += 1
        # if maxnode == 1 and minnode == len(pheromone) - len(visited) - 1 and minnode != 0:
        #     # print(self.maxpheromone)
        #     # print(minnode)
        #     # print(pheromone)
        #     # print(pheromone.index(self.maxpheromone))
        #     self.numconvergence += 1 
        #     return pheromone.index(self.maxpheromone)
        # pheromone=np.array(pheromone)

        row = pheromone ** self.alpha * (( 1.0 / dist) ** self.beta)
        # print(row)
        norm_row = row / row.sum()
        move = np_choice(self.all_inds, 1, p=norm_row)[0]

        return move

    # def pick_best(self, pheromone,dist, visited):
    #     pheromone = np.copy(pheromone)
    #     pheromone[list(visited)] = 0
    #     row = pheromone ** self.alpha * (( 1.0 / dist) ** self.beta)
    #     move=np.argmax(row)
    #     return move
    
    # def best_path(self,pheromone):
    #     path = []
    #     visited = set()
    #     visited.add(0)
    #     prev = 0
    #     for i in range(len(self.distances) - 1):
    #         move = self.pick_best(self.pheromone[prev],self.distances[prev], visited)
    #         path.append((prev, move))
    #         prev = move
    #         visited.add(move)
    #     path.append((prev, 0)) # going back to where we started    
    #     return path


with open("data/tspdata128.txt", "r") as f:  
  data= f.read()

sys.stdin=StringIO(data)
c=[]
n=[int(x) for x in sys.stdin.readline().split()]    #number of city
n=n[0]
for i in range(n):
    d=[int(x) for x in sys.stdin.readline().split()]    
    d[i]=np.inf
    c.append(d) 

distances=np.array(c)   

begin=process_time()
ant_colony = AntColony(distances, 5*n, 1, 100, 0.4, alpha=1, beta=4, qo=0.3)
shortest_path = ant_colony.run()
path, dist = shortest_path
path = deque(path)
while path[0][0] != 0:
    path.rotate(-1)

print(f"shortest path {path}, distance {dist}")
finish=process_time()

print('time taken', finish-begin)