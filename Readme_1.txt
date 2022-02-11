Sudoku Pair Solver

A general k*k × k*k Sudoku pair solver that works by encoding a simple program to translate partially solved Sudoku puzzle pair into CNF formulas such that the CNF is satisfiable iff the puzzle has a solution. The project is written in pySAT.

Features:-
1.Work for all values of k
2.Code is easy to read and understand
3.Reads a csv file as input 

Following shows the example of how to use this program:
1.Give input in form of k and a csv file containing two partially filled sudoku of k*k x k*k size.
2.In the function <read_csv()> change the file name you want to run as a test case. (Don't forget to change the directory when accesing different input files).
3.Run the program by writing py solver.py

It may take some time to give output so one need to wait for a while for large value of k.
