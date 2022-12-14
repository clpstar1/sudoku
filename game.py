from enum import Enum
from functools import reduce
from typing import List
from sudoku import Sudoku
from cursor import SudokuCursor
from sudoku import Cell
from generator import fill, holes
import curses as cu
from interval import Interval

def notify_listeners(f):
    def wrapper(*args):
        f(*args)
        args[0].notify()
    return wrapper

class CursorDirection(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class Screen():

    BLINK_DURATION = 0.25

    def __init__(self, window: cu.window):

       
        self.window = window
        
        self.sudoku_win = window.derwin(15, 27, 0, 0)
        self.status_win = window.derwin(5, 100, 13, 0)
        self.opt_win = window.derwin(10, 100, 0, 27)

        self.game: Game = None
        self.interval = None

    
    def render(self, cursor = None):
        self.opt_win.erase()
        self.sudoku_win.erase()
        self.status_win.erase()
        self.window.erase()
        self.opt_win.addstr(self.__options)
        self.sudoku_win.addstr(self.render_sudoku(cursor))
        self.status_win.addstr(f"{self.__available_string(self.game.available())}\n{self.__difficulty_string(self.game.difficulty)}")

        self.sudoku_win.refresh()
        

    __options = "Controls:\n(n)ew\n(q)uit\n(c)lear\n(r)eveal\n[1 - 9]: set cell\n[arrow]: move\n[+ / -]: adjust difficulty"

    def __available_string(self, avail):
        return f"Available : {avail}"

    def __difficulty_string(self, diff):
        return f"Difficulty: {float(diff) * 100}% holes"

    
    def render_sudoku(self, cursor = None):
        sudoku = self.game.sudoku
        sudoku_size = sudoku.size()
        cell_size = sudoku.cell_size

        res = ""
        res += "- " * (sudoku_size + cell_size + 1) + "\n"

        for row in range(0, sudoku_size):
            for col in range(0, sudoku_size):
                cell = sudoku.get(row, col)

                cell = "?" if cell.value == 0 else str(cell.value)

                if row == self.game.cursor.row and col == self.game.cursor.col:
                    cell = cursor if cursor != None else cell

                if col == 0:
                    res += "| " + cell + " "
                
                elif (col+1) % cell_size == 0:
                    res += cell + " | "
                    
                else:
                    res += cell + " " 
            
            res += "\n"

            if (row+1) % cell_size == 0:
                res += "- " * (sudoku_size + cell_size + 1) + "\n"
        return res


    def onUpdate(self, game):
        self.game = game
        self.restart()

    def start(self):

        self.render(" ")
        self.interval = Interval(
            self.BLINK_DURATION, 
            lambda : self.render(" "),
            lambda : self.render()
        )
        self.interval.start()

    def stop(self):
        if self.interval:
            self.interval.stop()
    
    def restart(self):
        self.stop()
        self.start()

class Game:

    NUMBER_KEYS = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

    def __init__(self, sudoku: Sudoku, difficulty) -> None:
        self.sudoku = sudoku
        self.cursor = SudokuCursor(self.sudoku)
        self.difficulty = difficulty
        self.listeners: List[Screen] = []
    
    def addListener(self, screen: Screen):
        self.listeners.append(screen)

    def new(size, difficulty): 
        return Game(Game.__new_sudoku(size, difficulty), difficulty)

    @notify_listeners
    def move(self, direction: CursorDirection): 
        if (direction == CursorDirection.UP):
            self.cursor.up()
        elif(direction == CursorDirection.RIGHT):
            self.cursor.right()
        elif(direction == CursorDirection.DOWN):
            self.cursor.down()
        elif(direction == CursorDirection.LEFT):
            self.cursor.left()

    @notify_listeners
    def set(self, key): 
        key = int(key)
        cell = self.__get()
        try:
            self.sudoku.set(self.cursor.row, self.cursor.col, Cell(key, True, cell.original_value))
        except:
            pass
    
    @notify_listeners
    def unset(self):
        cell = self.__get()
        try:
            self.sudoku.set(self.cursor.row, self.cursor.col, Cell(0, False, cell.original_value))
        except:
            pass
    
    @notify_listeners
    def raise_difficulty_by(self, value): 
        new_difficulty = (self.difficulty * 10) + value
        if new_difficulty >= 10.0 or new_difficulty <= 0.0: return
        self.difficulty = new_difficulty / 10 
        self.sudoku = Game.__new_sudoku(self.sudoku.size(), self.difficulty)
    
    @notify_listeners
    def reset(self):
        self.sudoku = Game.__new_sudoku(self.sudoku.size(), self.difficulty)
    
    @notify_listeners
    def reveal(self):
        original_cell = self.__get()
        original_cell.value  = original_cell.original_value

    def check_win(self):
        return reduce(lambda prev, cur: prev and cur.solved, self.sudoku.sudoku, Cell(0, True))

    def available(self):
        return str(self.sudoku.available(self.cursor.row, self.cursor.col))

    def __new_sudoku(size, difficulty):
        h = Game.__curry(Game.__flip(holes))(difficulty)
        s = Game.__compose(h, fill)(Sudoku(size))
        return s

    def notify(self):
        for listener in self.listeners:
            listener.onUpdate(self)
    
    def __set(self, item: Cell):
        return self.sudoku.set(self.cursor.row, self.cursor.col, item)

    def __get(self):
        return self.sudoku.get(self.cursor.row, self.cursor.col)

    def __compose(f, g):
        return lambda x : f(g(x))

    def __flip(f):
        return lambda a, b: f(b, a)
    
    def __curry(f):
        return lambda a: lambda b: f(a, b)

