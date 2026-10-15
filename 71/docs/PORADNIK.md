# Opracowanie pomiarów dwóch szczelin

## Od surowych odczytów do wykresu

Zapisuj położenie detektora `p` w mm i napięcie `U` w mV, zachowując
stały opór oraz skalę miernika w całej serii. Napięcie jest proporcjonalne
do natężenia światła. Początek serii jest położeniem na skali, a nie
automatycznie środkiem obrazu interferencyjnego.

Położenie względem centrum: `x = p − p₀`. Przy stałym kroku można użyć
umownej skali `pᵢ = (i − 1) × 0,1 mm`; przesunięcie początku nie zmienia odległości między prążkami.
Nie zastępuj pustych wierszy zerami. Zapisuj zmiany ustawień i przyrządów.

Wykres liniowy `U(p)` pomaga ustalić maksima i minima. Odcinki łączące
odczyty są pomocnicze i nie zastępują dopasowania modelu. Tło można
odejmować dopiero po jego wiarygodnym ustaleniu.

## Odległość między szczelinami

Dla małych kątów parę maksimów rzędu `−m, +m` opisują zależności:

```text
rₘ = (p_prawe,m − p_lewe,m) / 2
dₘ = m λ L / rₘ
```

`L` oznacza odległość płytka ze szczelinami–detektor, `λ` długość fali,
a `d` odległość między środkami szczelin. Przed podstawieniem użyj
jednakowych jednostek długości. Rozstaw sąsiednich prążków jest
w przybliżeniu równy `λL/d`.

Nie utożsamiaj odległości stół–laser z `L` bez sprawdzenia geometrii
stanowiska. Największy zapisany odczyt nie musi dowodzić, że objęto
całe maksimum centralne i obie strony obrazu.

## Niepewności

Przy niezależnych odczytach położenia:

```text
u(rₘ) = ½ √[u²(p_lewe,m) + u²(p_prawe,m)]
u(dₘ)/dₘ = √[(u(λ)/λ)² + (u(L)/L)² + (u(rₘ)/rₘ)²]
```

Rozdzielczość `q` przy modelu zaokrąglania daje `q/√12`, a graniczny
błąd jednostajny `±Δ` daje `Δ/√3`. Specyfikacja przyrządu może wymagać
innego modelu. Sama działka skali nie zawsze opisuje pełną niepewność.

Przy uśrednianiu wyników uwzględnij wspólne `λ` i `L`: ich wkład
nie maleje automatycznie wraz z liczbą prążków. Niepewność typu A
nie zastępuje wszystkich składowych typu B.

## Co sprawdzić przed oddaniem?

- sprawdzić ręczną transkrypcję ze skanem;
- potwierdzić odległość szczeliny–detektor i długość fali;
- zapisać dokładność miernika, rozdzielczość skali i opór;
- zidentyfikować środek obrazu oraz rzędy maksimów;
- ustalić końcowe niepewności i zaokrąglenia.

Aktualne dokumenty, zakresy numeracji i polecenia znajdziesz w [README](../README.md).
