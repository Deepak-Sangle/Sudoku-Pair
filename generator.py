from glob import glob
# import init
import random 
import csv
import time
from pysat.card import *
from pysat.solvers import Solver

def create_no1(a, b, c):
    return (k ** 4) * (a - 1) + (k ** 2) * (b - 1) + c

def extract_k(i, j, a):
    if a % n == 0:
        return n
    else:
        return a % n

# Each cell contains atleast one value
def cell_atleast_one_value():
    for i in range(0, 2 * n):
        for j in range(0, n):
            row_list = []
            for k in range(0, n):
                row_list.append(create_no1(i + 1, j + 1, k + 1))
            solver.add_clause(row_list)
            temp_cnf.append(row_list)

# Each cell contains atmost one value
def cell_atmost_one_value():
    for i in range(0, 2 * n):
        for j in range(0, n):
            for k in range(1, n):
                a = create_no1(i + 1, j + 1, k)
                for l in range(k+1, n + 1):
                    b = create_no1(i + 1, j + 1, l)
                    solver.add_clause([-a, -b])
                    temp_cnf.append([-a,-b])

# ​Each row has all the numbers
def each_row_all_nos():
    for i in range(0, 2 * n):
        for k in range(0, n):
            row_list = []
            for j in range(0, n):
                row_list.append(create_no1(i + 1, j + 1, k + 1))
            solver.add_clause(row_list)
            temp_cnf.append(row_list)

# ​Each col has all the numbers
def each_col_all_nos():
    for j in range(0, n):
        for k in range(0, n):
            row_list = []
            for i in range(0, n):
                row_list.append(create_no1(i + 1, j + 1, k + 1))
            solver.add_clause(row_list)
            temp_cnf.append(row_list)
            row_list = []
            for i in range(n, 2 * n):
                row_list.append(create_no1(i + 1, j + 1, k + 1))
            solver.add_clause(row_list)
            temp_cnf.append(row_list)

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
                temp_cnf.append(temp_list)

def sudoku_pair_cndn():
    for i in range(0, n):
        for j in range(0, n):
            for k in range(0, n):
                a = (-create_no1(i + 1, j + 1, k + 1))
                b = (-create_no1(i + 1 + n, j + 1, k + 1))
                solver.add_clause([a, b])
                temp_cnf.append([a, b])

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
                    temp_cnf.append([-a,-b])

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
                    temp_cnf.append([-a,-b])

    for j in range(0,n) :
        for k in range(1,n+1):
            for l in range(n,2*n):
                for r in range(n,2*n):
                    if(r<=l) :
                        continue
                    a = create_no1(l+1,j+1,k)
                    b = create_no1(r+1,j+1,k)
                    solver.add_clause([-a,-b])
                    temp_cnf.append([-a,-b])

def create_template_sudoku():
    for x in range(0,n,k) :
        sudoku1[x][x] = random.randrange(1,9)   
        assumption_list.append(create_no1(x+1,x+1,sudoku1[x][x]))
    
def create_empty_sudoku():
    global sudoku1
    sudoku1 = []
    global sudoku2 
    sudoku2 = []
    for i in range(0,n) :
        temp_list = []
        for j in range(0,n) :
            temp_list.append(0)
        sudoku1.append(temp_list)
        sudoku2.append(temp_list)

def store_solved_sudoku():
    global ans_sudoku
    ans_sudoku = []
    global fin_sudoku1
    global fin_sudoku2
    fin_sudoku1 = []
    fin_sudoku2 = []
    count = 0
    i = 0
    while count < 2 * n * n:
        x = solver.get_model()[i]
        if x > 0:
            ans_sudoku.append(x)
            count = count + 1
        i = i + 1

    count = 0
    for i in range(1, n + 1):
        temp_ans = []
        for j in range(1, n + 1):
            z = ans_sudoku[count]
            count = count + 1
            temp_ans.append(extract_k(i, j, z))
        fin_sudoku1.append(temp_ans)
    
    for i in range(n, 2*n):
        temp_ans = []
        for j in range(1, n + 1):
            z = ans_sudoku[count]
            count = count + 1
            temp_ans.append(extract_k(i, j, z))
        fin_sudoku2.append(temp_ans)
    
def call_conditions():
    # Calling all the functions
    cell_atmost_one_value()
    cell_atleast_one_value()
    each_row_all_nos()
    each_col_all_nos()
    each_block_all_nos()
    sudoku_pair_cndn()
    # Adding extra condition/restriction so that our Sudoku solves faster
    row_has_atmost_one_val()
    col_has_atmost_one_val()
      

def solve_template_sudoku():
    call_conditions()
    solver.solve(assumption_list)
    store_solved_sudoku()

