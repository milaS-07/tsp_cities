import random
import time
from graph_viz import *


def brute_force(g):
    otvorene_rute = [[0]]
    najbolja_duzina = float("inf")
    najbolja_ruta = []

    while len(otvorene_rute) > 0:
        trenutna = otvorene_rute.pop()

        if len(trenutna) == g.n:
            duzina = tour_length(g, trenutna)
            if duzina < najbolja_duzina:
                najbolja_duzina = duzina
                najbolja_ruta = trenutna
        else:
            grad = 0
            while grad < g.n:
                if grad not in trenutna:
                    otvorene_rute.append(trenutna + [grad])
                grad = grad + 1

    return najbolja_ruta, najbolja_duzina


def nearest_neighbour(g):
    trenutna_ruta = [0]

    while len(trenutna_ruta) < g.n:
        trenutni_grad = trenutna_ruta[-1]

        najblizi_grad = None
        najmanja_udaljenost = None

        grad = 0
        while grad < g.n:
            if grad not in trenutna_ruta:
                udaljenost = g.D[trenutni_grad][grad]

                if (
                    najmanja_udaljenost is None
                    or udaljenost < najmanja_udaljenost
                ):
                    najmanja_udaljenost = udaljenost
                    najblizi_grad = grad

            grad = grad + 1

        trenutna_ruta.append(najblizi_grad)

    najbolja_duzina = tour_length(g, trenutna_ruta)
    return trenutna_ruta, najbolja_duzina


def genetski_algoritam(g):
    broj = g.n

    populacija = []
    for _ in range(2 * broj):
        jedinka = [[j for j in range(1, broj)], None]
        random.shuffle(jedinka[0])
        populacija.append(jedinka)

    matrica_distanci = g.D
    recn = {}
    for i in range(len(matrica_distanci)):
        for j in range(len(matrica_distanci)):
            recn[f"{i}-{j}"] = matrica_distanci[i][j]

    def izracunaj_duzinu(ruta):
        b = 0
        for k in range(len(ruta) - 1):
            b += recn[f"{ruta[k]}-{ruta[k + 1]}"]
        b += recn[f"{0}-{ruta[0]}"]
        b += recn[f"{ruta[-1]}-{0}"]
        return b

    zadnje_najbolje = float("inf")
    vreme_od_zadnjeg_najboljeg = 0
    najbolja_jedinka = populacija[0][0][:]

    max_generacija = 500
    for _ in range(max_generacija):

        for j in populacija:
            j[1] = izracunaj_duzinu(j[0])

        nova_populacija = []
        novo_l = []
        dok_populacija = populacija.copy()

        while dok_populacija:
            for _ in range(13):
                if not dok_populacija:
                    continue
                novo_l.append(
                    dok_populacija.pop(
                        random.randint(0, len(dok_populacija) - 1)
                    )
                )
            novo_l = sorted(novo_l, key=lambda x: x[1])

            for _ in range(13):
                nova_populacija.append([novo_l[0][0][:], novo_l[0][1]])
            novo_l.clear()

        roditelji = [[r[0][:], r[1]] for r in nova_populacija]

        deca = []
        while roditelji:
            roditelj1 = roditelji.pop(random.randint(0, len(roditelji) - 1))

            if roditelji:
                roditelj2 = roditelji.pop(
                    random.randint(0, len(roditelji) - 1)
                )
                n = [[-1 for _ in range(len(roditelj1[0]))], None]

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

        for j in populacija:
            if random.random() < 1 / 13:
                ox, oy = 0, 0
                while ox == oy:
                    ox = random.randint(0, len(j[0]) - 1)
                    oy = random.randint(0, len(j[0]) - 1)
                j[0][ox], j[0][oy] = j[0][oy], j[0][ox]

        for j in populacija:
            j[1] = izracunaj_duzinu(j[0])

        sortirana_populacija = sorted(populacija, key=lambda x: x[1])
        trenutno_najbolje = sortirana_populacija[0][1]

        if zadnje_najbolje > trenutno_najbolje:
            zadnje_najbolje = trenutno_najbolje
            vreme_od_zadnjeg_najboljeg = 0
            najbolja_jedinka = sortirana_populacija[0][0][:]
        else:
            vreme_od_zadnjeg_najboljeg += 1

        if vreme_od_zadnjeg_najboljeg > 10 * broj:
            break

    konacna_ruta = [0] + najbolja_jedinka
    konacna_duzina = izracunaj_duzinu(najbolja_jedinka)

    return konacna_ruta, konacna_duzina