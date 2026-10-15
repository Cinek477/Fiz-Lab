# Ćwiczenie 31 — modelowanie pola elektrycznego

[Wszystkie ćwiczenia](../README.md)

Wariant wybiera prowadzący. Każdy ma osobną kartę, szablon i paczkę Overleaf.

| Folder | Zakres |
|---|---|
| [1. Kondensator płaski — A](<1. Kondensator płaski/README.md>) | Trzy profile potencjału i 50 miejsc na punkty mapy poza elektrodami |
| [2. Kondensator cylindryczny — B](<2. Kondensator cylindryczny/README.md>) | Pomiary wzdłuż trzech promieni |
| [3. Dowolne elektrody — C](<3. Dowolne elektrody/README.md>) | 100 miejsc na punkty mapy 2D |

[Teoria](Instrukcja/31_opis.pdf) · [Wykonanie i wymagania](Instrukcja/31_wykon.pdf)

## Co zapisać

Napięcia i biegunowość elektrod, ich geometrię, położenie początku oraz zwroty osi,
rzeczywisty krok siatki i dokładności miernika. W B zapisz również kierunki promieni.
Siatka na końcu karty służy do szkicu; nie jest kalibracją odległości na stanowisku.

Pole wyznaczaj z **E = −grad V**. Rozróżniaj składową ze znakiem i dodatni moduł.
Przeliczaj mm na m, aby otrzymać V/m. Brak pomiaru nie oznacza 0 V.
Mapy pomiarowe opieraj na odczytach; schematy idealne podpisuj jako teoretyczne.

## Źródła i kompilacja

Z `31/`: `python Tworzenie/generuj.py` odtwarza źródła trzech wariantów i ZIP-y.
Własne zmiany generowanych plików zachowaj przed ponownym uruchomieniem.
Generator nie nadpisuje README.

Kompiluj z `Tworzenie/` wybranego wariantu, np.:

```powershell
tectonic 31_A_karta.tex --outdir ../PDF
tectonic 31_A_szablon.tex --outdir ../PDF
```

Wspólny styl i rysunki są w `Wspolne/`. ZIP-y zawierają ich kopie z dopasowanymi
ścieżkami. W Overleaf wybierz **XeLaTeX** i plik główny karty albo szablonu.
Daty są puste. Folder `Przykład/` jest wykluczony z Git.
