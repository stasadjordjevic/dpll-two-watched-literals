from typing import List
class CNFFormula:
    def __init__(self, clauses: List[List[int]]):
        self.clauses = clauses
        self.n_clauses = len(clauses)
        self.wached_per_clause = {} # mapa koja slika indeks klauze u par njegovih watched literala
        self.literal_to_clauses = {} # mapa koja cuva slika literal u klauze u kojima je on watched
        for i,clause in enumerate(clauses):
            if len(clause)>=2:
                watched = (clause[0],clause[1])
            elif len(clause)==1:
                watched = (clause[0],clause[0])
            else:
                continue # prazna klauza
            self.wached_per_clause[i] = watched
            self.literal_to_clauses.setdefault(watched[0],set()).add(i)
            self.literal_to_clauses.setdefault(watched[1],set()).add(i)

def read_dimacs(filename:str)->CNFFormula:
    res = []
    with open(filename,"r") as f:
        # prvo cita prvu liniju da vidi koliko klauza ima
        first_line = f.readline().split()
        num_of_vars = int(first_line[2])
        num_of_clauses = int(first_line[3])
        for line in f:
            line = line.split()
            # komentar pocinje sa c - preskacemo ga
            if line[0]=="c":
                continue
            clause = []
            for l in line:
                if l == "0":
                    break
                if abs(int(l))>num_of_vars:
                    print("wrong clause format!")
                    break
                clause.append(int(l))
            res.append(clause)
    return CNFFormula(res)

# f = read_dimacs("proba.cnf")
# print(f.clauses)