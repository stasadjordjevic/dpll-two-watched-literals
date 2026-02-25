# DPLL Two-Watched Literals SAT Solver

**Implementation of a DPLL SAT solver with the Two-Watched Literals scheme**  
This repository contains an implementation of a SAT solver based on the **DPLL (Davis-Putnam-Logemann-Loveland)** algorithm, enhanced with the **Two-Watched Literals** scheme for efficient unit propagation. The project demonstrates both the algorithmic procedure and practical programming techniques for handling propositional formulas in **CNF (Conjunctive Normal Form)**.

This work is a **seminar project** prepared for the course *Automated Reasoning* at the **Faculty of Mathematics, University of Belgrade**.  

The repository also includes **documentation in Serbian** describing the implementation and methodology.

## Repository structure

- `cnf_formula.py` — `CNFFormula` class with data structures for the two-watched literals scheme and DIMACS file parsing
- `dpll_solver.py` — `DPLLSolver` class with the DPLL procedure implementation
- `main.py` — program entry point

## Usage
```bash
python3 main.py proba.cnf
```

## Input format

Input files must be in standard **DIMACS CNF format**:
```
c this is a comment
p cnf <num_variables> <num_clauses>
1 -2 0
3 0
...
```
Each clause is a list of integers terminated by `0`. Lines starting with `c` are treated as comments.