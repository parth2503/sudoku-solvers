import pulp

input_sudoku = [
                    [3,0,0,8,0,0,0,0,1],
                    [0,0,0,0,0,2,0,0,0],
                    [0,4,1,5,0,0,8,3,0],
                    [0,2,0,0,0,1,0,0,0],
                    [8,5,0,4,0,3,0,1,7],
                    [0,0,0,7,0,0,0,2,0],
                    [0,8,5,0,0,9,7,4,0],
                    [0,0,0,1,0,0,0,0,0],
                    [9,0,0,0,0,7,0,0,6]
                ]


prob=pulp.LpProblem("Sudoku_Solver")
objective=pulp.lpSum(0)
prob.setObjective(objective)

rows=range(0,9)
cols=range(0,9)
grids=range(0,9)
values=range(1,10)

variables=pulp.LpVariable.dicts("value",(rows,cols,values),cat='Binary')

#constraints

for row in rows:
    for col in cols:
        prob.addConstraint(pulp.LpConstraint(e=pulp.lpSum([variables[row][col][value] for value in values]), sense=pulp.LpConstraintEQ,rhs=1))

for row in rows:
    for value in values:
        prob.addConstraint(pulp.LpConstraint(e=pulp.lpSum([variables[row][col][value]*value for col in cols]), sense=pulp.LpConstraintEQ,rhs=value))

for value in values:
    for col in cols:
        prob.addConstraint(pulp.LpConstraint(e=pulp.lpSum([variables[row][col][value]*value for row in rows]), sense=pulp.LpConstraintEQ,rhs=value))

for grid in grids:
    grid_row=grid//3
    grid_col=grid%3

    for value in values:
        prob.addConstraint(pulp.LpConstraint(e=pulp.lpSum([variables[grid_row*3+row][grid_col*3+col][value]*value for col in range(0,3) for row in range(0,3)]),sense=pulp.LpConstraintEQ, rhs=value))

for row in rows:
    for col in cols:
        if(input_sudoku[row][col]!=0):
            prob.addConstraint(pulp.LpConstraint(e=pulp.lpSum([variables[row][col][value]*value for value in values]),sense=pulp.LpConstraintEQ,rhs=input_sudoku[row][col]))

            
prob.solve()

solution=[[0 for col in cols] for row in rows]
for row in rows:
    for col in cols:
        for value in values:
            if pulp.value(variables[row][col][value]):
                solution[row][col]=value


print("\n\n+ ----------- + ----------- + ----------- +",end="")
for row in rows:
    print("\n",end="\n|  ")
    for col in cols:
        num_end = "  |  " if ((col+1)%3==0) else "   "
        print(solution[row][col],end=num_end)
    
    if ((row+1)%3==0):
        print("\n\n+ ----------- + ----------- + ----------- +",end="")