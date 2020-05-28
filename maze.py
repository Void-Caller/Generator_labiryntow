import random
import time

random.seed(time.time())

class Too_large_exception(Exception):
    pass

class Too_small_exception(Exception):
    pass

class Maze:
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
        self.cells = [[True for i in range(x)] for j in range(y)]
        self.entry = entry.copy()
        self.exit = exit.copy()
        self.generate()
        self.find_linear(entry,exit)

    def generate(self):
        self.cells[self.entry[1]][self.entry[0]] = False
        '''kroki:
        1 - wylosuj trzy punkty (A,B i C) oprocz wyjscia i wejscia
        2 - twórz liniową ścierzkę między entry i A
        3 - usuń pokoje
        4 - twórz liniową ścierzkę między A i B
        5 - usuń pokoje
        6 - liniowa między B i C
        7 - usuń pokoje
        8 - liniowa między C i exit'''

    def find_linear(self, point_a, point_b):
        y=point_a[1]
        x=point_a[0]
        dx=1
        dy=1
        x_b=x-point_b[0]
        y_b=y-point_b[1]
        if x_b>0:
            dx=-1
        if y_b>0:
            dy=-1

        while x_b or y_b:
            if x_b:
                if abs(x_b)>2:
                    r=random.randint(1, abs(x_b))
                    for i in range(r):
                        self.cells[y][x + dx] = False
                        x += dx
                        x_b = x - point_b[0]
                else:
                    self.cells[y][x + dx] = False
                    x += dx
                    x_b = x - point_b[0]
            if y_b:
                r=random.randint(1, abs(y_b))
                if abs(y_b)>1:
                    for i in range(r):
                        self.cells[y + dy][x]=False
                        y += dy
                        y_b = y - point_b[1]
                else:
                    self.cells[y + dy][x] = False
                    y += dy
                    y_b = y - point_b[1]



maze = Maze(10, 10,[0, 0],[9, 9])

for i in range(10):
    for j in range(10):
        print("#", end=" ") if maze.cells[i][j] else print("@", end=" ")
    print()