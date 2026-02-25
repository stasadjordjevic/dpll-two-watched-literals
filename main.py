import sys
from cnf_formula import read_dimacs
from dpll_solver import DPLLSolver

if len(sys.argv) != 2:
    print("Upotreba: python3 main.py <putanja_do_fajla.cnf>")
    sys.exit(1)

formula = read_dimacs(sys.argv[1])
solver = DPLLSolver(formula)
result = solver.solve()
solver.print_result(result)