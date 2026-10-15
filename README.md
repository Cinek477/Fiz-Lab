# Fiz-Lab — laboratorium fizyki

Karty pomiarowe, puste szablony sprawozdań w LaTeX i narzędzia do opracowania wyników.
Każde ćwiczenie ma własny opis i instrukcję uruchomienia.

## Materiały

| Ćwiczenie | Temat | Dokumenty i narzędzia |
|:---:|---|---|
| **0** | Wahadło matematyczne | [Dane i obliczenia](0/README.md) |
| **11** | Moduł Younga | [Opis](11/README.md) · [Karta](11/PDF/11_karta_pomiarowa.pdf) · [Szablon](11/PDF/11_szablon_sprawozdania.pdf) · [Overleaf](11/11_overleaf.zip) |
| **31** | Modelowanie pola elektrycznego | [Osobne warianty A, B i C](31/README.md) |
| **71** | Dyfrakcja i interferencja na dwóch szczelinach | [Opis](71/README.md) · [Karta 1–1200](71/Templatka/PDF/71_karta_pomiarowa_1_1200.pdf) · [Szablon](71/Sprawko/PDF/71_szablon_sprawozdania.pdf) · [Overleaf](71/71_overleaf.zip) |
| **83** | Spektrometr optyczny, widmo rtęci | [Opis](<83/README.md>) · [Karta](<83/PDF/83_karta_pomiarowa.pdf>) · [Szablon](<83/PDF/83_szablon_sprawozdania.pdf>) · [Overleaf](<83/83_overleaf.zip>) |

## Jak korzystać

1. Wybierz ćwiczenie i wydrukuj potrzebne strony karty pomiarowej.
2. Rozpakuj ZIP w Overleaf, ustaw **XeLaTeX** i wybierz plik główny karty lub szablonu.
3. Uzupełnij metrykę, parametry rzeczywistego stanowiska, odczyty i niepewności.
4. Opracuj własne wyniki zgodnie z instrukcją ćwiczenia. Same generatory nie zastępują interpretacji.

Lokalnie źródła kompiluje **Tectonic** lub XeLaTeX. Polecenia w README są podane
względem wskazanego folderu. Skrypty wymagają Python 3.11 lub nowszego;
`uv run` instaluje zależności zadeklarowane w skryptach.

## Foldery

| Folder | Zawartość |
|---|---|
| `PDF/` | Dokumenty do druku; w projektach obliczeniowych także wykresy |
| `Tworzenie/` | Źródła LaTeX, generatory i narzędzia obliczeniowe |
| `Dane/` | Dane CSV, parametry JSON, puste wejścia generatorów |
| `Instrukcja/` | Dostarczone instrukcje ćwiczeń |
| `Wspolne/` | Wspólny styl i rysunki wariantów ćwiczenia 31 |
| `Narzedzia/` | Kontrola plików i odtwarzanie paczek Overleaf |

Ćwiczenie 0 korzysta z `0/wahadlo/`, a 71 z osobnych folderów `Templatka/` i `Sprawko/`.

## Kontrola i paczki

Uruchom z głównego folderu:

```powershell
python Narzedzia/sprawdz.py
python Narzedzia/pakuj_overleaf.py
```

Pierwsze polecenie sprawdza linki README, składnię Pythona, JSON/CSV, zgodność ZIP-ów
ze źródłami i reguły Git. Wymaga programu `git` dostępnego w PATH.
Drugie odtwarza paczki ćwiczeń 11, 31, 71 i 83. [Szczegóły](Narzedzia/README.md).

## Sprawozdania

| Ćwiczenie | Własne sprawozdanie |
|---|---|
| 0 — wahadło | [PDF](0/wahadlo/PDF/sprawozdanie.pdf) |

## Współpraca

Wszystkie ćwiczenia są dostępne na gałęzi `main`, w folderach z numerami.
Zmiany przygotowuj na osobnej gałęzi, np. `poprawki-31`, i zgłaszaj przez pull request.
