import random as rn
import numpy as np
from numpy.random import choice as np_choice, rand
import sys
from io import StringIO
from time import process_time

class AntColony(object):

    def __init__(self, distances, n_ants, n_best, n_iterations, decay, alpha=1, beta=1):
        """
        Args:
            distances (2D numpy.array): Square matrix of distances. Diagonal is assumed to be np.inf.
            n_ants (int): Number of ants running per iteration
            n_best (int): Number of best ants who deposit pheromone
            n_iteration (int): Number of iterations
            decay (float): Rate it which pheromone decays. The pheromone value is multiplied by decay, so 0.95 will lead to decay, 0.5 to much faster decay.
            alpha (int or float): exponenet on pheromone, higher alpha gives pheromone more weight. Default=1
            beta (int or float): exponent on distance, higher beta give distance more weight. Default=1

        Example:
            ant_colony = AntColony(german_distances, 100, 20, 2000, 0.95, alpha=1, beta=2)          
        """
        self.distances  = distances
        self.pheromone = np.ones(self.distances.shape) / len(distances)
        self.all_inds = range(len(distances))
        self.n_ants = n_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta
        self.qo = 0

    def _qo(self, interation, interations):
        return interation/interations

    def run(self):
        shortest_path = None
        all_time_shortest_path = ("placeholder", np.inf)
        interations = self.n_iterations
        i=0

        while i < interations:
            self.qo=self._qo(i, interations)
            print(self.qo)
            all_paths = self.gen_all_paths()
            self.spread_pheronome(all_paths, self.n_best)

            self.pheromone = self.pheromone * self.decay  

            path=self.best_path(self.pheromone)
            shortest_path = [path,self.gen_path_dist(path)] 

            # shortest_path = min(all_paths, key=lambda x: x[1])
            if shortest_path[1] < all_time_shortest_path[1]:
                all_time_shortest_path = shortest_path  
                interations += self.n_iterations
                print(interations)
            print(all_time_shortest_path)
            i+=1
        return all_time_shortest_path

    def spread_pheronome(self,all_paths, n_best):
        sorted_paths = sorted(all_paths, key=lambda x: x[1])
        for path, dist in sorted_paths[:n_best]:
            for move in path:
                self.pheromone[move] += 1.0 / self.distances[move]

    def gen_path_dist(self, path):
        total_dist = 0
        for ele in path:
            total_dist += self.distances[ele]
        return total_dist

    def gen_all_paths(self):
        all_paths = []
        for i in range(self.n_ants):
            path = self.gen_path(i)
            all_paths.append((path, self.gen_path_dist(path)))
        return all_paths

    def gen_path(self, start):
        path = []
        start=start%(len(self.distances))
        visited = set()
        visited.add(start)
        prev = start
        for i in range(len(self.distances) - 1):
            move = self.pick_move(self.pheromone[prev], self.distances[prev], visited)
            path.append((prev, move))
            prev = move
            visited.add(move)
        path.append((prev, start)) # going back to where we started    
        return path

    def pick_move(self, pheromone, dist, visited):
        q=rand()
        pheromone = np.copy(pheromone)
        pheromone[list(visited)] = 0

        row = pheromone ** self.alpha * (( 1.0 / dist) ** self.beta)
        if q>self.qo:
            norm_row = row / row.sum()
            move = np_choice(self.all_inds, 1, p=norm_row)[0]
        else:
            move=np.argmax(row)
        return move

    def pick_best(self, pheromone,dist, visited):
        pheromone = np.copy(pheromone)
        pheromone[list(visited)] = 0
        row = pheromone ** self.alpha * (( 1.0 / dist) ** self.beta)
        move=np.argmax(row)
        return move
    
    def best_path(self,pheromone):
        path = []
        visited = set()
        visited.add(0)
        prev = 0
        for i in range(len(self.distances) - 1):
            move = self.pick_best(self.pheromone[prev],self.distances[prev], visited)
            path.append((prev, move))
            prev = move
            visited.add(move)
        path.append((prev, 0)) # going back to where we started    
        return path


with open("data/tspdata15.txt", "r") as f:  
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
ant_colony = AntColony(distances, n, 1, 20, 0.9, alpha=2, beta=1)
shortest_path = ant_colony.run()
print ("shorted_path: {}".format(shortest_path))
finish=process_time()

print('time taken', finish-begin)