"""
Graf pećine (sve distance u METRIMA, razmera sa papira: 1 cm = 2 m, tj. 1:200).

S      = stanica u sredini iz koje su mereni svi pravci
T1..T11 = tačke na obodu pećine, numerisane redom kao na listu sa razmerama
         (T1 je kod ulaza; idu redom po obodu: T1 -> T2 -> ... -> T11 -> T1)

Koordinate: x = istok, y = sever, S = (0, 0).
(Sa fotografije su očitani samo pravci/uglovi; dužine su iz merenja.)
"""

RAZMERA_M_PO_CM = 2.0  # 1 cm na papiru = 2 m u stvarnosti

# --- čvorovi: ime -> (x_istok, y_sever) u metrima ---
CVOROVI = {
    "S":   (0.00,   0.00),
    "T1":  (-7.13,  12.35),   # kod ulaza
    "T2":  (-7.84,  10.40),   # ulaz
    "T3":  (-9.50,   3.27),   # gornji kraj stepenica
    "T4":  (-7.97,   0.84),
    "T5":  (-7.93,  -1.40),
    "T6":  (-8.43, -7.08),
    "T7":  (-10.30, -12.27),
    "T8":  (-8.53, -14.77),
    "T9":  (12.00,   0.00),
    "T10": (6.98,    4.03),
    "T11": (6.17,    5.18),
}

# --- ivice: (a, b, distanca_m, opis) ---
# 1) merenja iz stanice S (stvarne izmerene vrednosti sa drugog lista)
MERENJA_IZ_S = [
    ("S", "T1",  14.26, "put/pravac ka ulazu"),
    ("S", "T2",  13.02, ""),
    ("S", "T3",  10.05, ""),
    ("S", "T4",   8.01, ""),
    ("S", "T5",   8.05, ""),
    ("S", "T6",  11.01, ""),
    ("S", "T7",  16.02, ""),
    ("S", "T8",  17.06, ""),
    ("S", "T9",  12.00, ""),
    ("S", "T10",  8.06, ""),
    ("S", "T11",  8.06, ""),
]

# 2) obod pećine (izračunato iz uglova sa mape i izmerenih rastojanja)
OBOD = [
    ("T1", "T2",   2.1, "ulaz"),
    ("T2", "T3",   7.3, "stepenice"),
    ("T3", "T4",   2.9, ""),
    ("T4", "T5",   2.2, ""),
    ("T5", "T6",   5.7, ""),
    ("T6", "T7",   5.5, ""),
    ("T7", "T8",   3.1, ""),
    ("T8", "T9",  25.3, "zid"),
    ("T9", "T10",   6.4, "stene"),
    ("T10", "T11",   1.4, ""),
    ("T11", "T1",  15.1, "zid"),
]

IVICE = MERENJA_IZ_S + OBOD


def napravi_graf():
    """Vraća networkx.Graph sa atributima 'weight' (m) i 'opis'."""
    import networkx as nx
    G = nx.Graph()
    for ime, (x, y) in CVOROVI.items():
        G.add_node(ime, pos=(x, y))
    for a, b, d, opis in IVICE:
        G.add_edge(a, b, weight=d, opis=opis)
    return G


if __name__ == "__main__":
    for a, b, d, opis in IVICE:
        print(f"{a:>3} - {b:<3} {d:6.2f} m  {opis}")