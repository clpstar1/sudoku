from random import randint
import sys
from typing import List
from sudoku_base import Sudoku
from printer import print_sudoku

class SudokuCursor: 

    def __init__(self, sudoku: Sudoku) -> None:
        self.sudoku = sudoku
        self.sudoku_size = sudoku.size()
        self.row = 0 
        self.col = 0

    def hasNext(self) -> bool:
        return self.row < self.sudoku_size and self.col < self.sudoku_size

    def hasPrev(self) -> bool:
        return self.row > 0 and self.col > 0

    def next(self) -> None:
        # end reached 
        if (
            self.row == self.sudoku_size and 
            self.col == self.sudoku_size
        ): raise Exception("Error: next: no next element")
        # new row 
        if self.col == self.sudoku_size-1:
            self.row += 1
            self.col = 0
        else: 
            self.col += 1
    
    def prev(self) -> None: 
        if (
            self.row == 0 and 
            self.col == 0
        ): raise Exception("Error: prev: no previous element")

        if self.col == 0: 
            self.row -= 1
            self.col = self.sudoku_size
        else: 
            self.col -= 1

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

def generate_sudoku(sudoku_sz):
    sudoku = Sudoku(sudoku_sz)
    cursor = SudokuCursor(sudoku)
    cache = SudokuCache()
    while cursor.hasNext():
        
        cached = cache.get(cursor.row, cursor.col)

        if len(cached) == sudoku_sz:
            if not cursor.hasPrev(): 
                sudoku = Sudoku(sudoku_sz)
                cursor = SudokuCursor(sudoku)
                cache = SudokuCache()
            else: cursor.prev()
        else: 
            
            element = -1
            while element == -1 and element not in cached:
                element = randint(1, sudoku_sz)
            
            cache.set(cursor.row, cursor.col, element)

            try:
                sudoku.set(cursor.row, cursor.col, element)
                if cursor.hasNext():
                    cursor.next() 
            except:
                pass

    return sudoku

def add_holes(sudoku: Sudoku, percentage):
    sudoku_sz_flat = sudoku.size() ** 2
    num_holes = int(sudoku_sz_flat * percentage)

    holes = set()
    while len(holes) < num_holes:
        holes.add(randint(0, sudoku_sz_flat-1))
    
    for hole in holes:
        sudoku.sudoku[hole] = '?'
    
    return sudoku

        
if __name__ == "__main__":
        
    sudoku = generate_sudoku(int(sys.argv[1]) or 9)
    sudoku = add_holes(sudoku, 0.5)

    print_sudoku(sudoku)