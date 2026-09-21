from graph_viz import *

#1. Učitavanje grafa (5 ovde predstavlja broj gradova)
g = load_graph(5)


#2. Dobijanje informacija o grafu
broj_cvorova = g.n
#mozda bude kasnije trebalo
matrica_distanci = g.D


#3. Dobijanje distancije između dva konkretna čvora

distanca_0_do_1 = g.D[0][1]  # Udaljenost u km od 0. do 1. grada
distanca_1_do_3 = g.D[1][3]  # Udaljenost u km od 1. do 3. grada


#4. Izračunavanje ukupne dužine rute (bez crtanja i bez printanja)
moja_ruta = [0, 2, 1, 4, 3]
ukupna_duzina = tour_length(g, moja_ruta)  # Vraća ukupnu kilometražu (float)

#5. Pokretanje
moja_ruta = [0, 2, 1, 4, 3]
run(g, moja_ruta)