# Szablon sprawozdania — dwie szczeliny

[Ćwiczenie 71](../README.md) · [PDF](PDF/71_szablon_sprawozdania.pdf) · [LaTeX](Tworzenie/71_szablon_sprawozdania.tex) · [Opis danych](Dane/README.md)

Szablon zawiera cel, teorię, aparaturę, tabele pomiarów i par maksimów,
miejsce na wykres, ocenę jakości obrazu, niepewności i wnioski.
Metryka i wyniki są puste. Źródło LaTeX jest samodzielne.

## Kompilacja

Z `71/Sprawko/Tworzenie/`:

```powershell
tectonic 71_szablon_sprawozdania.tex --outdir ../PDF
```

W Overleaf użyj paczki z README ćwiczenia i kompilatora **XeLaTeX**.

## Odtworzenie z generatora

Z folderu `71/`:

```powershell
uv run Sprawko/Tworzenie/generuj.py --template --output-dir Sprawko/Tworzenie
```

Generator czyta puste `Dane/szablon/` i zapisuje LaTeX oraz pomocniczy DOCX.
Nadpisuje źródło szablonu, więc własne zmiany zachowaj przed uruchomieniem.
Pliki robocze generatora i wyniki obliczeń nie są wymagane do kompilacji pustego szablonu.

