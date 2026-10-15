# Kontrola i paczki Overleaf

[Wszystkie ćwiczenia](../README.md)

Skrypty działają z Pythonem 3.11 lub nowszym, bez dodatkowych bibliotek Pythona.
Kontrola `.gitignore` wymaga programu Git. Polecenia uruchamiaj z głównego folderu zbioru.

```powershell
python Narzedzia/pakuj_overleaf.py
python Narzedzia/sprawdz.py
```

Pakowanie odtwarza sześć publicznych ZIP-ów: ćwiczenia 11, 71, 83 oraz warianty A/B/C ćwiczenia 31.
Paczki zawierają źródła pustych dokumentów i potrzebne rysunki.
Pakowanie nie odtwarza źródeł ani PDF-ów; najpierw uruchom odpowiednie generatory i kompilację.

Kontrola sprawdza:

- lokalne linki wszystkich README oraz ich dostępność po zastosowaniu `.gitignore`;
- składnię skryptów, strukturę JSON i zgodność liczby kolumn CSV;
- dopuszczenie dokładnie wskazanych własnych sprawozdań PDF z ćwiczenia 0;
- integralność ZIP-ów i zgodność ich zawartości z aktualnymi źródłami.

Dodatkowo możesz skompilować wszystkie 12 dokumentów z ZIP-ów:

```powershell
python Narzedzia/sprawdz.py --compile tectonic
```

Jeżeli Tectonic nie jest w PATH, zamiast `tectonic` podaj pełną ścieżkę do programu w cudzysłowie.
Git i kompilacja działają w katalogach tymczasowych; kontrola nie zmienia źródeł ani indeksu Git.
Nie zastępuje oceny poprawności fizycznej pomiarów lub ręcznego przeglądu wyglądu stron.
