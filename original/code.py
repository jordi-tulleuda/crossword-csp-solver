# GRUP_4_15:00 

import copy
import time

inicio = time.perf_counter()

nom_crossword = "./MaterialsPractica/crossword_A.txt"
nom_diccionari = "./MaterialsPractica/diccionari_A.txt"

class lletra:
    def __init__(self, valor, esInterseccio=False, top=None, right=None, down=None, left=None):
        self.valor = valor
        self.esInterseccio = esInterseccio
        self.top = top
        self.right = right
        self.down = down
        self.left = left

class forat_paraula:
    def __init__(self, mida = 0, vertical = None, casella_inicial = None, interseccions = None, id = None):
        self.mida = mida
        self.vertical = vertical
        self.casella_inicial = casella_inicial
        self.interseccions = [] if interseccions is None else interseccions
        self.id = id

# --- Secció: Lectura Matriu
mat = []
with open(nom_crossword, "r") as f:
    for linea in f:
        linea2 = []
        for c in linea:
            if c == '0' or c == '#':
                linea2.append(c)
        mat.append(linea2)

# Matriu de lletres i chars
mat2 = copy.deepcopy(mat)
for i in range(len(mat2)):
    for j in range(len(mat2[i])):
        if mat2[i][j] == '0':
            lletra_actual = lletra(mat2[i][j])
            mat2[i][j] = lletra_actual

for i in range(len(mat2)):
    for j in range(len(mat2[i])):
        lletra_actual = mat2[i][j]
        if (isinstance(lletra_actual, lletra) == True):
            if (i > 0 and isinstance(mat2[i-1][j], lletra)): lletra_actual.top = mat2[i-1][j]
            if (i < len(mat2)-1 and isinstance(mat2[i+1][j], lletra)): lletra_actual.down = mat2[i+1][j]
            if (j > 0 and isinstance(mat2[i][j-1], lletra)): lletra_actual.left = mat2[i][j-1]
            if (j < len(mat2[i])-1 and isinstance(mat2[i][j+1], lletra)): lletra_actual.right = mat2[i][j+1]
            lletra_actual.esInterseccio = bool((lletra_actual.top and lletra_actual.right) or (lletra_actual.top and lletra_actual.left) or (lletra_actual.down and lletra_actual.right) or (lletra_actual.down and lletra_actual.left))
            mat2[i][j] = lletra_actual

# --- Secció: Forats
# Horitzontal
forats_paraules = []
tmp = forat_paraula()
mida_mat_vert = len(mat2)
for i in range(mida_mat_vert):
    mida_mat_horz = len(mat2[i])
    for j in range(mida_mat_horz):
        element_actual = mat2[i][j]
        if isinstance(element_actual, lletra):
            if element_actual.esInterseccio:
                tmp.interseccions.append([i, j, tmp.mida])
            if tmp.casella_inicial is None:
                tmp.casella_inicial = ([i, j])
            tmp.mida = tmp.mida + 1
            if (isinstance(element_actual.right, lletra) == False):
                if  tmp.mida > 1:
                    tmp.vertical = False
                    forats_paraules.append(tmp)
                tmp = forat_paraula()
        else:
            tmp = forat_paraula()

# Vertical
for j in range(len(mat2[0])):
    tmp = forat_paraula()
    for i in range(len(mat2)):
        element_actual = mat2[i][j]
        if isinstance(element_actual, lletra):
            if element_actual.esInterseccio:
                tmp.interseccions.append([i, j, tmp.mida])
            if tmp.casella_inicial is None:
                tmp.casella_inicial = [i, j]
            tmp.mida += 1
            if not isinstance(element_actual.down, lletra):
                if tmp.mida > 1:
                    tmp.vertical = True
                    forats_paraules.append(tmp)
                tmp = forat_paraula()
        else:
            tmp = forat_paraula()

for n, forat in enumerate(forats_paraules):
    forat.id = n

# --- Secció: Diccionari/Domini
mides_necessaries = []
for forat in forats_paraules:
    mida = forat.mida
    if mida not in mides_necessaries:
        mides_necessaries.append(mida)

diccionari = {}
for mida in mides_necessaries:
    diccionari[mida] = []

with open(nom_diccionari, "r", encoding="latin-1") as f:
    for linia in f:
        paraula = linia.strip()
        mida = len(paraula)

        if mida in mides_necessaries:
            diccionari[mida].append(paraula)