def get_assumption_list() :
    for r in range(0,n) :
        for c in range(0,n) :
            s = fin_sudoku1[r][c]
            assumption_list1.append(create_no1(r+1,c+1,s))

    for r in range(n,2*n) :
        for c in range(0,n) :
            s = fin_sudoku2[r-n][c]
            assumption_list1.append(create_no1(r+1,c+1,s))

def write_csv_file() :
    output_file = "output.csv"
    with open(output_file, 'w', newline='') as csvfile: 
        csvwriter = csv.writer(csvfile)  
        # writing the data rows 
        csvwriter.writerows(fin_ans_sudoku1)
        csvwriter.writerows(" ")
        csvwriter.writerows(fin_ans_sudoku2)    

    print("\nThe unsolved Sudoku pair output is now present in the file named 'output.csv' file.\n")
    print("Time required for Solving the sudoku pair is", exc_time, "seconds")

def generate_sudoku() :
    count = 0
    shuf_assumption = assumption_list1.copy()
    random.shuffle(shuf_assumption)
    len_assump = len(shuf_assumption)
    i = 0
    for count in range(0,2*n*n) :
        a = shuf_assumption[0]
        shuf_assumption.remove(a)
        temp_solver = Solver()
        temp_solver.append_formula(temp_cnf)
        temp_count = 0
        for m in temp_solver.enum_models(shuf_assumption) :
            temp_count = temp_count + 1
            if temp_count > 1 :
                shuf_assumption.append(a)
                break
        if(count == 2*n*n - 1) :
            # Final Sudoku is generated now
            fin_ans_sudoku = []
            global fin_ans_sudoku1
            global fin_ans_sudoku2
            fin_ans_sudoku1 = []
            fin_ans_sudoku2 = []
            cc = 0
            i = 0
            shuf_assumption.sort()
            fin_len = len(shuf_assumption)
            cc = 0
            ll = 0
            flg = 0
            end_time = time.time()
            time2 = end_time - begin_time
            global exc_time
            exc_time="{:.2f}".format(time2)
            yn = input("\nDo you want to print the unsolved Sudoku pair(Y/N): ")
            while flg!=1 and flg!=-1 :
                if(yn=='Y' or yn=='y') :
                    print("The two Sudoku Pair is given below!\n")
                    flg=1
                else :
                    if (yn=='N' or yn=='n') :
                        flg=-1
                    else :
                        yn = input("Invalid Input. Please type either y/n! ")
            if(flg==1):
                print("First Sudoku is given below: ")
            for i in range(0,n):
                temp_ans = []
                for j in range(0,n):
                    if(assumption_list1[cc] == shuf_assumption[ll]) :
                        ll = ll+1
                        temp_ans.append(extract_k(i, j, assumption_list1[cc]))
                    else :
                        temp_ans.append(0)
                    cc = cc + 1
                fin_ans_sudoku1.append(temp_ans)
                frmt = "{:>3}"*len(temp_ans)
                if flg == 1 :
                    print(frmt.format(*temp_ans))
            if(flg==1):
                print("\nSecond Sudoku is given below: ")
            for i in range(0,n):
                temp_ans = []
                for j in range(0,n):
                    if(ll<fin_len and assumption_list1[cc] == shuf_assumption[ll]) :
                        ll = ll+1
                        temp_ans.append(extract_k(i, j, assumption_list1[cc]))
                    else :
                        temp_ans.append(0)
                    cc = cc + 1
                fin_ans_sudoku2.append(temp_ans)
                frmt = "{:>3}"*len(temp_ans)
                if flg == 1 :
                    print(frmt.format(*temp_ans))
            write_csv_file()

def main():
    create_empty_sudoku()
    create_template_sudoku()
    solve_template_sudoku()
    get_assumption_list()
    generate_sudoku()
    
if __name__ == "__main__":
    # Define Global Variables
    begin_time = time.time()
    solver = Solver()
    temp_cnf = []
    assumption_list = []
    assumption_list1 = []
    # assumption_list2 = []
    global n
    global k
    inpflg=0
    k=(input("Enter the value of k: "))
    while inpflg!=1 :
        if k.isnumeric() :
            k = int(k)
            if k == 0 or k==1 :
                k = input("Sudoku does not exists for such k value! Input other value. ")
            elif k > 5 :
                k = input("Value of k is too large! Input smaller value! ")    
            elif k>1 and k<=5 :
                if(k==5):
                    print("Please wait a moment while the code generates the sudoku pair")
                inpflg=1
        else :
            k = input("Value of k should be integer! Please type valid input! ")
    
    n=k**2
    main()
