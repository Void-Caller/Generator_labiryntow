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
        self.x_max = x
        self.y_max = y
        self.cells = [[True for i in range(x)] for j in range(y)]
        self.entry = entry.copy()
        self.exit = exit.copy()
        self.generate()

    def generate(self):
        '''kroki:
        1 - wylosuj trzy punkty (A,B i C) oprocz wyjscia i wejscia
        2 - twórz liniową ścierzkę między entry i A
        3 - usuń pokoje
        4 - twórz liniową ścierzkę między A i B
        5 - usuń pokoje
        6 - liniowa między B i C
        7 - usuń pokoje
        8 - liniowa między C i exit'''
        self.cells[self.entry[0]][self.entry[1]] = False
        #losowanie
        #Gwarantuję, że współżędne wylosowanych punktów nie pokryją się z wejściem i wyjściem.
        #Dodatkowo, plasuję je w oddzielnych rzędach, by uniknąć linii prostych.
        tabx = [i for i in range(self.x_max)]
        taby = [i for i in range(self.y_max)]
        tabx.remove(self.entry[0])
        if self.exit[0] in tabx:
            tabx.remove(self.exit[0])
        taby.remove(self.entry[1])
        if self.exit[1] in taby:
            taby.remove(self.exit[1])
        #Wylosowany punkt 1
        point1 = [random.choice(tabx),random.choice(taby)]

        tabx.remove(point1[0])
        taby.remove(point1[1])

        point2 = [random.choice(tabx), random.choice(taby)]

        tabx.remove(point2[0])
        taby.remove(point2[1])

        point3 = [random.choice(tabx), random.choice(taby)]

        self.find_linear(self.entry,point1)
        self.find_linear(point1,point2)
        self.room_check()
        self.find_linear(point2, point3)
        self.room_check()
        self.find_linear(point3,self.exit)
        self.room_check()

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

    def correct_room(self,x,y):
        '''Sprawdza, czy w danym miejscu znajduje się pokój. Jeśli tak, to go usuwa.
        False - nic nie znalazł. True - znalazł i naprawił.'''
        if not self.cells[x][y]:
            if not self.cells[x][y+1]:
                if not self.cells[x+1][y]:
                    if not self.cells[x+1][y+1]:
                        self.cells[x+random.randint(0,1)][y+random.randint(0,1)] = True
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False

    def correct_diagonal(self,x,y):
        '''Koryguje ścieżki przerwane przez correct_room.
        False - nic nie skorygował. True - znalazł i skorygował przerwę'''
        '''if self.cells[x][y]:
            if self.cells[x+1][y+1]:
                if self.cells[x][y+1] or self.cells[x+1][y]:
                    return True
                elif self.cells[x+1][y]:
                    return True
                else:'''
        if self.cells[x][y] and self.cells[x+1][y+1]:
            if self.cells[x][y+1] or self.cells[x+1][y]:
                return False
            else:
                d = random.randint(0,1)
                self.cells[x+d][y+d] = False
                return True
        elif self.cells[x][y+1] and self.cells[x+1][y]:
            if self.cells[x][y] or self.cells[x+1][y+1]:
                return False
            else:
                d = random.randint(0,1)
                self.cells[x+d][y+(not d)] = False
                return True

    def room_check(self):
        '''Szuka i usuwa pokoje'''
        for i in range(self.x_max-1):
            for j in range(self.y_max-1):
                self.correct_room(i,j)
        for i in range(self.x_max-1):
            for j in range(self.y_max-1):
                self.correct_diagonal(i,j)

maze = Maze(20, 20,[0, 0],[0, 3])

for i in range(20):
    for j in range(20):
        print("#", end=" ") if maze.cells[i][j] else print("@", end=" ")
    print()