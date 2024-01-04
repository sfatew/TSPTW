from ortools.sat.python import cp_model

def TSP_CP(n, time_matrix, dist_matrix):
    model = cp_model.CpModel()

    num_nodes = n + 1 #N+1
    e = {}  # earliest time to visit city i
    l = {}  # latest time to visit city i
    d = {}  # duration time (delivery time) to visit city i
    x = {}  # x[i,j] = 1 if i -> j else 0
    C = {}  # C[i,j] = d[i] + dist_matrix[i][j]
    M = {}  # M[i] = time to visit city i
    d[0] = 0
    e[0] = 0
    l[0] = 1000000000

    for i in range(1, num_nodes):
        e[i] = time_matrix[i-1][0]
        l[i] = time_matrix[i-1][1]
        d[i] = time_matrix[i-1][2]
    for i in range(num_nodes):
        for j in range(num_nodes):
            x[i, j] = model.NewIntVar(0, 1, 'x[%i,%i]' % (i, j)) #binary matrix
            C[i, j] = d[i] + dist_matrix[i][j] #distance matrix + d[i] 
    #cumulative cost at node 0 = 0
    M[0] = model.NewIntVar(0, 0, 'M[%i]' % 0)
    for i in range(1, num_nodes):
        M[i] = model.NewIntVar(e[i], l[i], 'M[%i]' % i)
    w = {}
    for i in range(num_nodes):
        w[i] = model.NewIntVar(0, l[i] - e[i], 'w[%i]' % i)

    for i in range(num_nodes):
    #constraint 1, 2 and 3: All nodes have to be visited by truck exactly once, Truck leaves depot D and comes back to depot D' exactly once. 
        model.Add(sum(x[i, j] for j in range(num_nodes) if j != i) == 1) #constraint 1
        model.Add(sum(x[j, i] for j in range(num_nodes) if j != i) == 1) #constraint 2
        model.Add(sum(x[j, i] for j in range(num_nodes) if j != i) == sum(x[j, k] for k in range(num_nodes) if j != k)) #constraint 3
    for i in range(num_nodes):
        for j in range(1, num_nodes):
            if i != j:
    #Add travel time tt_ij to arrival node at node i to get arrival time at node j if truck travels in ij path (linearize) - constraint 5 
                model.Add(M[i] + C[i, j]*x[i, j] - M[j] <= (1 - x[i, j]) * 1000000000)

    for i in range(num_nodes):
        for j in range(1, num_nodes):
            if i != j:
    #Only add w if that node is being visited - constraint 6
                model.Add(w[j] == M[j] - M[i] - C[i, j]).OnlyEnforceIf(x[i, j])
    #objective function = cumulative cost at each node * binary matrix x
    model.Minimize(sum(C[i, j] * x[i, j] for i in range(num_nodes) for j in range(num_nodes) if j != i) + sum(w[i] for i in range(num_nodes)))
    
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        print(n)
        solution = {}
        solution[0] = 0 #node 0

        for i in range(1, num_nodes):
            solution[i] = solver.Value(M[i])
        solution = sorted(solution.items(), key=lambda x: x[1]) #sort by the values

        for i in range(1, num_nodes):
            print(solution[i][0], end=' ') #print the keys in the required format. For e.g. "1 5 3 2 4 "
        return solver.ObjectiveValue() #final cost
#run main() function
def main():
    N = int(input())
    customers = []
    t = []
    for i in range(1, N+1):
        e, l, d = map(int, input().split())
        customers.append([e, l, d])

    for _ in range(N+1):
        row = list(map(int, input().split()))
        t.append(row)
    TSP_CP(N, customers, t)

if __name__ == '__main__':
    main()