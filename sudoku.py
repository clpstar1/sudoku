from typing import List
from math import sqrt

sudoku_sz = 9

class Cell:

    def __init__(self, value, solved, original_value = None) -> None:
        self.value = value
        self.solved = solved
        self.original_value = original_value or value

class Sudoku:

    def __init__(self, size) -> None:
        self.sudoku = [Cell(0, False)] * (size ** 2)
        self.sudoku_size = size
        self.cell_size = int(sqrt(size))

        self.index_cache = {}

    def size(self) -> int:
        return self.sudoku_size
    
    def get(self, row, col) -> Cell:
        return self.sudoku[self._index(row, col)]

    def set(self, row, col, cell: Cell) -> None:
        if not self._check(row, col, cell.value):
            raise Exception(f"Error: set: cannot set item: {cell.value} at position [{row}, {col}]")

        index = self._index(row, col)
        self.sudoku[index] = cell
    
    def clear(self) -> None:
        self.sudoku = map(lambda cell: Cell(0, False) if cell.solved == False else cell, self.sudoku)
        
    def row(self, row_index) -> List[int]:
        row = [] 
        for col in range(0, self.sudoku_size):
            row.append(self.get(row_index, col).value)
        return row

    def col(self, col_index) -> List[int]:
        col = []
        for row in range(0, self.sudoku_size):
            col.append(self.get(row, col_index).value)
        return col

    def cell(self, row_index, col_index): 
        row_offset = int(row_index / self.cell_size) * self.cell_size
        col_offset = int(col_index / self.cell_size) * self.cell_size

        cell = []
        for row in range(0, self.cell_size):
            for col in range(0, self.cell_size):
                cell.append(
                    self.get(row_offset + row, col_offset + col).value
                )

        return cell 
    
    def available(self, row_index, col_index):
        res = []
        for maybe in range(1, self.sudoku_size+1):
            if (self._check(row_index, col_index, maybe)):
                res.append(maybe)
        return res 

    def _index(self, row, col) -> int:
        
        if row > (self.sudoku_size - 1) or row < 0: 
            raise IndexError(f"Error: row: {row} out of range")
        if col > (self.sudoku_size - 1) or col < 0: 
            raise IndexError(f"Error: col: {col} out of range")
        
        return (row * self.sudoku_size) + col 

    def _rows(self) -> List[List[int]]:
        rows = []
        for row in range(0, self.sudoku_size):
            collect_row = []
            for col in range(0, self.sudoku_size):
                collect_row.append(self.get(row, col))
            rows.append(collect_row)
        return rows
    
    def _check(self, row_index, col_index, item) -> bool:
        if item == 0:
            return True

        check_row = self.row(row_index)
        check_col = self.col(col_index)
        check_cell = self.cell(row_index, col_index)

        ok = (
            item not in check_row and
            item not in check_col and 
            item not in check_cell
        )
        
        return ok


