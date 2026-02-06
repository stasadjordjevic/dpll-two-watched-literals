from typing import List
from cnf_formula import CNFFormula

class DPLLSolver:
    def __init__(self, formula:CNFFormula):
        self.formula = formula
        self.partial_valuation = set()
# vraca -1 ako je false, 1 ako je true a 0 ako je undef
    def get_value_of_var(self, var:int):
        if var in self.partial_valuation:
            return 1 #true
        elif -var in self.partial_valuation:
            return -1 #false
        else:
            return 0 #undef

# vrednost formule cnf_formula u valuaciji partial_valuation - proveravamo samo ako je partial_valuation zapravo potpuna val.
    def valuation(self):
        for clause in self.formula:
            tmp_clause = False
            for lit in clause:
                val = self.get_value_of_var(lit)
                if val==1:
                    tmp_clause=True
                    break
            if not tmp_clause:
                return False
        return True
    
# solve funkcija treba da vrati jedan model ako je formula zadovoljiva
# a mozda i ne? zbog rekurzije - videti to
    def solve(self)->List[int]:
        return self.partial_valuation

# proverava da li je partial_val potpuna
    def is_complete(self):
        for clause in self.formula:
            for lit in clause:
                if lit not in self.partial_valuation and -lit not in self.partial_valuation:
                    return False
        return True