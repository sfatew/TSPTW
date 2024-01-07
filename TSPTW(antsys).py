import random as rn
import numpy as np
from numpy.random import choice as np_choice, rand, randint
import sys
from io import StringIO
from time import process_time, sleep
from plot import plot


class AntColony(object):

    def __init__(self, time_travel, time_window, n_ants, n_best, n_iterations, persistence, alpha=1, beta=1,gamma=1, epsilon=1, qo=0.5):
        """
        Args:
            time_travel (2D numpy.array): Square matrix of time_travel. Diagonal is assumed to be np.inf.
            time_window : the time window constrain, the window of node 0 is set to [0,0,0]
            n_ants (int): Number of ants running per iteration
            n_best (int): Number of best ants who deposit pheromone
            n_iteration (int): Number of iterations
            persistence (float): Rate it which pheromone persistences. The pheromone value is multiplied by persistence, persistence=(1-decay).
            alpha (int or float): exponenet on pheromone, higher alpha gives pheromone more weight. Default=1
            beta (int or float): exponent on distance, higher beta give distance more weight. Default=1

        Example:
            ant_colony = AntColony(german_time_travel, 100, 20, 2000, 0.95, alpha=1, beta=2)          
        """
        self.time_travel  = time_travel
        self.time_window = time_window
        self.pheromone = np.full(self.time_travel.shape, 9999, dtype='float64')
        self.all_inds = range(len(time_travel))
        self.n_ants = n_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.persistence = persistence
        self.alpha = alpha
        self.beta = beta
        self.gamma=gamma
        self.epsilon = epsilon
        self.qo= qo     

        self.time=0     #current travel time
        self.penalty = self._find_penalty()

    def _find_penalty(self):
        max_timetravel = 0
        for i in self.time_travel:
            for j in i:
                if j> max_timetravel:
                    max_timetravel = j

        max_timewindow = 0
        for j in self.time_window[:,2]:
                if j> max_timewindow:
                    max_timewindow = j

        return (max_timetravel + max_timewindow) * len(self.time_travel) 
                    

    def run(self):
        # print(self.time_travel)
        print(self.penalty)
        sleep(1)
        shortest_path = None
        all_time_shortest_path = ("placeholder", np.inf)
        all_time_best_fail_path = ("placeholder", np.inf)

        interations = self.n_iterations
        i=0

        # q=rand()
        fail_counter = 0

        while i < interations:

            print(fail_counter)
            all_paths, fail_path = self.gen_all_paths()
            # plotlen = []

            if len(fail_path) != 0:
                best_fail_path = min(fail_path, key=lambda x: x[1])
                print(best_fail_path)
                print('len ',len(best_fail_path[0]))
                # plotlen.append(len(best_fail_path[0]))
                # plot(plotlen)
                
                if best_fail_path[1] <= all_time_best_fail_path[1]:
                    all_time_best_fail_path = best_fail_path 
                    print('.')

            if len(all_paths) == 0:
                fail_counter += 1

                self.pheromone = self.pheromone * self.persistence 

                self._spread_pheronome(fail_path, self.n_best)

                self._spread_pheronome_gb(all_time_best_fail_path)

                if fail_counter > 999:
                    print(all_time_best_fail_path)
                    break
                else:
                    continue
            else:
                fail_counter = 0 
                shortest_path = min(all_paths, key=lambda x: x[1])
                print(shortest_path)
                if shortest_path[1] < all_time_shortest_path[1]:
                    all_time_shortest_path = shortest_path  

                    interations += self.n_iterations
                    print(interations)

                    print(all_time_shortest_path[1])
                
                self.pheromone = self.pheromone * self.persistence 


                self._spread_pheronome(all_paths, self.n_best)
                if len(fail_path) != 0:
                        self._spread_pheronome(fail_path, self.n_best)

                self._spread_pheronome_gb(all_time_shortest_path)
                self._spread_pheronome_gb(all_time_best_fail_path)

                i+=1

        return all_time_shortest_path

    def _spread_pheronome(self, all_paths, n_best):
        sorted_paths = sorted(all_paths, key=lambda x: x[1])
        for path, time in sorted_paths[:n_best]:
            for move in path:
                self.pheromone[move] += 999.0 / time


    def _spread_pheronome_gb(self,all_time_shortest_path):
        path, time = all_time_shortest_path
        for move in path:
                self.pheromone[move] += 999.0 / time


    def gen_time_taken(self, i):     
        #i=(prev, move)
        #caculate time finished service at node that we move to
        self.time +=self.time_travel[i]
        if self.time < self.time_window[i[1]][0]:
            self.time=self.time_window[i[1]][0]
            self.time+=self.time_window[i[1]][2]
        else:
            self.time+=self.time_window[i[1]][2]
        return self.time

    def gen_all_paths(self):
        all_paths = []
        fail_paths = []
        for _ in range(self.n_ants):
            self.time=0
            # print(self.pheromone)
            # sleep(0.4)
            path = self.gen_path(0)
            if len(path) == len(self.time_travel):
                all_paths.append((path, self.time))
            else:
                fail_paths.append((path, self.penalty + 10*(self.time/len(path))))

        return all_paths, fail_paths

    def gen_path(self, start):
        path = []
        start=start%(len(self.time_travel))
        visited = set()
        visited.add(start)
        prev = start
        for _ in range(len(self.time_travel) - 1):
            move = self.pick_move(self.pheromone[prev], self.time_travel[prev], visited, prev)

            if move == None:
                # for edge in path:
                #     self.pheromone[edge] = self.pheromone[edge] * self.persistence

                # path = (path, self.penalty - self.time)
                # self._spread_pheronome_gb(path)

                return path
            else:
                path.append((prev, move))
                self.gen_time_taken((prev, move))
                # print(self.time)
                prev = move
                visited.add(move)
            
        path.append((prev, start)) # going back to where we started    
        self.time += self.time_travel[(prev, start)]
        return path

    def pick_move(self, pheromone, time, visited, prev):
        q=rand()
        pheromone = np.copy(pheromone)
        pheromone[list(visited)] = 0

        g = self.upper_bound_heuristic(time)
        h = self.lower_bound_heuristic(time)
        t = self.time_trav(time, prev)

        row = (pheromone ** self.alpha) * (g ** self.beta) * (h ** self.gamma) * (t ** self.epsilon)
        # print(row)
        sum = row.sum()
        # print(sum)

        if sum == 0:
            return None
        else:
            norm_row = row / sum   
            # print(norm_row)
            # sleep(3)

            move = np_choice(self.all_inds, 1, p=norm_row.astype('float64'))[0]


            return move

    def upper_bound_heuristic(self, time):
        # time is time travel from current node to other node
        ''' G = the upper bound - the time arrived at node
        -->ant should chose the node which the arrived time is cloder to the upper bound
        g is the sigmoid of G (smaller G -> greater g)
        g = 1/(1 + exp(delta(G - mu)))
        delta: slope
        mu: inflection point

        '''
        G = time + self.time
        mu = sum(G)/len(G)
        delta = 0.003
        upper_bound = self.time_window[:,1]
        G = upper_bound - G
        G = np.array(G, dtype= np.longdouble)
        # print(G)
        # print(mu)
        for i in range(len(G)):
            if G[i] >= 0:
                G[i] = 1/(1 + np.exp(delta * (G[i] - mu)))  
                # print(G[i])
                # sleep(2)
            else:
                G[i] = 0
        return G

    def lower_bound_heuristic(self, time):
        # time is time travel from current node to other node
        ''' H = the lower bound - the time arrived at node
        --> ant should chose the node with the lowest waiting time
        h is the sigmoid of G (smaller H -> greater h)
        h = 1/(1 + exp(delta(H - mu)))
        delta: slope
        mu: inflection point

        '''
        H = time + self.time
        mu = sum(H)/len(H)
        delta = 0.003
        lower_bound = self.time_window[:,0]
        H = lower_bound - H
        H = np.array(H, dtype= np.longdouble)
        for i in range(len(H)):
            if H[i] > 0:
                H[i] = 1/(1 + np.exp(delta * (H[i] - mu)))
            else:
                H[i] = 1
        return H

    def time_trav(self, time, prev):
        T = time + self.time
        T = [list(T)]
        T.append(list(self.time_window[:,0]))
        # print(T)

        t = []
        for i in range(len(T[0])):
            t.append(max(T[0][i], T[1][i]))
        t[prev] = np.inf
        t = np.array(t)
        t = t - self.time
        for i in range(len(t)):
            if t[i] == 0:
                t[i] = 1
            if t[i] == 1:
                t[i] = 1.000000001

        # print(prev)
        # print(1/t)
        # sleep(1)
        return 1/t


if __name__ == '__main__':
    with open("data/data100.txt", "r") as f:  
        data= f.read()

    sys.stdin=StringIO(data)
    T=[]
    c=[[0,0,0]]
    n=[int(x) for x in sys.stdin.readline().split()]    #number of city excluding 0
    n=n[0]
    for i in range(n):
        time_required=[int(x) for x in sys.stdin.readline().split()]           # start=[0]   end=[1]   service=[2]
        c.append(time_required) #time window matrix
    for i in range(n+1):
        d=[int(x) for x in sys.stdin.readline().split()]    
        # d[i]=np.inf
        T.append(d) 

    time_travel=np.array(T)   
    time_window=np.array(c)

    begin=process_time()
    ant_colony = AntColony(time_travel,time_window, 50, 1, 100, 0.8, alpha=1, beta=3, gamma=3, epsilon=4, qo=0.1)
    shortest_path = ant_colony.run()
    print ("shortest_path: {}".format(shortest_path))
    finish=process_time()

    print('time taken', finish-begin)