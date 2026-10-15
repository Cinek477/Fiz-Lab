# Wahadło — obliczenia

[Ćwiczenie 0](../README.md) · [Dane i jednostki](Dane/README.md) · [Skrypt](Tworzenie/analiza.py)

Skrypt wyznacza g z własnej serii oraz z nachylenia zależności T²(L) dla wyników
innych grup. Przygotowuje wykres z niepewnościami i tabele LaTeX.
Dopasowanie T² = A·L przechodzi przez początek układu, a g = 4π²/A.

## Uruchomienie

Z folderu `0/wahadlo/`:

```powershell
uv run --with numpy --with matplotlib python Tworzenie/analiza.py
```

Alternatywnie zainstaluj `Tworzenie/requirements.txt` i uruchom skrypt zwykłym Pythonem.
Dane wejściowe są w `Dane/`, wykresy w `PDF/Wykresy/`, a generowane tabele w `Tworzenie/`.
Uruchomienie nadpisuje wyniki obliczeń, zachowując pliki pomiarowe.

Na wykresie współczynnik kierunkowy ma jednostkę s²/m. Kąt widocznej prostej
zależy od skal osi i proporcji rysunku; nie jest niezależną wielkością fizyczną.
[Gotowe sprawozdanie PDF](PDF/sprawozdanie.pdf) na własnych danych jest publiczne.
Zestaw nie zawiera pustego szablonu.
