from graph_viz import *

g = load_graph(5)


#------------
# Brute-force

otvorene_rute = [[0]]
najbolja_duzina = None
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

run(g, najbolja_ruta)
