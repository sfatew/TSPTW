from ortools.sat.python import cp_model

def get_input(filename):
    time_window=[[0,10**10,0]]
    travel_time=[]
    with open(file=filename) as f:
        n=int(f.readline())
        for _ in range(n):
            time_window.append(list(map(int,f.readline().split())))
        for _ in range(n+1):
            travel_time.append(list(map(int,f.readline().split())))
    return n,time_window,travel_time

def TSP_TW_CP(filename):
    n,time_window,travel_time=get_input(filename)
    model=cp_model.CpModel()
    all_customers=n+1
    M=10**10 
    # Define variables  

    e = [] # earliest time to serve customer i
    l = [] # latest time to serve customer i
    d = [] # duration time to serve customer i
    x = {} # = 1 if exists path i to j, 0 otherwise
    t = {} # arrival time at customer i
    tt= {} # = d[i] + travel_time[i][j]
    u = {} # takes the value of order of node i in final route
    w = {} # waiting time to serve customer i
    for i in range(all_customers):
        e.append(time_window[i][0])
        l.append(time_window[i][1])
        d.append(time_window[i][2])
    for i in range(all_customers):
        for j in range(all_customers):
            x[i,j]=model.NewBoolVar(f"x[{i}{j}]")
            tt[i,j]=d[i]+travel_time[i][j]
    t[0]=model.NewIntVar(0,0,f"t[0]")
    for i in range(1,all_customers):
        t[i]=model.NewIntVar(e[i],l[i],f"t[{i}]")
    for i in range(all_customers):
        w[i]=model.NewIntVar(0,l[i]-e[i],f"w[{i}]")
    for i in range(all_customers):
        if i==0:
            u[i]=model.NewIntVar(0,0,f"u{i}")
            continue
        u[i]=model.NewIntVar(0,all_customers-1,f"u{i}")
        
    # Define constraints 
        
    for i in range(all_customers):
        model.Add(sum(x[i,j] for j in range(all_customers) if j!=i)==1) # 1 node has only 1 edge out
        model.Add(sum(x[j,i] for j in range(all_customers) if j!=i)==1) # 1 node has only 1 edge in
    
    for i in range(1,all_customers):
        for j in range(1,all_customers):
            if i!=j:
                model.Add(u[i]-u[j]+n*x[i,j]<=n-1) # avoiding subtour
    
    for i in range(all_customers):
        for j in range(1,all_customers):
            if i!=j:
                # We will add travel time ttij to arrival time at node i to get arrival time at node j if exists path i to j
                model.Add(t[i] + tt[i, j]*x[i, j] - t[j] <= (1 - x[i, j]) * M)
    
    for i in range(all_customers):
        for j in range(1,all_customers):
            if i!=j:
                model.Add(w[j]==t[j]-t[i]-tt[i,j]).OnlyEnforceIf(x[i,j]) 
    
    # Objective function
    model.Minimize(sum(tt[i,j]*x[i,j] for j in range(all_customers) for i in range(all_customers) if i!=j) + sum(w[i] for i in range(all_customers)))
    
    # Solve
    solver=cp_model.CpSolver()
    status=solver.Solve(model)

    if status==cp_model.OPTIMAL or status==cp_model.FEASIBLE:
        print(n)
        current_node=0
        finished=False
        while(not finished):
            for i in range(all_customers):
                if i!=current_node and solver.BooleanValue(x[current_node,i]):
                    current_node=i
                    if current_node==0:
                        finished=True
                        break
                    print(current_node,end=" ")
                    break
    else:
        print("No solution!")

TSP_TW_CP("10nodes.txt")




        
