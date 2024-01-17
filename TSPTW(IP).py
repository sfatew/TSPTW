from ortools.linear_solver import pywraplp

def TSPinteger_programming(n, time_matrix, dist_matrix):
    model = pywraplp.Solver.CreateSolver('SCIP')
    num_nodes = n + 1
    e = {}  # earliest time to visit city i
    l = {}  # latest time to visit city i
    d = {}  # duration time to visit city i
    x = {}  # x[i,j] = 1 if i -> j else 0
    C = {}  # C[i,j] = d[i] + dist_matrix[i][j]
    M = {}  # M[i] = time to visit city i
    d[0] = 0
    e[0] = 0
    l[0] = 100000000
    for i in range(1, num_nodes):
        e[i] = time_matrix[i-1][0]
        l[i] = time_matrix[i-1][1]
        d[i] = time_matrix[i-1][2]

    for i in range(num_nodes):
        for j in range(num_nodes):
            x[i, j] = model.IntVar(0, 1, 'x[%i,%i]' % (i, j))
            C[i, j] = d[i] + dist_matrix[i][j]
    #cumulative cost at node 0 = 0
    M[0] = model.IntVar(0, 0, 'M[%i]' % 0)
    for i in range(1, num_nodes):
        M[i] = model.IntVar(e[i], l[i], 'M[%i]' % i)
    
    w = {}
    for i in range(num_nodes):
        w[i] = model.IntVar(0, model.infinity(), 'w[%i]' % i)

    u = {}
    for i in range(num_nodes):
        u[i] = model.IntVar(0, n, 'u[%i]' % i)
    # each city is visited exactly once
    for i in range(num_nodes):
        constraint = model.Constraint(1, 1)
        for j in range(num_nodes):
            if i != j:
                constraint.SetCoefficient(x[i, j], 1)
    # each city is left exactly once
    for i in range(num_nodes):
        constraint = model.Constraint(1, 1)
        for j in range(num_nodes):
            if i != j:
                constraint.SetCoefficient(x[j, i], 1)
    #subtour elimination
    for i in range(1,num_nodes):
        for j in range(num_nodes):
            if i != j:
                constraint = model.Constraint(-model.infinity(), 100000001)
                constraint.SetCoefficient(u[i], 1)
                constraint.SetCoefficient(u[j], -1)
                constraint.SetCoefficient(x[i,j], 100000000)
    #Add travel time tt_ij to arrival node at node i to get arrival time at node j if truck travels in ij path (linearize)
    for i in range(num_nodes):
        for j in range(1, num_nodes):
            if i != j:
                constraint = model.Constraint(-model.infinity(), 100000000)
                constraint.SetCoefficient(M[i], 1)
                constraint.SetCoefficient(x[i, j], C[i, j] + 100000000)
                constraint.SetCoefficient(M[j], -1)
    #time windows cons
    for i in range(num_nodes):
        for j in range(1, num_nodes):
            if i != j:
                constraint = model.Constraint(- 100000000 - C[i,j], model.infinity())
                constraint.SetCoefficient(w[j], 1)
                constraint.SetCoefficient(M[j], -1)
                constraint.SetCoefficient(M[i], 1)
                constraint.SetCoefficient(x[i, j], -100000000)  

    objective = model.Objective()
    for i in range(num_nodes):
        for j in range(num_nodes):
            if i != j:
                objective.SetCoefficient(x[i, j], C[i, j])
    for i in range(num_nodes):
        objective.SetCoefficient(w[i], 1)
    objective.SetMinimization()
    status = model.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print(n)
        solution = {}
        solution[0] = 0
        for i in range(1, num_nodes):
            solution[i] = M[i].solution_value()
        solution = sorted(solution.items(), key=lambda x: x[1])
        for i in range(1,num_nodes):
            print(solution[i][0], end=' ')
    else:
        print('The problem does not have an optimal solution.')

    return model.Objective().Value()
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
    TSPinteger_programming(N, customers, t)
if __name__ == '__main__':
    main()