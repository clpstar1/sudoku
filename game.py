from enum import Enum
from functools import reduce
from sudoku import Sudoku
from cursor import SudokuCursor
from sudoku import Cell


class CursorDirection(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

class Game:

    NUMBER_KEYS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]

    def __init__(self, sudoku: Sudoku) -> None:
        self.sudoku = sudoku
        self.cursor = SudokuCursor(self.sudoku)

    def sudoku_string(self, cursor = None):
        sudoku_size = self.sudoku.size()
        cell_size = self.sudoku.cell_size

        res = ""
        res += "- " * (sudoku_size + cell_size + 1) + "\n"

        for row in range(0, sudoku_size):
            for col in range(0, sudoku_size):
                cell = str(self.sudoku.get(row, col).value)

                if row == self.cursor.row and col == self.cursor.col:
                    cell = cursor if cursor else cell

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

    def move(self, direction: CursorDirection): 
        if (direction == CursorDirection.UP):
            self.cursor.up()
        elif(direction == CursorDirection.RIGHT):
            self.cursor.right()
        elif(direction == CursorDirection.DOWN):
            self.cursor.down()
        elif(direction == CursorDirection.LEFT):
            self.cursor.left()
    
    def set(self, key): 
        key = int(key)
        cell = Cell(key, True) if key != 0 else Cell(key, False)
        try:
            self.sudoku.set(self.cursor.row, self.cursor.col, cell)
        except:
            pass
    
    def check_win(self):
        return reduce(lambda prev, cur: prev and cur.solved, self.sudoku.sudoku, Cell(0, True))