# Pomiary w Excelu — wersja 1.1

[Fiz-Lab](../README.md)

Otwórz kartę w Microsoft Excel lub LibreOffice Calc i zapisuj dane tak jak na papierowej karcie.
Żółte pola służą do wpisywania danych. Szare pola zawierają numerację, a niebieska kolumna
położenia w 71 wylicza się z początku i kroku serii. Puste komórki oznaczają brak pomiaru;
rzeczywiste zero wpisz jako `0`.

| Ćwiczenie | Arkusz | Zawartość |
|---|---|---|
| 0 | [Wahadło](../0/Excel/0_pomiary.xlsx) | 100 powtórzeń czasu i 100 zestawów L,T innych grup |
| 11 | [Moduł Younga](../11/Excel/11_pomiary.xlsx) | Dwa druty, wymiary i po 21 punktów obciążania/odciążania |
| 31 A | [Kondensator płaski](<../31/1. Kondensator płaski/Excel/31A_pomiary.xlsx>) | 20 pozycji trzech profili i 50 punktów mapy |
| 31 B | [Kondensator cylindryczny](<../31/2. Kondensator cylindryczny/Excel/31B_pomiary.xlsx>) | 20 pozycji trzech promieni |
| 31 C | [Dowolne elektrody](<../31/3. Dowolne elektrody/Excel/31C_pomiary.xlsx>) | 100 punktów mapy |
| 71 | [Dwie szczeliny](../71/Excel/71_pomiary.xlsx) | 1200 odczytów i 20 par maksimów |
| 83 | [Spektrometr](../83/Excel/83_pomiary.xlsx) | 8 linii × 3 powtórzenia × 2 rzędy, osobne stopnie i minuty |

Każde ćwiczenie ma własny folder **Excel/** z arkuszem, krótką instrukcją
i plikiem **utworz_sprawozdanie.cmd**. W ćwiczeniu 31 folder Excel znajduje się
wewnątrz wybranego wariantu A/B/C.

## Od pomiarów do sprawozdania

1. Zapisz kopię wybranego arkusza, np. `Moje_pomiary/11.xlsx`.
2. W zakładce **Ustawienia** wpisz metrykę, parametry, przyrządy oraz opis przebiegu.
3. Uzupełnij tabele pomiarowe, zachowując jednostki z nagłówków. Zapisz i zamknij plik.
4. Uruchom generator, a po obejrzeniu wyników dopisz w arkuszu wnioski i uruchom go ponownie.

Z głównego folderu repozytorium:

```powershell
uv run Narzedzia/excel_sprawozdanie.py Moje_pomiary/11.xlsx
```

Na Windows możesz przeciągnąć XLSX na **utworz_sprawozdanie.cmd** obok arkusza
lub na [wspólny plik uruchamiający](../Narzedzia/utworz_sprawozdanie.cmd).
Wymagany jest `uv` albo Python 3.11+ z bibliotekami z
`Narzedzia/requirements_excel.txt`. Przy użyciu `uv run` biblioteki instalują się automatycznie.

Obok kopii arkusza powstaje folder `Wyniki/<ćwiczenie>/`:

- `sprawozdanie.tex` — sformatowany raport z metryką, wzorami w ramkach, tabelami i wnioskami;
- wykresy PDF, `obliczenia.json` i CSV z odczytanymi danymi;
- `sprawozdanie_overleaf.zip` — komplet źródeł i wykresów do Overleaf (**XeLaTeX**);
- `sprawozdanie.pdf` — jeśli dostępny jest program **Tectonic**.

Tectonic powinien być dostępny w PATH. Możesz też wskazać go parametrem:

```powershell
uv run Narzedzia/excel_sprawozdanie.py Moje_pomiary/11.xlsx --tectonic "C:/narzedzia/tectonic.exe"
```

Zmienna środowiskowa `FIZLAB_TECTONIC` może zawierać tę samą ścieżkę dla przeciągania pliku na CMD.
Bez Tectonica generator zapisuje źródła i ZIP do Overleaf. Opcja `--tex-only` pomija kompilację.
Własny katalog wynikowy wskaż przez `--output-dir`.

## Ważne przy wpisywaniu

- **Wszystkie karty:** nie zmieniaj nazw zakładek, nagłówków w wierszu 6 ani układu parametrów.
  Wpisuj liczby bez jednostek; Excel może wyświetlać przecinek dziesiętny.
  Nie zastępuj braków zerami. Niepewności `u(...)` są standardowe — przelicz działkę lub błąd
  graniczny zgodnie z modelem przyrządu przed wpisaniem ich do arkusza.
- **0:** czas dotyczy liczby okresów `n`. W drugiej tabeli wpisuj już okres jednego drgania.
  Regresja T²(L) jest OLS przez początek; podana składowa niepewności dopasowania nie obejmuje
  pełnego modelu błędów L i T.
- **11:** wpisz oba rzeczywiste zera czujnika i masę sumaryczną. Kolumna `Regresja` przyjmuje
  `tak`/`nie`; pusta oznacza `tak`. Wyłączone punkty pozostają na wykresie.
  Przełożenie dźwigni jest uwzględnione raz. Potrzeba co najmniej trzech wybranych punktów.
- **31:** wewnętrzna elektroda B ma V0+U, zewnętrzna V0. Podaj zgodne zwroty osi.
  Kontury map powstają tylko przy znanym dodatnim kroku h,k i lokalnym pokryciu danymi.
  Wektory są liczone wyłącznie ze zmierzonych sąsiadów; długości strzałek są skalowane.
- **71:** początek `0 mm` jest umowny, a domyślny krok `0,1 mm` możesz zmienić.
  Automatyczne położenia można nadpisać liczbowymi odczytami. Wpisz pary i rzędy maksimów,
  aby wyznaczyć rozstaw szczelin; program nie zgaduje rzędów i nie dopasowuje wyniku nominalnego.
  Przy samych napięciach otrzymasz wykres oraz raport z informacją, czego brakuje do obliczeń d.
- **83:** wpisuj surowe wskazania skali i kierunek zerowy dla każdego rzędu.
  Stopnie i minuty są osobnymi polami (0 ≤ minuty < 60); 14°20′ nie oznacza 14,20°.
  Generator uwzględnia przejście skali przez 360° i wspólne zero. Wpisane odniesienia
  służą porównaniu, a nie zastępują pomiarów.

Arkusze nie zawierają makr. Obliczenia raportu wykonuje Python na zapisanych wartościach,
więc nie zależą od pamięci podręcznej formuł Excela. Jedyny obsługiwany wzór wejściowy to
automatyczna kolumna położenia w 71. Opis przebiegu i wnioski pochodzą z Twoich wpisów.
