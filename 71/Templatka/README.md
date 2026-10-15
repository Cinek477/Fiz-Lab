# Karta pomiarowa — dwie szczeliny

[Ćwiczenie 71](../README.md) · [PDF 1–1200](PDF/71_karta_pomiarowa_1_1200.pdf) · [LaTeX](Tworzenie/71_karta_pomiarowa_1_1200.tex)

Jedna karta obejmuje 1200 odczytów położenia i sygnału. Ma 65 stron:
parametry, 60 tabel po 20 pomiarów i końcowe miejsca na obliczenia/notatki.

Z folderu `71/`:

```powershell
python Templatka/Tworzenie/polacz_karty.py
```

Z `71/Templatka/Tworzenie/`:

```powershell
tectonic 71_karta_pomiarowa_1_1200.tex --outdir ../PDF
```

Generator korzysta z `uklad_karty.tex`. Ten plik jest bazą układu,
nie dokumentem do samodzielnej kompilacji. Edytuj go przed odtworzeniem karty.
