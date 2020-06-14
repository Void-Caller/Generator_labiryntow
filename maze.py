import random
import time

random.seed(time.time())


class MazeVirt:
    """Wirtualna klasa labiryntu."""
    def generate(self):
        raise NotImplementedError()


class Maze(MazeVirt):
    """Klasa generująca labirynt.

    Zmienne klasy:
    x_max - wymiar x, krotka 2-elementowa, oba elementy to int.
    y_max - wymiar y, krotka 2-elementowa, oba elementy to int.
    cells - 2D array zapisujący ściany i korytarze,
    odpowiednio jako True i False.
    entry - współrzędne wejścia, krotka 2-elementowa, oba elementy to int.
    exit - współrzędne wyjścia, krotka 2-elementowa, oba elementy to int.
    intermid - tablica punktów pośrednich, krotek (int, int).

    Metody klasy:
    __init__(self, coord, entry, exit) - inicjalizuje labirynt.

    generate(self) - generuje labirynt na podstawie zmiennych klasy.
    Korzysta z losowego algorytmu opartego na deep-first search.

    neighbour_check(self, x, y) - wyszukuje możliwe ruchy
    dla algorytmu generującego. Zwraca tablicę krotek współrzędnych,
    odpowiadających dozwolonym krokom.

    exit_check(self) - sprawdza, czy wyjście jest częścią labiryntu.
    Jeśli nie, zwraca True. Jeśli tak, zwraca False.
    """
    def __init__(self, coord, entry, exit):
        """Inicjalizuje pusty labirynt.

        cood - wymiary
        entry - wejście
        exit - wyjście
        """
        self.x_max, self.y_max = coord
        # Tworzę wypełniony murami labirynt.
        self.cells = [
            [True for i in range(self.x_max)]
            for j in range(self.y_max)]
        self.entry = entry[:]
        self.exit = exit[:]

    def generate(self):
        """Funkcja generuje losowy labirynt w oparciu o metodę depth-first search.

        Nie zwraca wartości. Jej operacje zachodzą na zmiennych klasy.
        """

        # Tworzę stos odwiedzonych do backtrackingu
        # Pierwszym elementem jest punkt wejścia
        stack = [(self.entry[1], self.entry[0])]

        # Ustawiam korytarz na wejściu.
        self.cells[self.entry[1]][self.entry[0]] = False

        # Ustawiam korytaż na wyjściu.
        self.cells[self.exit[1]][self.exit[0]] = False
        # Gwarantuje, że wyjście jest częścią labiryntu.

        # Zapisuje obecne współrzędne.
        x, y = self.entry

        # Pętla generująca labirynt
        while stack:

            # Szukam sąsiadów, do których mogę wkroczyć
            neighs = self.neighbour_check(x, y)
            # Jeśli są sąsiedzi
            if neighs:
                # Wybieram sąsiada.
                neigh = random.choice(neighs)
                # Ustawiam korytarz na współżędnych sąsiada.
                self.cells[neigh[1]][neigh[0]] = False
                # Ustawiam korytarz między mną a sąsiadem.
                tmp_x = x + ((neigh[0] - x) // 2)
                tmp_y = y + ((neigh[1] - y) // 2)
                self.cells[tmp_y][tmp_x] = False
                # Przechodzę do wybranego sąsiada.
                x, y = neigh
                # Dodaję sąsiada do stack w celu backtrackingu.
                stack.append(neigh)
            else:
                # Jeśli nie ma sąsiada, to cofam się o do poprzedniego.
                # Gdy nie będę miał się do kogo cofać, to kończę pętle.
                x, y = stack.pop()

        # Jeśli wyjście nie jest częścią labiryntu
        if self.exit_check():
            # Jeśli wyjście jest na krawędzi górnej lub dolnej
            if not self.exit[1] or self.exit[1] == self.y_max - 1:
                # Otwórz korytarz w zachód, jeśli można.
                # Sprawdzam, czy na zachodzie pojawia się wejście.
                if (self.exit[0] - 1 >= 0 and
                        self.exit[0] - 2 is not self.entry[0]):
                    self.cells[self.exit[1]][self.exit[0] - 1] = False
                # Powtórnie sprawdzam wejście
                elif (self.exit[0] + 1 < self.x_max and
                        self.exit[0] + 2 is not self.entry[0]):
                    self.cells[self.exit[1]][self.exit[0] + 1] = False
                # Jeśli nie mogę iść na boki, to idę do środka.
                # jeśli jestem na górze
                elif self.exit[1]:
                    self.cells[self.exit[1] - 1][self.exit[0]] = False
                # jeśli jestem na dole
                else:
                    self.cells[self.exit[1] + 1][self.exit[0]] = False
            # Jeśli wyjście jest na krawędzi wschodniej lub zachodniej
            elif not self.exit[0] or self.exit[0] == self.x_max - 1:
                # Otwórz korytarz w południe, jeśli można.
                # Sprawdzam, czy na południu pojawia się wejście.
                if (self.exit[1] - 1 >= 0 and
                        self.exit[1] - 2 is not self.entry[1]):
                    self.cells[self.exit[1] - 1][self.exit[0]] = False
                # Powtórnie sprawdzam wejście
                elif (self.exit[1] + 1 < self.y_max and
                        self.exit[1] + 2 is not self.entry[1]):
                    self.cells[self.exit[1] + 1][self.exit[0]] = False
                # Jeśli nie mogę iść na boki, to idę do środka.
                # jeśli jestem na zachodzie.
                elif self.exit[0]:
                    self.cells[self.exit[1]][self.exit[0] - 1] = False
                # jeśli jestem na wschodzie.
                else:
                    self.cells[self.exit[1]][self.exit[0] + 1] = False

    def neighbour_check(self, x, y):
        """Wyszukuje i zwraca listę pól, do których generate może wkroczyć.

         Współżędne zapisywane są w krotkach.
         Jeśli nie ma dobrych sąsiadów, to zwraca pustą listę.
         Funkcja wykrywa granice labiryntu na podstawie zmiennych klasy.
         Jeśli zadane pole jest wejściem, przeprowadze procedurę,
         która zapobiega prostej ścieżce do wyjścia"""

        neighbours = []

        # Sprawdzam, czy jest to wejście.
        is_entry = (x == self.entry[0] and y == self.entry[1])

        # Sprawdzam zachodniego sąsiada.
        if x - 2 >= 0:
            if self.cells[y][x - 2]:
                # Jeśli jest to wejście, to sąsiad nie może dzielić
                # współrzędnych z wyjściem.
                if is_entry:
                    if not(x - 2 == self.exit[0] or y == self.exit[1]):
                        neighbours.append((x - 2, y))
                # Jeśli nie jesteśmy na wejściu,
                # to po prostu dodajemy sąsiada.
                else:
                    neighbours.append((x - 2, y))
        # Sprawdzam wschodniego sąsiada.
        if x + 2 < self.x_max:
            if self.cells[y][x + 2]:
                # Analogicznie jak dla wschodniego sąsiada.
                if is_entry:
                    if not(x + 2 == self.exit[0] or y == self.exit[1]):
                        neighbours.append((x + 2, y))
                else:
                    neighbours.append((x + 2, y))
        # Sprawdzam północnego sąsiada.
        if y + 2 < self.y_max:
            if self.cells[y + 2][x]:
                # Analogicznie jak dla wschodniego sąsiada.
                if is_entry:
                    if not(x == self.exit[0] or y + 2 == self.exit[1]):
                        neighbours.append((x, y + 2))
                else:
                    neighbours.append((x, y + 2))
        # Sprawdzam południowego sąsiada.
        if y - 2 >= 0:
            if self.cells[y - 2][x]:
                # Analogicznie jak dla wschodniego sąsiada.
                if is_entry:
                    if not (x == self.exit[0] or y - 2 == self.exit[1]):
                        neighbours.append((x, y - 2))
                else:
                    neighbours.append((x, y - 2))

        # Zwracam tablicę.
        return neighbours

    def exit_check(self):
        """Sprawdza, czy wyjście jest częścią labiryntu.

        Jeśli nie, zwraca True."""

        # Sprawdzam zachodniego sąsiada.
        x = self.exit[0]
        y = self.exit[1]

        # Sprawdzam zachodniego sąsiada.
        if x - 1 >= 0:
            if not self.cells[y][x - 1]:
                return False
        # Sprawdzam wschodniego sąsiada.
        if x + 1 < self.x_max:
            if not self.cells[y][x + 1]:
                return False
        # Sprawdzam północnego sąsiada.
        if y + 1 < self.y_max:
            if not self.cells[y + 1][x]:
                return False
        # Sprawdzam południowego sąsiada.
        if y - 1 >= 0:
            if not self.cells[y - 1][x]:
                return False
        return True


if __name__ == '__main__':
    maze = Maze((10, 10), (0, 0), (9, 9))
    maze.generate()
    for i in reversed(range(10)):
        for j in range(10):
            print("#", end=" ") if maze.cells[i][j] else print("+", end=" ")
        print()

    print(maze.deep_search((0, 0), (9, 9)))
