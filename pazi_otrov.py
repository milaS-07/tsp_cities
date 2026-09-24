from graph_viz import *

g = load_graph(5)


#------------
# Brute-force

otvorene_rute = [[0]]
najbolja_duzina = 9999999
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


# -----------------
# Nearest Neighbour
# -----------------

trenutna_ruta = [0]

while len(trenutna_ruta) < g.n:
    trenutni_grad = trenutna_ruta[-1]

    najblizi_grad = None
    najmanja_udaljenost = None

    grad = 0
    while grad < g.n:
        if grad not in trenutna_ruta:
            # Matrica rastojanja (g.D)
            udaljenost = g.D[trenutni_grad][grad]

            if najmanja_udaljenost is None or udaljenost < najmanja_udaljenost:
                najmanja_udaljenost = udaljenost
                najblizi_grad = grad

        grad = grad + 1

    trenutna_ruta.append(najblizi_grad)

najbolja_ruta = trenutna_ruta
najbolja_duzina = tour_length(g, najbolja_ruta)

run(g, najbolja_ruta)