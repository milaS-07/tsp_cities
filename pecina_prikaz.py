import math

import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.patches import Polygon

from pecina import CVOROVI, IVICE

INK, MUTED, EDGE, LAND, BORDER, STANICA = "#12233F", "#5A6779", "#8E9AAB", "#EEF1EA", "#9AA5B1", "#D1495B"
BOJE_OPISA = {"ulaz": "#2A9D8F", "stepenice": "#E9A23B"}   # posebno obojene ivice

OBOD_REDOM = [f"T{i}" for i in range(1, 12)]               # T1 -> T2 -> ... -> T11 -> T1


def _oznaka_ivice(ax, a, b, tekst, fs, t=0.5):
    (xa, ya), (xb, yb) = CVOROVI[a], CVOROVI[b]
    x, y = xa + t * (xb - xa), ya + t * (yb - ya)
    ugao = math.degrees(math.atan2(yb - ya, xb - xa))
    if ugao > 90:
        ugao -= 180
    if ugao <= -90:
        ugao += 180
    ax.text(x, y, tekst, fontsize=fs, color=MUTED, ha="center", va="center",
            rotation=ugao, rotation_mode="anchor", zorder=4, linespacing=0.95,
            bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=.9))


def show_graph(merenja=True, oznake=True):
    """
    merenja : crtati i linije iz stanice S ka tačkama na obodu
    oznake  : ispisati distancu (u metrima) na svakoj grani
    """
    fig, ax = plt.subplots(figsize=(9, 10))

    # unutrašnjost pećine (kao "teritorija" u TSP prikazu)
    ax.add_patch(Polygon([CVOROVI[k] for k in OBOD_REDOM], closed=True,
                         facecolor=LAND, edgecolor="none", zorder=0))

    for a, b, d, opis in IVICE:
        (xa, ya), (xb, yb) = CVOROVI[a], CVOROVI[b]
        je_merenje = "S" in (a, b)
        if je_merenje and not merenja:
            continue
        if je_merenje:
            boja, lw, alpha, z = EDGE, 0.9, .6, 2
        else:
            boja, lw, alpha, z = BOJE_OPISA.get(opis, BORDER), 2.6, 1, 3
        ax.plot([xa, xb], [ya, yb], color=boja, lw=lw, alpha=alpha,
                solid_capstyle="round", zorder=z)
        if oznake:
            t = 0.62 if je_merenje else 0.5
            _oznaka_ivice(ax, a, b, f"{d:.1f}", 8.5, t)
            if opis in BOJE_OPISA:                       # naziv ispisan sa spoljne strane, van pećine
                mx, my = (xa + xb) / 2, (ya + yb) / 2
                r = math.hypot(mx, my) or 1
                ax.text(mx + 2.3 * mx / r, my + 2.3 * my / r, opis, fontsize=9, fontweight="bold",
                        color=BOJE_OPISA[opis], ha="center", va="center", zorder=7,
                        path_effects=[pe.withStroke(linewidth=2.2, foreground="white")])

    # čvorovi
    xs = [p[0] for p in CVOROVI.values()]
    ys = [p[1] for p in CVOROVI.values()]
    ax.scatter(xs, ys, s=70, color=INK, edgecolor="white", linewidth=1.5, zorder=5)
    sx, sy = CVOROVI["S"]
    ax.scatter([sx], [sy], s=150, color=STANICA, edgecolor="white", linewidth=1.5, zorder=6)

    halo = [pe.withStroke(linewidth=2.2, foreground="white")]
    for ime, (x, y) in CVOROVI.items():
        ax.annotate(ime, (x, y), xytext=(7, 6), textcoords="offset points",
                    fontsize=10, fontweight="bold", color=INK, path_effects=halo, zorder=7)

    # okvir, sever gore
    ax.set_xlim(min(xs) - 3, max(xs) + 3)
    ax.set_ylim(min(ys) - 3, max(ys) + 3)
    ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.annotate("sever", xy=(0.96, 0.95), xytext=(0.96, 0.88), xycoords="axes fraction",
                ha="center", va="center", fontsize=11, fontweight="bold", color=MUTED,
                arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.5))   # strelica ka severu

    n_ivica = len(IVICE) if merenja else sum(1 for a, b, *_ in IVICE if "S" not in (a, b))
    ax.set_title(f"Pećina: {len(CVOROVI)} čvorova, {n_ivica} grana", loc="left",
                 fontsize=16, fontweight="bold", color=INK)
    ax.set_xlabel("Broj na svakoj grani: stvarna distanca u metrima (1 cm na papiru = 2 m)",
                  loc="left", color=MUTED)
    plt.show()


if __name__ == "__main__":
    show_graph()