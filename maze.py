import random
import time

random.seed(time.time())

class Too_large_exception(Exception):
    pass

class Too_small_exception(Exception):
    pass

class Maze:
    '''Klasa generująca labirynt.
    Zawiera funkcjonalność przeszukiwania labiryntu'''
    def __init__(self,x,y,entry,exit):
        try:
            if x<3 or y<3:
                raise Too_small_exception
            elif x>30 or y>30:
                raise  Too_large_exception
        except Too_small_exception:
            print("Too small!, maze needs to be at least 3 by 3.")
        except Too_large_exception:
            print("Too large!, maze needs to be at most 30 by 30.")
        self.x_max = x
        self.y_max = y
        self.cells = [[True for i in range(x)] for j in range(y)]
        self.entry = entry.copy()
        self.exit = exit.copy()
        self.generate()

    def generate(self):
        '''
        Funkcja generuje losowy labirynt w oparciu o metodę depth-first search.
        Nie zwraca wartości. Jej operacje zachodzą na zmiennych klasy.
        '''
        #Tworzę stos odwiedzonych do backtrackingu
        #Pierwszym elementem jest punkt wejścia
        stack = [(self.entry[1], self.entry[0])]

        #Ustawiam korytarz na wejściu.
        self.cells[self.entry[1]][self.entry[0]] = False

        #Ustawiam korytaż na wyjściu.
        self.cells[self.exit[1]][self.exit[0]] = False
        #Gwarantuje, że wyjście jest częścią labiryntu.

        #Zapisuje obecne współrzędne.
        x = self.entry[0]
        y = self.entry[1]

        #Pętla generująca labirynt

        while stack:

            #Szukam sąsiadów, do których mogę wkroczyć
            neighs = self.neighbour_check(x, y)
            #Jeśli są sąsiedzi
            if neighs:
                #Wybieram sąsiada.
                neigh = random.choice(neighs)
                #Ustawiam korytarz na współżędnych sąsiada.
                self.cells[neigh[1]][neigh[0]] = False
                #Ustawiam korytarz między mną a sąsiadem.
                self.cells[y + ((neigh[1] - y) // 2)][x + ((neigh[0] - x) // 2)] = False
                x, y = neigh

                stack.append((x, y))
            else:
                x, y = stack.pop()

        #Jeśli wyjście nie jest częścią labiryntu
        if self.exit_check():
            #Jeśli wyjście jest na krawędzi górnej lub dolnej
            if not self.exit[1] or self.exit[1] == self.y_max - 1:
                #Otwórz korytarz w lewo, jeśli można
                if self.exit[0] - 1 >= 0:
                    self.cells[self.exit[1]][self.exit[0] - 1] = False
                #Lewa i prawa strona nie mogą byś równocześnie poza zasięgiem.
                else:
                    self.cells[self.exit[1]][self.exit[0] - 1] = False
            #Jeśli wyjście jest na krawędzi wschodniej lub zachodniej
            elif not self.exit[0] or self.exit[0] == self.x_max - 1:
                #Otwórz korytarz w na południe, jeśli można
                if self.exit[1] - 1 >= 0:
                    self.cells[self.exit[1] - 1][self.exit[0]] = False
                #Południe i pólnoc strona nie mogą byś równocześnie poza zasięgiem.
                else:
                    self.cells[self.exit[1] + 1][self.exit[0]] = False

    def neighbour_check(self,x,y):
        '''Wyszukuje i zwraca listę pól,
         do których funkcja generująca może wkroczyć.
         Współżędne zapisywane są w krotkach
         Jeśli nie ma dobrych sąsiadów, to zwraca pustą listę.
         Funkcja wykrywa granice labiryntu na podstawie zmiennych klasy'''
        neighbours = []

        #sprawdzam zachodniego sąsiada
        if x - 2 >= 0:
            if self.cells[y][x - 2]:
                neighbours.append((x - 2, y))
        #sprawdzam wschodniego sąsiada
        if x + 2 < self.x_max:
            if self.cells[y][x + 2]:
                neighbours.append((x + 2, y))
        #sprawdzam północnego sąsiada
        if y + 2 < self.y_max:
            if self.cells[y + 2][x]:
                neighbours.append((x, y + 2))
        #sprawdzam południowego sąsiada
        if y - 2 >= 0:
            if self.cells[y - 2][x]:
                neighbours.append((x, y - 2))

        #zwracam tablicę
        return neighbours
    def exit_check(self):
        '''Sprawdza, czy wyjście jest częścią labiryntu.
        Jeśli nie, zwraca True.'''
        #sprawdzam zachodniego sąsiada
        x = self.exit[0]
        y = self.exit[1]

        #sprawdzam zachodniego sąsiada
        if x - 1 >= 0:
            if not self.cells[y][x - 1]:
                return False
        #sprawdzam wschodniego sąsiada
        if x + 1 < self.x_max:
            if not self.cells[y][x + 1]:
                return False
        #sprawdzam północnego sąsiada
        if y + 1 < self.y_max:
            if not self.cells[y + 1][x]:
                return False
        #sprawdzam południowego sąsiada
        if y - 1 >= 0:
            if not self.cells[y - 1][x]:
                return False
        return True

maze = Maze(20, 20,[0, 0],[3, 0])

for i in reversed(range(20)):
    for j in range(20):
        print("#", end=" ") if maze.cells[i][j] else print("+", end=" ")
    print()