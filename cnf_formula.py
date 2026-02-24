from typing import List
class CNFFormula:
    def __init__(self, clauses: List[List[int]]):
        self.clauses = clauses
        self.n_clauses = len(clauses)
        self.watched_per_clause = {} # mapa koja slika indeks klauze u par njegovih watched literala
        self.literal_to_clauses = {} # mapa koja cuva slika literal u klauze u kojima je on watched
        for i,clause in enumerate(clauses):
            if len(clause)>=2:
                watched = (clause[0],clause[1])
            elif len(clause)==1:
                watched = (clause[0],clause[0])
            else:
                continue # prazna klauza
            self.watched_per_clause[i] = watched
            self.literal_to_clauses.setdefault(watched[0],set()).add(i)
            self.literal_to_clauses.setdefault(watched[1],set()).add(i)

def read_dimacs(filename:str)->CNFFormula:
    res = []
    with open(filename,"r") as f:
        # preskacem sve komentare na pocetku dok ne dodjem do linije koja je pravi pocetak - iz nje citam broj klauza i promenljivih
        for line in f:
            if line.startswith('c'):
                continue
            if line.startswith('p'):
                parts = line.split()
                num_of_vars = int(parts[2]) # da li negde treba da cuvam num_of_vars?
                break
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
