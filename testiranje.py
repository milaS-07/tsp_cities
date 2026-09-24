import time
from algorithms import *
from graph_viz import *


N = 10                  #broj čvorova
ALGORITAM = "bf"   #izbor: "bf", "nn", "ga"
BROJ_GA_RUNOVA = 5      #koliko puta ćete pokrenuti GA


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

    for i in range(BROJ_GA_RUNOVA):
        t0 = time.perf_counter()
        ga_ruta, ga_duzina = genetski_algoritam(g)
        t_ga = time.perf_counter() - t0

        ga_duzine.append(ga_duzina)
        ga_vremena.append(t_ga)
        poslednja_ga_ruta = ga_ruta
        print(f"    > Pokretanje #{i+1}: Dužina = {ga_duzina:.2f} | Vreme = {t_ga:.4f} s")

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