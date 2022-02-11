# import random
import csv
import time
from pysat.card import *
from pysat.solvers import Solver
# from pysat.formula import CNF

# Reading inputs from the given CSV File
def read_csv_file():
    # Opening the CSV File
    input_file = open("test cases\input_4.csv")
    csvreader = csv.reader(input_file)
    # Reading the dimension of Sudoku
    header = (next(csvreader))
    global k
    global n
    k = int(header[0])
    n = k ** 2

    # Reading each row of CSV File
    for row in csvreader:
        temp_input.append(row)

    # Typecasting the input to integer datatype
    for i in range(0, 2 * n):
        for j in range(0, n):
            temp_input[i][j] = int(temp_input[i][j])

    # Closing the CSV File
    input_file.close()


# Function to create Variables
def create_no1(a, b, c):
    return (k ** 4) * (a - 1) + (k ** 2) * (b - 1) + c


# Filled entries should correspond to true!
def assign_assumption():
    for i in range(0, 2 * n):
        for j in range(0, n):
            if (temp_input[i][j] != 0):
                assumption1.append(create_no1(i + 1, j + 1, temp_input[i][j]))

# Conditions for Generating Sudoku Pairs
# ​Each row has all the numbers
# ​Each col has all the numbers
# Each cell contains atmost one value
# Each cell contains atleast one value
# Each block contains all k*k values
# x(i,j) of Sudoko 1 and x(i,j) of Sudoko2 is not equal

# Each cell contains atleast one value
def cell_atleast_one_value():
    for i in range(0, 2 * n):
        for j in range(0, n):
            row_list = []
            for k in range(0, n):
                row_list.append(create_no1(i + 1, j + 1, k + 1))
            solver.add_clause(row_list)
            # solver.append(row_list)


# Each cell contains atmost one value
def cell_atmost_one_value():
    for i in range(0, 2 * n):
        for j in range(0, n):
            for k in range(1, n):
                a = create_no1(i + 1, j + 1, k)
                for l in range(k+1, n + 1):
                    b = create_no1(i + 1, j + 1, l)
                    solver.add_clause([-a, -b])
                    # solver.append([-a,-b])

# ​Each row has all the numbers
def each_row_all_nos():
    for i in range(0, 2 * n):
        for k in range(0, n):
            row_list = []
            for j in range(0, n):
                row_list.append(create_no1(i + 1, j + 1, k + 1))
            solver.add_clause(row_list)
            # solver.append(row_list)


# ​Each col has all the numbers
def each_col_all_nos():
    for j in range(0, n):
        for k in range(0, n):
            row_list = []
            for i in range(0, n):
                row_list.append(create_no1(i + 1, j + 1, k + 1))
            solver.add_clause(row_list)
            row_list = []
            for i in range(n, 2 * n):
                row_list.append(create_no1(i + 1, j + 1, k + 1))
            solver.add_clause(row_list)


# Each block contains all k*k values
def each_block_all_nos():
    for r in range(0, 2 * n, k):
        for c in range(0, n, k):
            for v in range(1, n + 1):
                temp_list = []
                for i in range(r, r + k):
                    for j in range(c, c + k):
                        temp_list.append(create_no1(i + 1, j + 1, v))
                solver.add_clause(temp_list)

# x(i,j) of Sudoko 1 and x(i,j) of Sudoko2 is not equal
def sudoku_pair_cndn():
    for i in range(0, n):
        for j in range(0, n):
            for k in range(0, n):
                a = (-create_no1(i + 1, j + 1, k + 1))
                b = (-create_no1(i + 1 + n, j + 1, k + 1))
                solver.add_clause([a, b])
                # solver.append([-a,-b])


# Each row has atmost n values
def row_has_atmost_one_val():
    for i in range(0,2*n) :
        for k in range(1,n+1):
            for l in range(0,n):
                for r in range(0,n):
                    if(r<=l) :
                        continue
                    a = create_no1(i+1,l+1,k)
                    b = create_no1(i+1,r+1,k)
                    solver.add_clause([-a,-b])

# Each col has atmost n values
def col_has_atmost_one_val():
    for j in range(0,n) :
        for k in range(1,n+1):
            for l in range(0,n):
                for r in range(0,n):
                    if(r<=l) :
                        continue
                    a = create_no1(l+1,j+1,k)
                    b = create_no1(r+1,j+1,k)
                    solver.add_clause([-a,-b])

    for j in range(0,n) :
        for k in range(1,n+1):
            for l in range(n,2*n):
                for r in range(n,2*n):
                    if(r<=l) :
                        continue
                    a = create_no1(l+1,j+1,k)
                    b = create_no1(r+1,j+1,k)
                    solver.add_clause([-a,-b])

def extract_k(i, j, a):
    if a % n == 0:
        return n
    else:
        return a % n

def print_ans():
    global ans_sudoku
    ans_sudoku = []
    count = 0
    i = 0
    flag = 0
    while count < 2 * n * n:
        x = solver.get_model()[i]
        if x > 0:
            ans_sudoku.append(x)
            count = count + 1
        i = i + 1

    count = 0
    print("Solution for the given inputs exists!")
    print("\nFirst Sudoku is given below:\n")
    for i in range(1, n + 1):
        temp_ans = []
        for j in range(1, n + 1):
            z = ans_sudoku[count]
            count = count + 1
            temp_ans.append(extract_k(i, j, z))
        frmt = "{:>3}"*len(temp_ans)
        print(frmt.format(*temp_ans))
    print("\nSecond Sudoku is given below:\n")
    for i in range(n, 2*n):
        temp_ans = []
        for j in range(1, n + 1):
            z = ans_sudoku[count]
            count = count + 1
            temp_ans.append(extract_k(i, j, z))
        frmt = "{:>3}"*len(temp_ans)
        print(frmt.format(*temp_ans))
    

def main():
    # Calling all the functions
    read_csv_file()
    assign_assumption()
    cell_atmost_one_value()
    cell_atleast_one_value()
    each_row_all_nos()
    each_col_all_nos()
    each_block_all_nos()
    sudoku_pair_cndn()
    # Adding extra condition/restriction so that our Sudoku solves faster
    row_has_atmost_one_val()
    col_has_atmost_one_val()
    solver.solve(assumption1)

    if solver.get_model():
        print_ans()
        end_time = time.time()
        time2 = end_time - begin_time
        exc_time="{:.2f}".format(time2)
        print("\nNumber of variables used are",solver.nof_vars())
        print("Number of clauses used are",solver.nof_clauses())
        print("Time required for Solving the sudoku pair is", exc_time, "seconds")

    else:
        print("No such Sudoku Pair Exists")

if __name__ == "__main__":
    # Define Global Variables
    begin_time = time.time()
    temp_input = []
    assumption1 = []
    solver = Solver()
    # solver = CNF()
    main()
