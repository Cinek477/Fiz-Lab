# Ćwiczenie 11 — moduł Younga

[Arkusz Excel](Excel/11_pomiary.xlsx) · [Wpisywanie danych i tworzenie raportu](Excel/README.md)
[Wszystkie ćwiczenia](../README.md)

| Materiał | Plik |
|---|---|
| Karta pomiarowa | [PDF](PDF/11_karta_pomiarowa.pdf) |
| Pusty szablon sprawozdania | [PDF](PDF/11_szablon_sprawozdania.pdf) |
| Źródła do Overleaf | [ZIP](11_overleaf.zip) |
| Teoria | [Instrukcja](Instrukcja/11_opis.pdf) |
| Wykonanie i wymagania | [Instrukcja](Instrukcja/11_wykon.pdf) |

Karta obejmuje dwa druty: długości, po trzy odczyty średnicy, dane przyrządów
i po 21 wierszy obciążania/odciążania. Instrukcja ogranicza obciążenie stali
do 10 kg, mosiądzu i miedzi do 6 kg. Rodzaje próbek potwierdź na stanowisku.
Daty w szablonach są puste, a metrykę dostosuj do swojego zespołu.

## Opracowanie

- Używaj sumarycznej masy obciążenia: F = mg.
- Dla wskazań przyrostowych dźwigni: Δl = (z↑ + z↓)/4.
- Średnicę uśrednij z trzech miejsc; niepewność typu B określ zgodnie z instrukcją.
- Dopasuj Δl = aF + b i oblicz E = 4l/(πd²a), w jednostkach SI.
- Uzasadnij zakres regresji i pokaż odrzucone punkty.
- Wkład względnej niepewności średnicy do u(E) zawiera czynnik 2.

## Odtworzenie

Z folderu `11/` odtwórz puste tabele:

```powershell
python Tworzenie/generuj.py
```

Następnie z `11/Tworzenie/`:

```powershell
tectonic 11_karta_pomiarowa.tex --outdir ../PDF
tectonic 11_szablon_sprawozdania.tex --outdir ../PDF
```

Overleaf: **XeLaTeX**, plik główny `11_karta_pomiarowa.tex` albo `11_szablon_sprawozdania.tex`.
Rysunek przyrządu znajduje się w `Tworzenie/Rysunki/` i w ZIP-ie.
Karta ma 3 strony, szablon 6. Paczkę odtworzysz z głównego folderu
przez `python Narzedzia/pakuj_overleaf.py`.

