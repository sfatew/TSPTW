import sys
import numpy as np
from io import StringIO
import json

with open("data.json", "r") as read_file:
    doc = json.load(read_file)

sys.stdin=StringIO(doc)
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

t_min= np.inf    # best solution so far
T_min= np.inf    # shortest segment of the time matrix t
t1_i=0
stored_ti=[]
sol=[]

for i in range(n+1):
      for j in range(n+1):
        if i != j and T_min>T[i][j]:
            T_min=T[i][j]

def solution():
  global t_min
  global sol

  a=t1_i + c[s[n]][2]+ T[s[n]][0]
  # print(a<t_min)
  if a < t_min:
     t_min=a 
     u=s[:]
     sol=[t_min,u]
    #  print(sol)

def check(v,k):
  return t1_i+ c[s[k-1]][2]+ T[s[k-1]][v] <= c[s[k]][1]

def Try(k):
  global t1_i         # declare t1_i to be a global
  global t_min
  global stored_ti

  for v in range (1,n+1): 
    if visited[v]==False: 
      s[k]=v
      if check(v,k):
        t_i= t1_i+ c[s[k-1]][2]+ T[s[k-1]][s[k]] 
        t1_i= max(c[v][0], t_i)         #time at which the agent can start to serve the node
        if t1_i==c[v][0]:
          stored_ti.append(t_i)         # Use 'STACK' to store the value of t_i (for backtracking) 
          # print(stored_ti)

        visited[v]=True
        if k==n:
           solution()
        else:
           g=t_i + T_min*(n-k+1)        #branch & bound
           if g< t_min:
              Try(k+1)

        visited[v]=False
        t1_i = t_i- c[s[k-1]][2]- T[s[k-1]][s[k]]    # caculate t1_(k-1)
        if t1_i == c[s[k-1]][0]:                     # caculate t_(k-1)   ( by t1_(k-1) = max(e(k-1),t(k-1)) )
           t_i= stored_ti.pop() 
           if v!= n :
              stored_ti.append(t_i) 
          #  print(t_i)
          #  print(k)  
          #  print(v)                  
        else:
           ti=t1_i


Try(1)

print(n)
print(sol)
print(' '.join(str(i) for i in sol[1][1:]))