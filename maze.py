from graphics import Window, Cell

class Maze:
    def __init__(
        self,
        x1: int,
        y1: int,
        num_rows: int,
        num_cols: int,
        cell_size_x: int,
        cell_size_y: int,
        win: Window,
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win

        self._cells = []
        self._create_cells()
    
    def _create_cells(self):
        for column_number in range(self.num_cols):
            row = []
            for row_number in range(self.num_rows):
                
                row.append(
                    Cell(
                        self.x1 + column_number * self.cell_size_x,
                        self.x1 + (column_number + 1) * self.cell_size_x,
                        self.y1 + row_number * self.cell_size_y,
                        self.y1 + (row_number + 1) * self.cell_size_y,
                        self.win
                    )
                )
            self._cells.append(row)

        for row in self._cells:
            for cell in row:
                cell.draw()