from typing import List
from cnf_formula import CNFFormula

class DPLLSolver:
    def __init__(self, formula:CNFFormula):
        self.formula = formula
        self.partial_valuation = set()
# vraca -1 ako je false, 1 ako je true a 0 ako je undef

    def assign(self, lit):
        self.partial_valuation.add(lit)

    def get_value_of_var(self, var:int):
        if var in self.partial_valuation:
            return 1 #true
        elif -var in self.partial_valuation:
            return -1 #false
        else:
            return 0 #undef
        
    def is_sat(self)->bool:
        formula_satisfied = True
        for clause in self.formula.clauses:
            clause_satisfied = False
            for lit in clause:
                if self.get_value_of_var(lit) == 1:
                    clause_satisfied = True
                    break  # klauza je zadovoljena
            if not clause_satisfied:
                formula_satisfied = False
                break  # pronađena klauza koja nije zadovoljena
        return formula_satisfied
    
    # proverava da li je partial_val potpuna
    def is_complete(self):
        for clause in self.formula.clauses:
            for lit in clause:
                if lit not in self.partial_valuation and -lit not in self.partial_valuation:
                    return False
        return True
    
    def is_unsat(self):
        for clause in self.formula.clauses:
            if all(self.get_value_of_var(lit)==-1 for lit in clause):
                return True
        return False

    
    # heuristika za biranje sledeceg literala koji je undef - vraca None ako su svi def
    def pick_unassigned(self):
        for clause in self.formula.clauses:
            for lit in clause:
                if self.get_value_of_var(lit)==0:
                    return lit
        return None # svi su dodeljeni
    

# vrednost formule cnf_formula u valuaciji partial_valuation - proveravamo samo ako je partial_valuation zapravo potpuna val.
    def valuation(self):
        for clause in self.formula.clauses:
            tmp_clause = False
            for lit in clause:
                val = self.get_value_of_var(lit)
                if val==1:
                    tmp_clause=True
                    break
            if not tmp_clause:
                return False
        return True
    
    # snimanje i vracanje stanja - backtracking
    def _save_state(self):
        return set(self.partial_valuation)

    def _restore_state(self, state):
        self.partial_valuation = state
    
    # pronalazi pure literale i dodeljuje im vrednosti
    def pure_literal(self):
        pos = set()
        neg = set()
        for clause in self.formula.clauses:
            # ako postoji pozitivan literal u klauzi preskacemo je - ona je svakako tacna
            if any(self.get_value_of_var(l)==1 for l in clause):
                continue
            for lit in clause:
                # proveravamo samo undef
                if self.get_value_of_var(lit)==0:
                    if lit>0: 
                        pos.add(lit)
                    else:
                        neg.add(-lit) # cuvamo samo "iskazno slovo" bez znaka - zbog razlike skupova
        pure_pos = pos - neg # oni koji su samo pozitivni
        pure_neg = neg - pos # oni koji su samo negativni
        for var in pure_pos:
            # self.assign(var)
            return var
        for var in pure_neg:
            # self.assign(-var)
            return -var
        return None


    def unit_propagate(self, literal):
        self.assign(literal)
        queue = [literal]
        while queue:
            lit = queue.pop()
            false_lit = -lit # u svim klauzulama gde je -l menjamo watched (one gde je samo l nestaju - postaju tacne)
            watched_clauses = list(self.formula.literal_to_clauses.get(false_lit, set()))
            for clause_idx in watched_clauses:
                clause = self.formula.clauses[clause_idx]
                w1, w2 = self.formula.watched_per_clause[clause_idx]
                #koji je drugi posmatrani literal (jedan od njih je sig false_lit)
                other = w1
                if w1==false_lit:
                    other = w2 

                #ova klauza je vec zadovoljena
                if self.get_value_of_var(other)==1:
                    continue 

                # trazimo alternativni posmatrani literal
                new_w = None
                for candidate in clause:
                    if candidate != false_lit and candidate != other:
                        if self.get_value_of_var(candidate) != -1:
                            new_w = candidate
                            break
                
                if new_w is not None:
                    self.formula.literal_to_clauses[false_lit].discard(clause_idx) #??
                    if new_w not in self.formula.literal_to_clauses:
                        self.formula.literal_to_clauses[new_w] = set()
                    self.formula.literal_to_clauses[new_w].add(clause_idx)
                    # gledamo da li new_w menja w1 ili w2 i menjamo ga u skupu wpc[clause_idx]
                    if w1==false_lit:
                        self.formula.watched_per_clause[clause_idx] = (new_w,w2)
                    else:
                        self.formula.watched_per_clause[clause_idx] = (w1,new_w)
                else:
                    #nema zamene - preostaje nam samo da vidimo da l 
                    if self.get_value_of_var(other)==-1:
                        return False
                    else:
                        # proveravamo da l other moze da bude tacno i da ne dodje do konflikta
                        self.assign(other)
                        queue.append(other)
        return True

    def dpll(self):
        if self.is_unsat():
            return None
        
        if self.is_complete():
            return list(self.partial_valuation)
        
        # unit propagate
        for clause in self.formula.clauses:
            if any(self.get_value_of_var(l)==1 for l in clause):
                continue # klauza je tacna
            undef = [l for l in clause if self.get_value_of_var(l)==0]
            if len(undef)==0:
                return None
            if len(undef)==1:
                state = self._save_state()
                if not self.unit_propagate(undef[0]):
                    self._restore_state(state)
                    return None
                result = self.dpll()
                if result is None:
                    self._restore_state(state)
                return result
        
        # pure literal 
        pure_lit = self.pure_literal()
        if pure_lit is not None:
            self.assign(pure_lit)
            return self.dpll()
        
        # split pravilo - biramo prvo literal
        lit = self.pick_unassigned()
        if lit is None:
            return None
        
        # pokusavamo da dodelimo literalu vrednost tacno
        state = self._save_state()
        if self.unit_propagate(lit):
            result = self.dpll()
            if result is not None:
                return result
        self._restore_state(state)
        # pokusavamo da dodelimo literalu vrednost netacno
        state = self._save_state()
        if self.unit_propagate(-lit):
            result = self.dpll()
            if result is not None:
                return result
        self._restore_state(state)

        return None # ne moze ni lit ni -lit  --> nema resenja

    def print_result(self, res):
        if res is None:
            print("UNSAT")
            return
        print("SAT")
        print("model:", " ".join(str(lit) for lit in res))

# solve funkcija treba da vrati jedan model ako je formula zadovoljiva
    def solve(self):
        # proveri da l ima prazna klauza
        for clause in self.formula.clauses:
            if len(clause)==0:
                return None
        # proveri da li je skup klauza prazan
        if len(self.formula.clauses)==0:
            return []
        
        #proveri inicijalne jedinicne klauze
        for clause in self.formula.clauses:
            if len(clause)==1:
                lit = clause[0]
                val = self.get_value_of_var(lit)
                # u jedinicnoj klauzi se nalazi neki koji je negativan u parcijalnoj val. ==> konflikt
                if val==-1:
                    return None
                # ako je undef dodeljujemo 
                if val==0:
                    if not self.unit_propagate(lit):
                        return None

                
        return self.dpll()
