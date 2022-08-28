from random import randint
from typing import List
from sudoku import Sudoku
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

    def _index(self, row, col): 
        return f"{row}{col}"

def fill(sudoku: Sudoku):
    sudoku_sz = sudoku.size()
    cursor = SudokuCursor(sudoku)
    cache = SudokuCache()

    while cursor.hasNext():
        
        cached = cache.get(cursor.row, cursor.col)

        if len(cached) == sudoku_sz:
            if not cursor.hasPrev(): 
                sudoku.clear()
                cursor = SudokuCursor(sudoku)
                cache = SudokuCache()
            else: cursor.prev()

        else: 
            
            element = 0
            while element not in cached:
                element = randint(1, sudoku_sz)
                cache.set(cursor.row, cursor.col, element)

            try:
                sudoku.set(cursor.row, cursor.col, element)
                if cursor.hasNext():
                    cursor.next() 
            except:
                pass

    return sudoku

def holes(sudoku: Sudoku, percentage):
    sudoku_sz_flat = sudoku.size() ** 2
    num_holes = int(sudoku_sz_flat * percentage)

    holes = set()
    while len(holes) < num_holes:
        holes.add(randint(0, sudoku_sz_flat-1))
    
    for hole in holes:
        sudoku.sudoku[hole] = 0
    
    return sudoku

