# Ćwiczenie 71 — dwie szczeliny

[Wszystkie ćwiczenia](../README.md)

| Materiał | Plik |
|---|---|
| Połączona karta pomiarowa 1–1200 | [PDF](Templatka/PDF/71_karta_pomiarowa_1_1200.pdf) |
| Pusty szablon sprawozdania | [PDF](Sprawko/PDF/71_szablon_sprawozdania.pdf) |
| Karta i szablon do Overleaf | [ZIP](71_overleaf.zip) |
| Tworzenie karty | [Instrukcja](Templatka/README.md) |
| Tworzenie szablonu | [Instrukcja](Sprawko/README.md) |
| Zasady opracowania | [Poradnik](docs/PORADNIK.md) |

Karta ma 1200 kolejnych numerów, bez powtórzeń: 60 stron po 20 odczytów,
parametry stanowiska i miejsce na obliczenia/notatki, łącznie 65 stron.
Drukuj tylko potrzebny zakres. Krok 0,1 mm jest krokiem położenia, nie wartością tła.

Długość fali, odległość szczeliny–detektor, parametry szczelin, opór i skalę sygnału
zapisz ze swojego stanowiska. Wzory i metrykę uzupełniaj zgodnie z pomiarem.
Szablon dotyczy wyłącznie dwóch szczelin.

## Foldery

- `Templatka/`: połączona karta i jej generator.
- `Sprawko/`: szablon, narzędzia i dane; puste wejścia są w `Sprawko/Dane/szablon/`.
- `docs/`: poradnik obliczeń.

Overleaf: **XeLaTeX**; wybierz `71_karta_pomiarowa_1_1200.tex` lub
`71_szablon_sprawozdania.tex`. ZIP odtwarza `Narzedzia/pakuj_overleaf.py`
uruchomiony z głównego folderu zbioru.

Gotowe raporty z ćwiczenia 71 nie są przeznaczone do publikacji. Ich PDF-y,
źródła treści i pliki robocze pozostają lokalne. Foldery przykładów i archiwum
są ignorowane przez Git. Zapisana wcześniejsza seria i jej wykresy również pozostają lokalne.
Publiczne są szablony, ich generatory oraz puste wejścia `Sprawko/Dane/szablon/`.
