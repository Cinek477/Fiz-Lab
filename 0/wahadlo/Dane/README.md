# Dane pomiarowe — ćwiczenie 0

[Obliczenia](../README.md)

Jednostki są zapisane w nazwach kolumn CSV. Kropka w CSV jest
separatorem dziesiętnym; poniższe tabele używają polskiego przecinka.
Niepewności długości i okresów w obliczeniach przyjęto jako standardowe.

## Sposób pierwszy — własna seria

Źródło: `dane_pierwszy.csv`. Każdy czas dotyczy **10 okresów**.
Długość L = 0,245 m oraz u(L) = 0,004 m zapisano w `parametry_pierwszy.json`.

| Nr | Czas 10 okresów [s] |
|---:|---:|
| 1 | 10,00 |
| 2 | 10,03 |
| 3 | 9,97 |
| 4 | 9,94 |
| 5 | 9,94 |
| 6 | 9,85 |
| 7 | 9,78 |
| 8 | 9,92 |
| 9 | 9,78 |
| 10 | 10,31 |

## Sposób drugi — wyniki innych grup

Źródło: `dane.csv`. Każdy zespół mierzył czas 10 okresów;
do analizy przekazano średni okres i jego niepewność.

| L [cm] | u(L) [cm] | T [s] | u(T) [s] |
|---:|---:|---:|---:|
| 24,5 | 0,4 | 0,9952 | 0,0048 |
| 29,8 | 0,3 | 1,0367 | 0,00403 |
| 42,7 | 0,3 | 1,3103 | 0,0040 |
| 18,3 | 0,4 | 0,8584 | 0,0034 |
| 32,8 | 0,2 | 1,1431 | 0,003462 |
| 17,5 | 0,3 | 0,8412 | 0,00160468 |

Do wykresu skrypt przelicza długość na metry, T na T², a niepewność
kwadratu okresu jako u(T²) = 2T·u(T). Nie zaokrągla danych wejściowych.
