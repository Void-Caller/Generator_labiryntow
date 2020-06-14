import tkinter as tk
import random
import time
import maze
import my_exceptions

#Wymiar pola na kanwach
CANVAS_DIM = 20

class MyGUI:
    def __init__(self, master):
        self.master = master
        master.title("Generator Labiryntów")

        #Nagłówek
        self.label = tk.Label(master, text="This is our first GUI!")
        self.label.pack(side = tk.TOP)

        #Wprowadzanie wymiarów labiryntu.

        self.dim_input_frame = tk.Frame(master)
        self.dim_input_frame.pack(fill = tk.X)

        self.dim_label = tk.Label(self.dim_input_frame, text = "Dimmensions")
        self.dim_label.pack(side = tk.LEFT)

        self.dim_entry = tk.Entry(self.dim_input_frame)
        self.dim_entry.pack(side = tk.RIGHT)

        #Wprowadzanie współrzędnych wejścia
        self.entry_input_frame = tk.Frame(master)
        self.entry_input_frame.pack(fill = tk.X)

        self.entry_label = tk.Label(self.entry_input_frame, text="Entry coordinates")
        self.entry_label.pack(side=tk.LEFT)

        self.entry_entry = tk.Entry(self.entry_input_frame)
        self.entry_entry.pack(side=tk.RIGHT, fill = tk.X)

        #Wprowadzanie współrzędnych wyjścia
        self.exit_input_frame = tk.Frame(master)
        self.exit_input_frame.pack(fill = tk.X)

        self.exit_label = tk.Label(self.exit_input_frame, text="Exit coordinates")
        self.exit_label.pack(side=tk.LEFT)

        self.exit_entry = tk.Entry(self.exit_input_frame)
        self.exit_entry.pack(side=tk.RIGHT)

        #Przycisk potwierdzający wprowadzenie danych
        self.input_button_frame = tk.Frame(master)
        self.input_button_frame.pack()

        self.input_button = tk.Button(self.input_button_frame, text="Enter Input", command=self.enter_input)
        self.input_button.pack(side = tk.LEFT)

        self.redraw_button = tk.Button(self.input_button_frame, text="Redraw", command=self.draw_maze)
        self.redraw_button.pack(side=tk.RIGHT)

        self.draw_path_button = tk.Button(self.input_button_frame, text="Draw path", command=self.draw_whole_path)
        self.draw_path_button.pack(side=tk.BOTTOM)

        #Kanwy, podstawowy rozmiar to 10x10 pól
        self.canvas_frame = tk.Frame(master, width = 10 * CANVAS_DIM, height = 10 * CANVAS_DIM)
        self.canvas_frame.pack()

        self.maze_canvas = tk.Canvas(self.canvas_frame, width = 10*CANVAS_DIM, height = 10*CANVAS_DIM)
        self.maze_canvas.bind("<Button-1>", self.set_inter_point)
        self.maze_canvas.pack()

        self.close_button = tk.Button(master, text="Close", command=master.quit)
        self.close_button.pack()

        #labirynt
        self.maze = None

        #punkty pośrednie
        self.inter_points = []

    def enter_input(self):
        """Przyjmuje input i tworzy na jego podstawie labirynt.
        Ta funkcja odpowiada za wyjątki związane z wymiarami labiryntu i
        pozycjami wejścia i wyjścia"""

        dim_str = self.dim_entry.get()
        dim_str = dim_str.split("x")
        dim_tuple = (int(dim_str[0]), int(dim_str[1]))

        entry_str = self.entry_entry.get()
        entry_str = entry_str.split(",")
        entry_tuple = (int(entry_str[0]), int(entry_str[1]))

        exit_str = self.exit_entry.get()
        exit_str = exit_str.split(",")
        exit_tuple = (int(exit_str[0]), int(exit_str[1]))

        self.maze = maze.Maze(dim_tuple, entry_tuple, exit_tuple)
        self.maze.generate()
        self.inter_points = []
        self.draw_maze()

    def draw_maze(self):
        '''Rysuje labirynt na podstawie zmiennych klasy'''

        if self.maze:
            self.canvas_frame.configure(width = self.maze.x_max*CANVAS_DIM, height = self.maze.y_max*CANVAS_DIM)
            self.maze_canvas.configure(width = self.maze.x_max*CANVAS_DIM, height = self.maze.y_max*CANVAS_DIM)

            for i in range(self.maze.y_max):
                for j in range(self.maze.x_max):
                    if self.maze.cells[i][j]:
                        self.maze_canvas.create_rectangle(j * CANVAS_DIM,(self.maze.y_max - i - 1)
                                                          * CANVAS_DIM,(j+1)*CANVAS_DIM,(self.maze.y_max - i)
                                                          * CANVAS_DIM, fill = "black")
                    else:
                        self.maze_canvas.create_rectangle(j * CANVAS_DIM, (self.maze.y_max - i - 1)
                                                          * CANVAS_DIM, (j + 1) * CANVAS_DIM, (self.maze.y_max - i)
                                                          * CANVAS_DIM, fill="white")

            x, y = self.maze.entry
            self.maze_canvas.create_rectangle(x * CANVAS_DIM, (self.maze.y_max - y - 1)
                                              * CANVAS_DIM, (x + 1) * CANVAS_DIM, (self.maze.y_max - y)
                                              * CANVAS_DIM, fill="green")
            x, y = self.maze.exit
            self.maze_canvas.create_rectangle(x * CANVAS_DIM, (self.maze.y_max - y - 1)
                                              * CANVAS_DIM, (x + 1) * CANVAS_DIM, (self.maze.y_max - y)
                                              * CANVAS_DIM, fill="red")

            for point in self.inter_points:
                x, y = point
                self.maze_canvas.create_rectangle(x * CANVAS_DIM, (self.maze.y_max - y - 1)
                                                  * CANVAS_DIM, (x + 1) * CANVAS_DIM, (self.maze.y_max - y)
                                                  * CANVAS_DIM, fill="magenta")

    def search_check(self, x, y, visited):
        '''Sprawdza, do których pól funkcja szukająca ścieżki może wejść.
        Przyjmuje współżędne obecnego punktu.
        Zwraca listę współżędnych sąsiednich pól, do których można wejść.
        W przypadku ślepego zaułka, zwraca [].'''

        neighbours = []

        #sprawdza zachodniego sąsiada
        if x - 1 >= 0:
            #Jeśli sąsiad nie jest murem.
            if not self.maze.cells[y][x - 1]:
                #Jeśli sąsiad jest nieodwiedzony
                if (x - 1, y) not in visited:
                    neighbours.append((x - 1, y))
        #sprawdzam wschodniego sąsiada
        if x + 1 < self.maze.x_max:
            # Jeśli sąsiad nie jest murem.
            if not self.maze.cells[y][x + 1]:
                #Jeśli sąsiad jest nieodwiedzony
                if (x + 1, y) not in visited:
                    neighbours.append((x + 1, y))
        #sprawdzam północnego sąsiada
        if y + 1 < self.maze.y_max:
            # Jeśli sąsiad nie jest murem.
            if not self.maze.cells[y + 1][x]:
                #Jeśli sąsiad jest nieodwiedzony
                if (x, y + 1) not in visited:
                    neighbours.append((x, y + 1))
        #sprawdzam południowego sąsiada
        if y - 1 >= 0:
            # Jeśli sąsiad nie jest murem.
            if not self.maze.cells[y - 1][x]:
                #Jeśli sąsiad jest nieodwiedzony
                if (x, y - 1) not in visited:
                    neighbours.append((x, y - 1))

        #zwracam tablicę
        return neighbours

    def deep_search(self, start, end):
        '''Znajduje ścieżkę między punktami start i end w oparciu o
        algorytm deep-first search. Zwraca tablicę krotek współżędnych,
        które odpowiadają kolejnym krokom ścieżki'''
        xs, ys = start
        xe, ye = end

        #stos do backtrackingu
        stack = [(xs, ys)]
        #lista odwiedzonych pól
        visited = [(xs, ys)]

        #Szukam dopóki nie dojdę do szukanego pola.
        #Algorytm generacji gwarantuje,
        #że mogę wytyczyć trasę między dowolnymi dwoma polami korytarza
        while (xs is not xe) or (ys is not ye):
            #Wyznaczam sąsiadów.
            neighs = self.search_check(xs, ys, visited)
            #Jeśli mam sąsiada.
            if neighs:
                if (xs, ys) not in stack:
                    stack.append((xs, ys))
                #Wybieram sąsiada.
                neigh = random.choice(neighs)
                #Dodaje sąsiada do odwiedzonych.
                visited.append(neigh)
                #Dodaję sąsiada do stack w celu backtrackingu.
                stack.append(neigh)
                #Przechodzę do sąsiada.
                xs, ys = neigh
            else:
                #Jeśli nie ma sąsiada, to cofam się o do poprzedniego.
                xs, ys = stack.pop()

        self.draw_path(stack)

    def set_inter_point(self, event):
        if self.maze:
            x = event.x // CANVAS_DIM
            y = self.maze.y_max - (event.y // CANVAS_DIM) - 1

            if (x, y) in self.inter_points:
                self.inter_points.remove((x, y))
                self.draw_maze()
            elif not self.maze.cells[y][x]:
                self.inter_points.append((x, y))
                self.draw_maze()
            print("clicked at", x, y)

    def draw_whole_path(self):
        if self.maze:
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

            x, y = self.maze.entry
            self.maze_canvas.create_rectangle(x * CANVAS_DIM, (self.maze.y_max - y - 1)
                                              * CANVAS_DIM, (x + 1) * CANVAS_DIM, (self.maze.y_max - y)
                                              * CANVAS_DIM, fill="green")
            x, y = self.maze.exit
            self.maze_canvas.create_rectangle(x * CANVAS_DIM, (self.maze.y_max - y - 1)
                                              * CANVAS_DIM, (x + 1) * CANVAS_DIM, (self.maze.y_max - y)
                                              * CANVAS_DIM, fill="red")



    def draw_path(self, path):
        for x, y in path:
            self.maze_canvas.create_rectangle(x * CANVAS_DIM, (self.maze.y_max - y - 1)
                                              * CANVAS_DIM, (x + 1) * CANVAS_DIM, (self.maze.y_max - y)
                                              * CANVAS_DIM, fill="cyan")

root = tk.Tk()
my_gui = MyGUI(root)
root.mainloop()