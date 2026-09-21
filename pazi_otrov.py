from graph_viz import *

g = load_graph(15)


# #------------
# # Brute-force

# otvorene_rute = [[0]]
# najbolja_duzina = None
# najbolja_ruta = []

# while len(otvorene_rute) > 0:
#     trenutna = otvorene_rute.pop()

#     if len(trenutna) == g.n:
#         duzina = tour_length(g, trenutna)
#         if duzina < najbolja_duzina:
#             najbolja_duzina = duzina
#             najbolja_ruta = trenutna
#     else:
#         grad = 0
#         while grad < g.n:
#             if grad not in trenutna:
#                 otvorene_rute.append(trenutna + [grad])
#             grad = grad + 1

# run(g, najbolja_ruta)


#------------------
# Nearest Neighbor

trenutni = 0
ruta = [trenutni]

while len(ruta) < g.n:
    najblizi_grad = None
    najmanja_duzina = None
    
    kandidat = 0
    while kandidat < g.n:
        if kandidat not in ruta:
            duzina = g.D[trenutni][kandidat]
            if najmanja_duzina is None or duzina < najmanja_duzina:
                najmanja_duzina = duzina
                najblizi_grad = kandidat
        kandidat = kandidat + 1
        
    ruta.append(najblizi_grad)
    trenutni = najblizi_grad

run(g, ruta)