# --- Secció: Creuaments/veins
creuaments = {}
for forat in forats_paraules:
    for i, j, pos in forat.interseccions:
        coordenades = (i, j)
        if coordenades not in creuaments:
            creuaments[coordenades] = []
        creuaments[coordenades].append((forat.id, pos))

veins = {}
for forat in forats_paraules:
    veins[forat.id] = []
posicions = {}
for elements in creuaments.values():
    if len(elements) == 2:
        (a, pos_a), (b, pos_b) = elements
        veins[a].append(b)
        veins[b].append(a)

        posicions[(a, b)] = (pos_a, pos_b)
        posicions[(b, a)] = (pos_b, pos_a)

# --- Secció: Cerca
def satisfaRestriccions(paraula_candidata, forat_actual, mat2):
    if forat_actual.mida != len(paraula_candidata):
        return False
    for i, j, pos in forat_actual.interseccions:
        valor_actual = mat2[i][j].valor
        if valor_actual != '0' and valor_actual != paraula_candidata[pos]:
            return False
    return True

def forwardChecking(forat_assignat, paraula_assignada, forats_restants, dominis_actuals):
    nous_dominis = dominis_actuals.copy()
    id_assignat = forat_assignat.id
    veins_actuals = veins[id_assignat]
    for forat_actual in forats_restants:
        id_vei = forat_actual.id
        if id_vei in veins_actuals:
            pos_assignat, pos_vei = posicions[(id_assignat, id_vei)]
            lletra_necessaria = paraula_assignada[pos_assignat]

            paraules_valides = []
            for paraula_candidata in dominis_actuals[id_vei]:
                if paraula_candidata[pos_vei] == lletra_necessaria:
                    paraules_valides.append(paraula_candidata)
            if not paraules_valides:
                return None
            nous_dominis[id_vei] = paraules_valides

    return nous_dominis

def backtracking(forats_assignats, forats_no_assignats, dominis_actuals, mat2):
    if len(forats_no_assignats) == 0:
        return forats_assignats

    # Escollim el forat amb menys possibilitats/paraules en aquell domini
    forat_actual = min(forats_no_assignats, key=lambda f: len(dominis_actuals[f.id])) # MRV
    clau_forat = forat_actual.id

    paraules_utilitzades = []
    for posicio, paraula in forats_assignats:
        if paraula not in paraules_utilitzades:
            paraules_utilitzades.append(paraula)

    for paraula_candidata in dominis_actuals[clau_forat]:
        if paraula_candidata not in paraules_utilitzades and satisfaRestriccions(paraula_candidata, forat_actual, mat2):
            backup_posicions = forat_actual.interseccions.copy()
            backup_lletres = [mat2[i][j].valor for i, j, _ in backup_posicions]

            for i, j, pos in forat_actual.interseccions:
                mat2[i][j].valor = paraula_candidata[pos]

            forats_restants = []
            for forat in forats_no_assignats:
                if forat is not forat_actual:
                    forats_restants.append(forat)
            nous_dominis = forwardChecking(forat_actual, paraula_candidata, forats_restants, dominis_actuals)
            # Guardar interseccio i checkejar només les lletres que son interseccio.
            if nous_dominis is not None:
                
                res = backtracking(forats_assignats + [[forat_actual, paraula_candidata]], forats_restants, nous_dominis, mat2)
                if res is not None:
                    return res

            for posicio, lletra_anterior in zip(backup_posicions, backup_lletres):
                mat2[posicio[0]][posicio[1]].valor = lletra_anterior
    return None

dominis_inicials = {}
for forat in forats_paraules:
    clau_forat = forat.id
    dominis_inicials[clau_forat] = diccionari[forat.mida].copy()

llista_forats_assignats = []
forats_no_assignats = forats_paraules
resultat = backtracking(llista_forats_assignats, forats_no_assignats, dominis_inicials, mat2)

def printmat(mat2):
    if resultat is None:
        print('No hi ha resultat.')
    else:
        for forat, paraula in resultat:
            i, j = forat.casella_inicial
            for lletra_p in paraula:
                mat2[i][j].valor = lletra_p
                if forat.vertical:
                    i += 1
                else:
                    j += 1
        print('Resultat: ')
        for i in range(len(mat2)):
            for j in range(len(mat2[i])):
                lletra_actual = mat2[i][j]
                if isinstance(lletra_actual, lletra):
                    print(lletra_actual.valor, end=" ")
                else:
                    print(lletra_actual, end=" ")
            print('\n')

printmat(mat2)

fin = time.perf_counter()

print(f"Temps: {fin - inicio:.4f} s")