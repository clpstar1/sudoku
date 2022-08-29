from random import randint
from typing import List
from sudoku import Sudoku, Cell
from cursor import SudokuCursor

class SudokuCache: 

    def __init__(self) -> None:
        self.cache = {}

    def set(self, row, col, item) -> bool: 
        index = self._index(row, col)
        if index not in self.cache:
            self.cache[index] = set()
        self.cache[index].add(item)
    
    def get(self, row, col) -> List[int]:
        index = self._index(row, col)
        if index not in self.cache:
            self.cache[index] = set()
        return self.cache[index]

    def clear(self, row, col):
        index = self._index(row, col)
        if index in self.cache:
            self.cache[index] = set()

    def _index(self, row, col): 
        return f"{row}{col}"

def fill(sudoku: Sudoku):
    cursor = SudokuCursor(sudoku)
    cache = SudokuCache()
    sudoku_sz = sudoku.size()
    while cursor.row < sudoku_sz and cursor.col < sudoku_sz:

        if (sudoku.get(cursor.row, cursor.col).solved == True):
            cursor.next()
            continue
        
        cached = cache.get(cursor.row, cursor.col)

        if len(cached) == sudoku_sz:
            
            # clear cache, set cell to unsolved, and try again
            cache.clear(cursor.row, cursor.col)
            sudoku.set(cursor.row, cursor.col, Cell(0, False)) 
            cursor.prev()
            while (sudoku.get(cursor.row, cursor.col).solved == True):
                cursor.prev()

        else: 
            
            element = -1
            while element not in cached:
                element = randint(1, sudoku_sz)
                cache.set(cursor.row, cursor.col, element)

            try:
                sudoku.set(cursor.row, cursor.col, Cell(element, False))
                cursor.next() 
            except:
                pass

    
    sudoku.sudoku = [Cell(cell.value, True, cell.value) for cell in sudoku.sudoku]
    return sudoku

def holes(sudoku: Sudoku, percentage):
    sudoku_sz_flat = sudoku.size() ** 2
    num_holes = int(sudoku_sz_flat * percentage)

    holes = set()
    while len(holes) < num_holes:
        holes.add(randint(0, sudoku_sz_flat-1))
    
    for hole in holes:
        cell = sudoku.sudoku[hole]
        
        sudoku.sudoku[hole] = Cell(0, False, cell.value)
    
    return sudoku
