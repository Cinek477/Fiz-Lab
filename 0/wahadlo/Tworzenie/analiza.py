"""Obliczenia NumPy i wykres Matplotlib: python analiza.py."""
from pathlib import Path
import csv
import json
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MultipleLocator

ROOT = Path(__file__).resolve().parent
DATA = ROOT.parent / 'Dane'
CHARTS = ROOT.parent / 'PDF' / 'Wykresy'
CHARTS.mkdir(parents=True, exist_ok=True)


def read_csv(name):
    with (DATA / name).open(encoding="utf-8", newline="") as source:
        return list(csv.DictReader(source))


def write(name, content):
    (ROOT / name).write_text(content, encoding="utf-8")


def pl(value, digits):
    return f"{value:.{digits}f}".replace(".", "{,}")


def main():
    rows = read_csv("dane.csv")
    raw = read_csv("dane_pierwszy.csv")
    params = json.loads((DATA / "parametry_pierwszy.json").read_text(encoding="utf-8"))
    x = [float(r["L_cm"]) / 100 for r in rows]
    ux = [float(r["u_L_cm"]) / 100 for r in rows]
    t = [float(r["T_s"]) for r in rows]
    ut = [float(r["u_T_s"]) for r in rows]
    first_raw = [float(r["t10_s"]) for r in raw]
    length, u_length = params["L_m"], params["u_L_m"]
    if len(x) < 2 or len(first_raw) < 2:
        raise ValueError("Potrzeba co najmniej dwóch punktów i dwóch powtórzeń.")
    values = x + ux + t + ut + first_raw + [length, u_length]
    if not all(math.isfinite(v) for v in values):
        raise ValueError("Dane muszą być skończone.")
    if min(x + t + first_raw + [length]) <= 0 or min(ux + ut + [u_length]) < 0:
        raise ValueError("Długości i czasy muszą być dodatnie; niepewności nieujemne.")
    periods = np.asarray(first_raw, dtype=float) / 10
    n = len(periods)
    mean = float(np.mean(periods))
    deviations = (periods - mean) ** 2
    ss = float(np.sum(deviations))
    u_mean = math.sqrt(ss / (n * (n - 1)))
    g1 = 4 * math.pi ** 2 * length / mean ** 2
    u_g1 = g1 * math.hypot(u_length / length, 2 * u_mean / mean)
    x, ux, t, ut = (np.asarray(values, dtype=float) for values in (x, ux, t, ut))
    y = t ** 2
    uy = 2 * t * ut
    slope = float(np.linalg.lstsq(x[:, None], y, rcond=None)[0][0])
    sum_xx = float(x @ x)
    residuals = y - slope * x
    rss = float(residuals @ residuals)
    u_slope = math.sqrt(rss / ((len(x) - 1) * sum_xx))
    g2 = 4 * math.pi ** 2 / slope
    u_g2 = g2 * u_slope / slope
    reference = 9.811
    macros = {
        "pL": (length, 3), "puL": (u_length, 3), "pN": (n, 0),
        "pT": (mean, 4), "puT": (u_mean, 6), "pSS": (ss, 8),
        "pg": (g1, 2), "pug": (u_g1, 2), "pUg": (2 * u_g1, 2),
        "pgcalc": (g1, 6), "pugcalc": (u_g1, 6),
        "wA": (slope, 5), "wuA": (u_slope, 5),
        "wg": (g2, 2), "wug": (u_g2, 2), "wUg": (2 * u_g2, 2),
        "pdelta": (abs(g1 - reference), 3), "wdelta": (abs(g2 - reference), 3),
        "preldelta": (100 * abs(g1 - reference) / reference, 2),
        "wreldelta": (100 * abs(g2 - reference) / reference, 2),
        "prelu": (100 * u_g1 / g1, 2), "wrelu": (100 * u_g2 / g2, 2),
        "prelL": (100 * u_length / length, 2), "prelT": (100 * u_mean / mean, 2),
    }
    write("wyniki.tex", "% Generowane przez analiza.py; nie edytować ręcznie.\n" +
          "\n".join("\\newcommand{\\" + name + "}{" + pl(v, digits) + "}"
                    for name, (v, digits) in macros.items()) +
          "\n")
    write("tabela_pierwszy.tex", "".join(
        f"{i} & 10 & {pl(v, 2)} & {pl(p, 3)} & {pl(d, 8)}" + r" \\ \hline" + "\n"
        for i, (v, p, d) in enumerate(zip(first_raw, periods, deviations), 1)))
    write("tabela.tex", "".join(
        " & ".join(pl(v, digits) for v, digits in zip(values, (3, 3, 4, 6, 6, 6))) +
        r" \\ \hline" + "\n" for values in zip(x, ux, t, ut, y, uy)))
    plot(x, ux, y, uy, slope, u_slope, g2, u_g2)
    print(f"Sposób 1: g={g1:.9f}, u(g)={u_g1:.9f}, U(g)={2*u_g1:.9f} m/s^2")
    print(f"Sposób 2: A={slope:.12f}, u(A)={u_slope:.12f} s^2/m")
    print(f"Sposób 2: g={g2:.9f}, u(g)={u_g2:.9f}, U(g)={2*u_g2:.9f} m/s^2")


