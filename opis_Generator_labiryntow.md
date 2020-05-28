## Saper
### Opis zadania
*  Główne okno programu zawiera kontrolki pozwalające na wybór wielkości labiryntu
(liczba pól N na M; para liczb całkowitych nie większych niż 30), wizualizację labiryntu
(na przykład jako siatka kolorowych przycisków) oraz przycisk “generuj”.
* Labirynt składa się z pól będących korytarzem lub ścianą.
Użytkownik wybiera dwa różne pola będące wejściem i wyjściem. Pola te
traktowane będą jak korytarz. Po naciśnięciu przycisku “generuj” następuje
generowanie losowego labiryntu.
* Dla każdej pary pól będących korytarzem powinna istnieć ścieżka je łącząca
(brak pól odłączonych od reszty labiryntu). Przechodzenie możliwe jest tylko na
pola będące korytarzem które sąsiadują krawędzią z danym polem.
* Wygenerowany labirynt powinien posiadać ścieżkę od wejścia do wyjścia, która
nie będzie linią prostą (poziomą lub pionową) i która powinna być zaznaczona na
wizualizacji.
* Przechowywana jest lista punktów pośrednich ścieżki prowadzącej od wejścia do
wyjścia.
* Po wybraniu dowolnego pola będącego korytarzem, dodawane jest ono na
koniec listy punktów pośrednich. Następnie powinna zostać znaleziona i
zaznaczona najkrótsza ścieżka prowadząca z wejścia do wyjścia przez wszystkie
punkty pośrednie.
* Wybranie pola będącego punktem pośrednim powoduje usunięcie danego punktu
pośredniego.
* Labirynt nie może posiadać żadnego „pokoju‟: obszar 2 na 2 pola korytarza (lub
większy).
* Labirynt nie może posiadać żadnych obszarów 3 na 3 pola ściany (lub większych).

### Testy
1. Wygenerowanie labiryntu o wymiarach 10 na 12 pól z wejściem i wyjściem
na przeciwnych krawędziach.
2. Wygenerowanie labiryntu o wymiarach 20 na 10 pól z wejściem i wyjściem
cztery pola od przeciwnych, krótszych krawędzi.
3. Próba wygenerowania labiryntu o wymiarach 10 na 10 z wejściem i wyjściem
w jednym polu - oczekiwana informacja o błędzie.
4. Próba wygenerowania labiryntu o wymiarach 10 na 10 z wejściem i wyjściem koło
siebie - oczekiwana informacja o błędzie, ścieżka jest linią prostą.
5. Próba wygenerowania labiryntu o wymiarach 10 na 10 z wejściem i wyjściem
między którymi jest 1, 2 lub 3 pola odstępu - oczekiwany labirynt bez ścieżki będącej
linią prostą.
6. Próba wygenerowania labiryntu którego przynajmniej jeden z wymiarów wynosi 0
lub jest liczbą ujemną - oczekiwana informacja o błędzie.
7. Próba wygenerowania za dużego labiryntu - oczekiwana informacja o błędzie.
8. Wygenerowanie labiryntu o wymiarach 13 na 17, wejście i wyjście w dowolnych
miejscach, wyszukanie ścieżki przez punkt pośredni wskazany przez prowadzącego.
Wygenerowanie labiryntu o wymiarach 13 na 17, dodanie dwóch punktów pośrednich
wskazanych przez prowadzącego, usunięcie pierwszego, dodanie kolejnego. Oczekiwane
znalezienie właściwej ścieżki.
9. Próba wyszukania ścieżki przez pole będące ścianą - oczekiwane niepowodzenie
przy próbie dodania punktu pośredniego

#### [Link do repozytorium](https://github.com/Void-Caller/Generator_labiryntow)