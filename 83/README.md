# Ćwiczenie 83 — spektrometr optyczny

[Arkusz Excel](Excel/83_pomiary.xlsx) · [Wpisywanie danych i tworzenie raportu](Excel/README.md)
[Wszystkie ćwiczenia](../README.md)

| Materiał | Plik |
|---|---|
| Karta pomiarowa | [PDF](PDF/83_karta_pomiarowa.pdf) |
| Pusty szablon sprawozdania | [PDF](PDF/83_szablon_sprawozdania.pdf) |
| Instrukcja | [PDF](Instrukcja/83.pdf) |
| Źródła do Overleaf | [ZIP](83_overleaf.zip) |
| Własne sprawozdanie — 20.10.2026 | [PDF](Sprawozdanie/PDF/83_sprawozdanie.pdf) |

## Własne sprawozdanie

[Sprawozdanie](Sprawozdanie/README.md) zawiera opracowanie pomiarów
Marcina Podymy i Pawła Mierzwy dla siatki 570 rys/mm.

## Puste materiały

Ćwiczenie dotyczy widma rtęci. Materiały o dwóch szczelinach znajdują się w ćwiczeniu 71.

Karta obejmuje 8 linii, po 3 powtórzenia, obie strony i I/II rząd.
Zapisuj surowe wskazania skali w stopniach i minutach, kierunek zerowy
i parametry siatki. Dwie żółte linie mają oddzielne ID.

Szablon zawiera teorię, opracowanie obu stron i rzędów, obliczenia długości fal,
identyfikację przejść, szacowanie błędu oraz wnioski w tabeli.
Wyniki i daty są puste; metrykę dostosuj do zespołu.

## Odtworzenie

Z folderu ćwiczenia: `python Tworzenie/generuj.py` odtwarza puste tabele.
Następnie z `Tworzenie/`:

```powershell
tectonic 83_karta_pomiarowa.tex --outdir ../PDF
tectonic 83_szablon_sprawozdania.tex --outdir ../PDF
```

Overleaf: **XeLaTeX**, plik główny `83_karta_pomiarowa.tex` lub
`83_szablon_sprawozdania.tex`. ZIP odtwarza `Narzedzia/pakuj_overleaf.py`
z głównego folderu zbioru.

Nie myl stopni dziesiętnych z zapisem stopnie–minuty: 14,20° to 14°12′.
Stałą siatki odczytaj na stanowisku, nie z przykładowych danych.
