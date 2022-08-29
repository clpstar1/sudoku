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
        self.game: Game = None
        self.interval = None

    
    def render(self, cursor = None):
        self.window.erase()
        self.window.addstr(self.render_sudoku(cursor))
        self.window.addstr(self.__available_string(self.game.available()))
        self.window.addstr(self.__difficulty_string(str(self.game.difficulty)))
        self.window.addstr(self.__options)
        
    __options = "Controls:\t(n)ew; (q)uit; (c)lear;\n\t\t[0-9]: set cell; [arrows]: move; [+/-]: adjust difficulty"

    def __available_string(self, avail):
        return f"Available:\t{avail} \n"

    def __difficulty_string(self, diff):
        return f"Difficulty: \t{float(diff) * 100}% holes \n"

    
    def render_sudoku(self, cursor = None):
        sudoku = self.game.sudoku
        sudoku_size = sudoku.size()
        cell_size = sudoku.cell_size

        res = ""
        res += "- " * (sudoku_size + cell_size + 1) + "\n"

        for row in range(0, sudoku_size):
            for col in range(0, sudoku_size):
                cell = str(sudoku.get(row, col).value)

                cell = "?" if cell == "0" else cell

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
        try:
            self.sudoku.set(self.cursor.row, self.cursor.col, Cell(key, True))
        except:
            pass
    
    @notify_listeners
    def unset(self):
        try:
            self.sudoku.set(self.cursor.row, self.cursor.col, Cell(0, False))
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

    def __compose(f, g):
        return lambda x : f(g(x))

    def __flip(f):
        return lambda a, b: f(b, a)
    
    def __curry(f):
        return lambda a: lambda b: f(a, b)