def plot(x, ux, y, uy, slope, u_slope, g, ug):
    """Wektorowy PDF do sprawozdania; słupki pokazują niepewności standardowe."""
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11,
                         "axes.labelsize": 12, "axes.spines.top": False,
                         "axes.spines.right": False, "pdf.fonttype": 42})
    fig, ax = plt.subplots(figsize=(8, 5.1), layout="constrained")
    blue, orange = "#245b83", "#c76b35"
    ax.errorbar(x, y, xerr=ux, yerr=uy, fmt="o", color=blue,
                markersize=6, ecolor=blue, elinewidth=1.2, capsize=4,
                markeredgecolor="white", markeredgewidth=.6,
                label="Pomiary innych grup; niepewności standardowe", zorder=3)
    xx = np.linspace(float(x.min()), float(x.max()), 200)
    ax.plot(xx, slope * xx, color=orange, linewidth=2,
            label=r"Dopasowanie OLS: $\overline{T}^{\,2}=A L$", zorder=2)
    xx0 = np.array([0, float(x.min())])
    ax.plot(xx0, slope * xx0, color=orange, linewidth=1.5, linestyle="--",
            label="Przedłużenie modelu do początku układu", zorder=2)
    number = lambda v, digits: f"{v:.{digits}f}".replace(".", ",")
    ax.text(.97, .06, "A = " + number(slope, 4) + " s²/m\n"
            + "u(A) = " + number(u_slope, 4) + " s²/m\n"
            + "g = " + number(g, 2) + " m/s²; u(g) = " + number(ug, 2) + " m/s²",
            transform=ax.transAxes, ha="right", va="bottom", fontsize=10,
            bbox={"boxstyle": "square,pad=.55", "facecolor": "white",
                  "edgecolor": "#cbd5df", "linewidth": .8})
    ax.set(xlim=(0, .45), ylim=(0, 1.9),
           xlabel="Długość wahadła L [m]",
           ylabel=r"Kwadrat średniego okresu $\overline{T}^{\,2}$ [s²]")
    ax.xaxis.set_major_locator(MultipleLocator(.05))
    ax.yaxis.set_major_locator(MultipleLocator(.25))
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: number(v, 2)))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: number(v, 2)))
    ax.grid(color="#e3e8ed", linewidth=.7)
    ax.set_axisbelow(True)
    ax.legend(loc="upper left", frameon=True, facecolor="white",
              edgecolor="#cbd5df", fontsize=9, framealpha=1)
    fig.savefig(CHARTS / "wykres.pdf", bbox_inches="tight")
    fig.savefig(CHARTS / "wykres.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
