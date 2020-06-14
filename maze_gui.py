import tkinter as tk
from tkinter import messagebox
import random
import maze
import my_exceptions

# Wymiar pola na kanwach.
CANVAS_DIM = 20
# Maksymalny wymiar labiryntu.
DIM_MAX = 30
# Minimalny wymiar labiryntu.
DIM_MIN = 5


class MyGUI:
    """Klasa interface'u graficznego labiryntu

    Odpowiada za graficzną reprezentację labiryntu i jego ścieżek.
    Grafika wykonana biblioteką tkinter i modułem tkinter.messagebox.

    Zmienne klasy:
    master - nasze okno.

    dim_input_frame - frame odpowiadający za wprowadzanie wymiarów labiryntu.
    dim_label - podpis lini wprowadzania wymiarów labiryntu.
    dim_entry - linia wprowadzania wymiarów labiryntu.

    entry_input_frame - frame odpowiadający za wprowadzanie wejścia labiryntu.
    entry_label - podpis lini wprowadzania wejścia labiryntu.
    entry_entry - linia wprowadzania wejścia labiryntu.

    exit_input_frame - frame odpowiadający za wprowadzanie wyjścia labiryntu.
    exit_label - podpis lini wprowadzania wyjścia labiryntu.
    exit_entry - linia wprowadzania wyjścia labiryntu.

    input_button_frame - frame przycisków.
    input_button - przycisk wprowadzania danych.
    redraw_button - przycisk ponownego rysowania tego samego labiryntu.
    draw_path_button - przycisk rysujący ścieżkę przez punkty pośrednie.

    canvas_frame - frame obiektu Canvas, który rysuje labirynt.
    maze_canvas - Canvas, rysuje labirynt i zaznaczenia punktów pośrednich.

    close_button - przycisk wychodzący z programu.

    maze - labirynt.
    inter_points - punkty pośrednie.

    Metody:

    Konstruktor:
    1. Przyjmuję obiekt master typu zwracanego przez tkinter.Tk().
    2. Początkowo zmienna maze = None i inter_points = [].

    enter_input(self) - zczytuje dane z widgetów entry, sprawdza ich
    poprawność, obsługuje wyjątki i, jeśli dane są poprawne, tworzy nowy
    labirynt.

    draw_maze(self) - rysuje labirynt na podstawie zmiennych klasy.
    Automatycznie uruchamiany po każdym poprawnym wczytaniu inputu.

    search_check(self, x, y, visited) - funkcja sprawdzająca sąsiadów
    komórki używana przy szukaniu ścieżek.

    deep_search(self, start, end) - deep-first search między dwiema komórkami.

    set_inter_point(self, event) - funkcja, która ustawia punkty pośrednie.

    draw_whole_path(self) - znajduje i rysuje ścieżkę przez
    wszystkie punkty pośrednie.

    draw_path(self, path) - rysuje ścieżkę przez zadane punkty.
    """
    def __init__(self, master):
        """
        Konstruktor klasy.
        Master to obiekt zwracany przez tkinter.TK()
        """
        self.master = master
        master.title("Generator Labiryntów")

        # Wprowadzanie wymiarów labiryntu.

        self.dim_input_frame = tk.Frame(master)
        self.dim_input_frame.pack(fill=tk.X)

        self.dim_label = tk.Label(self.dim_input_frame, text="Dimmensions")
        self.dim_label.pack(side=tk.LEFT)

        self.dim_entry = tk.Entry(self.dim_input_frame)
        self.dim_entry.pack(side=tk.RIGHT)

        # Wprowadzanie współrzędnych wejścia.
        self.entry_input_frame = tk.Frame(master)
        self.entry_input_frame.pack(fill=tk.X)

        self.entry_label = tk.Label(self.entry_input_frame,
                                    text="Entry coordinates")
        self.entry_label.pack(side=tk.LEFT)

        self.entry_entry = tk.Entry(self.entry_input_frame)
        self.entry_entry.pack(side=tk.RIGHT, fill=tk.X)

        # Wprowadzanie współrzędnych wyjścia.
        self.exit_input_frame = tk.Frame(master)
        self.exit_input_frame.pack(fill=tk.X)

        self.exit_label = tk.Label(self.exit_input_frame,
                                   text="Exit coordinates")
        self.exit_label.pack(side=tk.LEFT)

        self.exit_entry = tk.Entry(self.exit_input_frame)
        self.exit_entry.pack(side=tk.RIGHT)

        # Przycisk potwierdzający wprowadzenie danych.
        self.input_button_frame = tk.Frame(master)
        self.input_button_frame.pack()

        self.input_button = tk.Button(self.input_button_frame,
                                      text="Enter Input",
                                      command=self.enter_input)
        self.input_button.pack(side=tk.LEFT)

        self.redraw_button = tk.Button(self.input_button_frame,
                                       text="Redraw", command=self.draw_maze)
        self.redraw_button.pack(side=tk.RIGHT)

        self.draw_path_button = tk.Button(self.input_button_frame,
                                          text="Draw path",
                                          command=self.draw_whole_path)
        self.draw_path_button.pack(side=tk.BOTTOM)

        # Kanwy, podstawowy rozmiar to 10x10 pól.
        self.canvas_frame = tk.Frame(master, width=10 * CANVAS_DIM,
                                     height=10 * CANVAS_DIM)
        self.canvas_frame.pack()

        self.maze_canvas = tk.Canvas(self.canvas_frame, width=10*CANVAS_DIM,
                                     height=10*CANVAS_DIM)
        self.maze_canvas.bind("<Button-1>", self.set_inter_point)
        self.maze_canvas.pack()

        # Przycisk wyjścia z programu.
        self.close_button = tk.Button(master, text="Close",
                                      command=master.quit)
        self.close_button.pack()

        # Zmienna do przechowywania labiryntu.
        self.maze = None

        # Punkty pośrednie
        self.inter_points = []

    def enter_input(self):
        """Przyjmuje input i tworzy na jego podstawie labirynt.

        Odpowiada za podnoszenie wyjątków związanych z wymiarami labiryntu
        i pozycjami wejścia i wyjścia"""
        try:
            # Wczytuję wymiary labiryntu jako string.
            dim_str = self.dim_entry.get()
            # Rozdzielam string na tablicę według wzorca.
            dim_str = dim_str.split("x")
            # Zmieniam tablicę na tuple intigerów.
            # ValueError oznacza zły format inputu.
            dim_tuple = (int(dim_str[0]), int(dim_str[1]))

            # Sprawdzam wymiary labiryntu.
            if dim_tuple[0] < DIM_MIN or dim_tuple[1] < DIM_MIN:
                raise my_exceptions.ToSmallError
            elif dim_tuple[0] > DIM_MAX or dim_tuple[1] > DIM_MAX:
                raise my_exceptions.ToLargeError

            # Wczzytuję położenie wejścia jako string.
            entry_str = self.entry_entry.get()
            # Rozdzielam string na tablicę według wzorca.
            entry_str = entry_str.split(",")
            # Zmieniam tablicę na tuple intigerów.
            # ValueError oznacza zły format inputu.
            entry_tuple = (int(entry_str[0]), int(entry_str[1]))

            # Sprawdzam, czy wejście znajduje się na krawędzi labiryntu.
            # Jeśli nie jest na krawędzi zachodniej lub wschodniej.
            if entry_tuple[0] and entry_tuple[0] is not dim_tuple[0] - 1:
                # Jeśli nie jest na krawędzi północnej lub południowej.
                if entry_tuple[1] and entry_tuple[1] is not dim_tuple[1] - 1:
                    raise my_exceptions.NotOnEdgeError

            # Wczzytuję położenie wyjścia jako string.
            exit_str = self.exit_entry.get()
            # Rozdzielam string na tablicę według wzorca.
            exit_str = exit_str.split(",")
            # Zmieniam tablicę na tuple intigerów.
            # ValueError oznacza zły format inputu.
            exit_tuple = (int(exit_str[0]), int(exit_str[1]))

            # Sprawdzam, czy wyjście znajduje się na krawędzi labiryntu.
            # Jeśli nie jest na krawędzi zachodniej lub wschodniej.
            if entry_tuple[0] and entry_tuple[0] is not dim_tuple[0] - 1:
                # Jeśli nie jest na krawędzi północnej lub południowej.
                if entry_tuple[1] and entry_tuple[1] is not dim_tuple[1] - 1:
                    raise my_exceptions.NotOnEdgeError

            # Sprawdzam, czy wejście i wyjście nie są obok siebie.
            # Czy nie są w tym samym punkcie.
            if (entry_tuple[0] is exit_tuple[0] and
                    entry_tuple[1] is exit_tuple[1]):
                raise my_exceptions.ToCloseError
            # Sprawdzam, czy nie są obok siebie.
            # Są dokładnie 4 przypadki, którę sprawdzam.
            # 2 gdy są w tym samym rzędzie.
            elif entry_tuple[0] is exit_tuple[0]:
                # Jeśli są sąsiadami.
                if (entry_tuple[1] is exit_tuple[1] + 1 or
                        entry_tuple[1] is exit_tuple[1] - 1):
                    raise my_exceptions.ToCloseError
            # 2 gdy są w tej samej kolumnie.
            elif entry_tuple[1] is exit_tuple[1]:
                # Jeśli są sąsiadami.
                if (entry_tuple[0] is exit_tuple[0] + 1 or
                        entry_tuple[0] is exit_tuple[0] - 1):
                    raise my_exceptions.ToCloseError

            # Generuję labirynt.
            self.maze = maze.Maze(dim_tuple, entry_tuple, exit_tuple)
            self.maze.generate()
            # Czyszczę tablicę punktów pośrednich.
            self.inter_points = []
            self.draw_maze()

        except my_exceptions.ToLargeError:
            messagebox.showerror("Dimmensions error",
                                 "Maze dimmensions can't be greater than 30.")
        except my_exceptions.ToSmallError:
            messagebox.showerror("Dimmensions error",
                                 "Maze dimmensions can't be smaller than 5.")
        except ValueError:
            messagebox.showerror("Format Error",
                                 "Dimmensions must be in IntxInt format\n" +
                                 "Coodinates must be in Int,Int format.")
        except my_exceptions.NotOnEdgeError:
            messagebox.showerror("Coordinates Error",
                                 "Entry and Exit must be on the mazes edge.")
        except my_exceptions.ToCloseError:
            messagebox.showerror("Coordinates Error",
                                 "Entry and Exit cannot touch.")

    def draw_maze(self):
        """Rysuje labirynt na podstawie zmiennych klasy"""

        if self.maze:
            # Dla skrócenia zapisu.
            y_max = self.maze.y_max
            x_max = self.maze.x_max

            # Dostosowuję rozmiar kanw do liczby pól.
            self.canvas_frame.configure(width=x_max * CANVAS_DIM,
                                        height=y_max * CANVAS_DIM)
            self.maze_canvas.configure(width=x_max * CANVAS_DIM,
                                       height=y_max * CANVAS_DIM)

            # Rysuję labirynt.
            for i in range(y_max):
                for j in range(x_max):
                    if self.maze.cells[i][j]:
                        self.maze_canvas.create_rectangle(j * CANVAS_DIM,
                                                          (y_max - i - 1) *
                                                          CANVAS_DIM,
                                                          (j+1)*CANVAS_DIM,
                                                          (y_max - i) *
                                                          CANVAS_DIM,
                                                          fill="black")
                    else:
                        self.maze_canvas.create_rectangle(j * CANVAS_DIM,
                                                          (y_max - i - 1) *
                                                          CANVAS_DIM,
                                                          (j + 1) *
                                                          CANVAS_DIM,
                                                          (y_max - i) *
                                                          CANVAS_DIM,
                                                          fill="white")
            # Dorysowuję wejście.
            x, y = self.maze.entry
            self.maze_canvas.create_rectangle(x * CANVAS_DIM,
                                              (y_max - y - 1) * CANVAS_DIM,
                                              (x + 1) * CANVAS_DIM,
                                              (y_max - y) * CANVAS_DIM,
                                              fill="green")
            # Dorysowuję wyjście.
            x, y = self.maze.exit
            self.maze_canvas.create_rectangle(x * CANVAS_DIM,
                                              (y_max - y - 1) * CANVAS_DIM,
                                              (x + 1) * CANVAS_DIM,
                                              (y_max - y) * CANVAS_DIM,
                                              fill="red")
            # Dorysowuję punkty pośrednie.
            for point in self.inter_points:
                x, y = point
                self.maze_canvas.create_rectangle(x * CANVAS_DIM,
                                                  (y_max - y - 1) *
                                                  CANVAS_DIM,
                                                  (x + 1) * CANVAS_DIM,
                                                  (y_max - y) * CANVAS_DIM,
                                                  fill="magenta")

    def search_check(self, x, y, visited):
        '''Sprawdza, do których pól funkcja szukająca ścieżki może wejść.

        Przyjmuje współżędne obecnego punktu.
        Zwraca listę współżędnych sąsiednich pól, do których można wejść.
        W przypadku ślepego zaułka, zwraca [].'''

        neighbours = []

        # Sprawdza zachodniego sąsiada.
        if x - 1 >= 0:
            # Jeśli sąsiad nie jest murem.
            if not self.maze.cells[y][x - 1]:
                # Jeśli sąsiad jest nieodwiedzony
                if (x - 1, y) not in visited:
                    neighbours.append((x - 1, y))
        # Sprawdzam wschodniego sąsiada.
        if x + 1 < self.maze.x_max:
            # Jeśli sąsiad nie jest murem.
            if not self.maze.cells[y][x + 1]:
                # Jeśli sąsiad jest nieodwiedzony
                if (x + 1, y) not in visited:
                    neighbours.append((x + 1, y))
        # Sprawdzam północnego sąsiada.
        if y + 1 < self.maze.y_max:
            # Jeśli sąsiad nie jest murem.
            if not self.maze.cells[y + 1][x]:
                # Jeśli sąsiad jest nieodwiedzony
                if (x, y + 1) not in visited:
                    neighbours.append((x, y + 1))
        # Sprawdzam południowego sąsiada.
        if y - 1 >= 0:
            # Jeśli sąsiad nie jest murem.
            if not self.maze.cells[y - 1][x]:
                # Jeśli sąsiad jest nieodwiedzony
                if (x, y - 1) not in visited:
                    neighbours.append((x, y - 1))

        # Zwracam tablicę.
        return neighbours

    def deep_search(self, start, end):
        """Znajduje ścieżkę między punktami algorytmem deep-first search.

        Po wykonaniu rysuje znalezioną ścieżkę."""
        xs, ys = start
        xe, ye = end

        # Stos do backtrackingu.
        stack = [(xs, ys)]
        # Lista odwiedzonych pól.
        visited = [(xs, ys)]

        # Szukam dopóki nie dojdę do szukanego pola.
        # Algorytm generacji gwarantuje,
        # że mogę wytyczyć trasę między dowolnymi dwoma polami korytarza.
        while (xs is not xe) or (ys is not ye):
            # Wyznaczam sąsiadów.
            neighs = self.search_check(xs, ys, visited)
            # Jeśli mam sąsiada.
            if neighs:
                if (xs, ys) not in stack:
                    stack.append((xs, ys))
                # Wybieram sąsiada.
                neigh = random.choice(neighs)
                # Dodaje sąsiada do odwiedzonych.
                visited.append(neigh)
                # Dodaję sąsiada do stack w celu backtrackingu.
                stack.append(neigh)
                # Przechodzę do sąsiada.
                xs, ys = neigh
            else:
                # Jeśli nie ma sąsiada, to cofam się o do poprzedniego.
                xs, ys = stack.pop()

        # Rysuję znalezioną ścieżkę.
        self.draw_path(stack)

    def set_inter_point(self, event):
        """ Ustawia punkt pośredni"""

        # Jeśli istnieje już labirynt.
        if self.maze:
            # Sprowadzenie współżędnych w pixelach do numerów kratek.
            x = event.x // CANVAS_DIM
            y = self.maze.y_max - (event.y // CANVAS_DIM) - 1

            # Jeśli pozycja jest już na liście, to ją usuwam.
            if (x, y) in self.inter_points:
                self.inter_points.remove((x, y))
                self.draw_maze()
            # Jeśli nie, to dodaję.
            elif not self.maze.cells[y][x]:
                self.inter_points.append((x, y))
                self.draw_maze()

    def draw_whole_path(self):
        """Rysuję ścieżkę przez wszyskie punkty pośrednie.

        Skoro reprezentacja ścieżki jest graficzna, to stosuję heurystykę
        opartą o algorytm Held'a-Karp'a.

        """

        # Jeśli istnieje labirynt.
        if self.maze:
            # Jeśli istnieją punkty pośrednie.
            if self.inter_points:
                tmp_points = self.inter_points[:]
                point1 = self.maze.entry
                point2 = tmp_points.pop(0)

                self.deep_search(point1, point2)
                while tmp_points:
                    point1 = point2
                    point2 = tmp_points.pop(0)
                    self.deep_search(point1, point2)

                point1 = point2
                point2 = self.maze.exit
                self.deep_search(point1, point2)

            else:
                point1 = self.maze.entry
                point2 = self.maze.exit
                self.deep_search(point1, point2)

            # Zaznaczam na rysunku wejście i wyjście.
            x, y = self.maze.entry
            self.maze_canvas.create_rectangle(x * CANVAS_DIM,
                                              (self.maze.y_max - y - 1) *
                                              CANVAS_DIM,
                                              (x + 1) * CANVAS_DIM,
                                              (self.maze.y_max - y) *
                                              CANVAS_DIM, fill="green")
            x, y = self.maze.exit
            self.maze_canvas.create_rectangle(x * CANVAS_DIM,
                                              (self.maze.y_max - y - 1) *
                                              CANVAS_DIM,
                                              (x + 1) * CANVAS_DIM,
                                              (self.maze.y_max - y) *
                                              CANVAS_DIM, fill="red")

    def draw_path(self, path):
        """
        Rysuję ścieżkę path.
        """

        # Dla każdego elementu ścieżki zamalowuję pole na "cyan"
        for x, y in path:
            self.maze_canvas.create_rectangle(x * CANVAS_DIM,
                                              (self.maze.y_max - y - 1) *
                                              CANVAS_DIM,
                                              (x + 1) * CANVAS_DIM,
                                              (self.maze.y_max - y) *
                                              CANVAS_DIM,
                                              fill="cyan")

if __name__ == '__main__':
    root = tk.Tk()
    my_gui = MyGUI(root)
    root.mainloop()
