from cnf_formula import read_dimacs
from dpll_solver import DPLLSolver

formula = read_dimacs("proba.cnf")
result = DPLLSolver(formula).solve()