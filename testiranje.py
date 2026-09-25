import time
import random
from algorithms import *
from graph_viz import *


N = 3              # broj čvorova
ALGORITAM = "bf"   # izbor: "bf", "nn", "ga"
BROJ_GA_RUNOVA = 5 # koliko puta ćete pokrenuti GA


g = load_graph(N)

print("=" * 65)
print(f"POKRETANJE EKSPERIMENTA: Graf sa n = {N} čvorova")
print("=" * 65)

if ALGORITAM in ["bf", "sva_tri"]:
    print("\n[1] Pokrećem Brute-Force...")
    t0 = time.perf_counter()
    bf_ruta, bf_duzina = brute_force(g)
    t_bf = time.perf_counter() - t0

    print(f"    Ruta: {bf_ruta}")
    print(f"    Dužina: {bf_duzina:.2f}")
    print(f"    Vreme:  {t_bf:.4f} s")

    if ALGORITAM == "bf":
        run(g, bf_ruta)


if ALGORITAM in ["nn", "sva_tri"]:
    print("\n[2] Pokrećem Nearest Neighbour...")
    t0 = time.perf_counter()
    nn_ruta, nn_duzina = nearest_neighbour(g)
    t_nn = time.perf_counter() - t0

    print(f"    Ruta: {nn_ruta}")
    print(f"    Dužina: {nn_duzina:.2f}")
    print(f"    Vreme:  {t_nn:.4f} s")

    # Ako je izabran samo NN, prikaži graf za njega
    if ALGORITAM == "nn":
        run(g, nn_ruta)


if ALGORITAM in ["ga", "sva_tri"]:
    print(f"\n[3] Pokrećem Genetski Algoritam ({BROJ_GA_RUNOVA}x)...")

    ga_duzine = []
    ga_vremena = []
    poslednja_ga_ruta = []

    for run_idx in range(BROJ_GA_RUNOVA):
        t0 = time.perf_counter()

        # --- PRIPREMA GA ---
        broj = N

        populacija = []
        for i in range(2 * broj):
            l = [[j for j in range(1, broj)], None]
            random.shuffle(l[0])
            populacija.append(l)

        matrica_distanci = g.D

        recn = {}
        for i in range(0, len(matrica_distanci)):
            for j in range(0, len(matrica_distanci)):
                recn[f"{i}-{j}"] = matrica_distanci[i][j]

        zadnjeNajbolje = float("inf")
        vremeOdZadnjegNajboljeg = 0

        # --- GLAVNA PETLJA GA ---
        i = 0
        while True:

            """CILJ"""
            for j in populacija:
                b = 0
                for k in range(len(j[0]) - 1):
                    b += recn[f"{j[0][k]}-{j[0][k + 1]}"]
                b += recn[f"{0}-{j[0][0]}"]
                b += recn[f"{j[0][-1]}-{0}"]
                j[1] = b

            """SELEKCIJA"""
            novaPopulacija = []
            novoL = []
            while populacija:
                for m in range(13):
                    if not populacija:
                        continue
                    novoL.append(populacija.pop(random.randint(0, len(populacija) - 1)))
                novoL = sorted(novoL, key=lambda x: x[1])
                for m in range(13):
                    novaPopulacija.append([novoL[0][0][:], novoL[0][1]])
                novoL.clear()

            roditelji = [[r[0][:], r[1]] for r in novaPopulacija]

            """UKRSTANJE"""
            deca = []

            while roditelji:
                roditelj1 = roditelji.pop(random.randint(0, len(roditelji) - 1))

                if roditelji:
                    roditelj2 = roditelji.pop(random.randint(0, len(roditelji) - 1))
                    n = [[-1 for ni in range(len(roditelj1[0]))], None]
                    cx = random.randint(0, len(roditelj1[0]) - 1)
                    cy = random.randint(0, len(roditelj1[0]) - 1)
                    if cx > cy:
                        cx, cy = cy, cx

                    for j in range(len(n[0])):
                        if cx < j < cy:
                            n[0][j] = roditelj1[0][j]

                    ostali = [k for k in roditelj2[0] if k not in n[0]]
                    for k in range(len(n[0])):
                        if n[0][k] == -1:
                            n[0][k] = ostali.pop(0)
                else:
                    n = roditelj1

                deca.append(n)
                deca.append([n[0][:], None])

            populacija = deca.copy()
            deca = []

            """MUTACIJE"""
            if i < 9987:
                for j in populacija:
                    if random.random() < 1/13:
                        ox, oy = 0, 0
                        while ox == oy:
                            ox = random.randint(0, len(j[0]) - 1)
                            oy = random.randint(0, len(j[0]) - 1)
                        j[0][ox], j[0][oy] = j[0][oy], j[0][ox]

            """EVALUACIJA PROGRESA"""
            for j in populacija:
                b = 0
                for k in range(len(j[0]) - 1):
                    b += recn[f"{j[0][k]}-{j[0][k + 1]}"]
                b += recn[f"{0}-{j[0][0]}"]
                b += recn[f"{j[0][-1]}-{0}"]
                j[1] = b

            sortiranaPopulacija = sorted(populacija.copy(), key=lambda x: x[1])

            if zadnjeNajbolje > sortiranaPopulacija[0][1]:
                vremeOdZadnjegNajboljeg = 0
                zadnjeNajbolje = sortiranaPopulacija[0][1]
            else:
                vremeOdZadnjegNajboljeg += 1

            if vremeOdZadnjegNajboljeg > 10 * broj:
                print("Zavrseno zbog stagnacije!")
                break

            i += 1

        oli = [0]
        for item in populacija[0][0]:
            oli.append(item)

        ga_ruta = oli
        ga_duzina = zadnjeNajbolje

        t_ga = time.perf_counter() - t0

        ga_duzine.append(ga_duzina)
        ga_vremena.append(t_ga)
        poslednja_ga_ruta = ga_ruta
        print(f"    > Pokretanje #{run_idx+1}: Dužina = {ga_duzina:.2f} | Vreme = {t_ga:.4f} s")

    min_ga = min(ga_duzine)
    avg_ga = sum(ga_duzine) / BROJ_GA_RUNOVA
    avg_t_ga = sum(ga_vremena) / BROJ_GA_RUNOVA

    print(f"\n    --- SAŽETAK ZA GA ---")
    print(f"    Najbolja dužina:  {min_ga:.2f}")
    print(f"    Prosečna dužina:  {avg_ga:.2f}")
    print(f"    Prosečno vreme:   {avg_t_ga:.4f} s")

    if ALGORITAM == "ga":
        run(g, poslednja_ga_ruta)

print("\n" + "=" * 65)