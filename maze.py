from graphics import Window, Cell
import time
import random

class Maze:
    def __init__(
        self,
        x1: int,
        y1: int,
        num_rows: int,
        num_cols: int,
        cell_size_x: int,
        cell_size_y: int,
        seed: int = None,
        win: Window = None,
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows  # j
        self.num_cols = num_cols  # i
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win

        if seed is not None:
            random.seed(seed)
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
                        visited=False,
                        _win=self.win
                    )
                )
            self._cells.append(row)

        for row in self._cells:
            for cell in row:
                cell.draw()
                pass

    def _draw_cell(self, i, j):
        self._cells[i][j].draw()
        self._animate()
    
    def _animate(self):
        self.win.redraw()
        time.sleep(0.1)
    
    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._cells[0][0].draw()
        self._cells[-1][-1].has_right_wall = False
        self._cells[-1][-1].draw()
    
    def _break_walls_r(self, i, j):
        time.sleep(0.1)
        self._cells[i][j].visited = True
        loop_counter = 0
        while True:
            # print('loop counter:', loop_counter)
            loop_counter += 1
            # to_visit = []
            possible_to_visit = []
            # check above
            check_i = i
            check_j = j - 1
            if (check_i >= 0 
                and check_i <= self.num_cols - 1
                and check_j >= 0
                and check_j <= self.num_rows - 1
                and self._cells[check_i][check_j].visited == False
            ): 
                possible_to_visit.append((check_i, check_j, 'above'))
            # check below
            check_i = i
            check_j = j + 1
            # print('check_i', check_i, "check_j", check_j, 'self.num_rows', self.num_rows)
            
            if (check_i >= 0 
                and check_i <= self.num_cols - 1
                and check_j >= 0
                and check_j <= self.num_rows - 1
                and self._cells[check_i][check_j].visited == False
            ): 
                possible_to_visit.append((check_i, check_j, 'below'))
            # check left
            check_i = i - 1
            check_j = j
            if (check_i >= 0 
                and check_i <= self.num_cols - 1
                and check_j >= 0
                and check_j <= self.num_rows - 1
                and self._cells[check_i][check_j].visited == False
            ): 
                possible_to_visit.append((check_i, check_j, 'left'))
            # check right
            check_i = i + 1
            check_j = j
            if (check_i >= 0 
                and check_i <= self.num_cols - 1
                and check_j >= 0
                and check_j <= self.num_rows - 1
                and self._cells[check_i][check_j].visited == False
            ): 
                possible_to_visit.append((check_i, check_j, 'right'))
            # base case
            if len(possible_to_visit) == 0:
                # print('sanity check 9257887594')
                self._cells[i][j].draw()
                self.win.redraw()
                return
            else:
                # print('possible to visit', possible_to_visit)
                to_visit = random.choice(possible_to_visit)
                # knock down the walls between current cell and cell to visit
                if to_visit[2] == 'above':
                    self._cells[i][j].has_top_wall = False
                    self._cells[to_visit[0]][to_visit[1]].has_bottom_wall = False
                elif to_visit[2] == 'below':
                    self._cells[i][j].has_bottom_wall = False
                    self._cells[to_visit[0]][to_visit[1]].has_top_wall = False
                elif to_visit[2] == 'left':
                    self._cells[i][j].has_left_wall = False
                    self._cells[to_visit[0]][to_visit[1]].has_right_wall = False
                elif to_visit[2] == 'right':
                    self._cells[i][j].has_right_wall = False
                    self._cells[to_visit[0]][to_visit[1]].has_left_wall = False
                self._cells[i][j].draw()
                self._cells[to_visit[0]][to_visit[1]].draw()
                self.win.redraw()
                # recursive call
                self._break_walls_r(to_visit[0], to_visit[1])