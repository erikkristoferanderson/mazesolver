from graphics import Window, Cell
import time
import random


class Maze:
    def __init__(self,
                 x_offset: int, y_offset: int,
                 num_rows: int, num_cols: int,
                 cell_size_x: int, cell_size_y: int,
                 seed: int = None,
                 win: Window = None,
                 frame_delay=0.05):

        self.x1, self.y1 = x_offset, y_offset
        self.num_rows, self.num_cols = num_rows, num_cols  # j, i
        self.cell_size_x, self.cell_size_y = cell_size_x, cell_size_y
        self.window = win
        self.frame_delay = frame_delay

        if seed is not None:
            random.seed(seed)
        self._cells = []
        self._create_cells()
        self._draw_cells()


    def _create_cells(self):
        """
        creates instances of cells row by row and add this to ._cells, also draws the cells
        :return:
        """
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
                        _win=self.window
                    )
                )
            self._cells.append(row)
        for cell in self._cells[0]:
            cell.neighbours.remove("left")
        for cell in self._cells[self.num_cols-1]:
            cell.neighbours.remove("right")
        for column in self._cells:
            column[0].neighbours.remove("top")
            column[self.num_rows-1].neighbours.remove("bottom")

    def _draw_cells(self):
        for row in self._cells:
            for cell in row:
                cell.draw()
                pass
    
    def next_window_frame(self):
        # if a maze has a window update that window every 0.01 seconds
        if self.window:
            self.window.redraw()
            time.sleep(self.frame_delay)
    
    def break_entrance_and_exit(self):
        maze_entrance = self._cells[0][0]
        maze_exit = self._cells[-1][-1]

        maze_entrance.has_top_wall = False
        maze_entrance.draw()
        maze_exit.has_right_wall = False
        maze_exit.draw()
    
    def dfs_maze_generator(self, i, j):
        self.next_window_frame()
        current_cell = self._cells[i][j]
        current_cell.visited = True

        while True:
            unvisited_neighbours = []
            current_neighbours = current_cell.neighbours
            # check: above, below, left then right
            if "top" in current_neighbours and not self._cells[i][j-1].visited:
                unvisited_neighbours.append((i, j-1, "top"))

            if "bottom" in current_neighbours and not self._cells[i][j+1].visited:
                unvisited_neighbours.append((i, j+1, "bottom"))

            if "left" in current_neighbours and not self._cells[i-1][j].visited:
                unvisited_neighbours.append((i-1, j, 'left'))

            if "right" in current_neighbours and not self._cells[i+1][j].visited:
                unvisited_neighbours.append((i+1, j, 'right'))

            no_more_neighbours_to_vist = len(unvisited_neighbours) == 0
            if no_more_neighbours_to_vist:
                current_cell.draw()
                return

            else:
                to_visit = random.choice(unvisited_neighbours)
                next_column, next_row, next_direction = to_visit
                next_cell = self._cells[next_column][next_row]
                # knock down the walls between current cell and cell to visit
                if next_direction == 'top':
                    current_cell.has_top_wall = False
                    next_cell.has_bottom_wall = False
                elif next_direction == 'bottom':
                    current_cell.has_bottom_wall = False
                    next_cell.has_top_wall = False
                elif next_direction == 'left':
                    current_cell.has_left_wall = False
                    next_cell.has_right_wall = False
                elif next_direction == 'right':
                    current_cell.has_right_wall = False
                    next_cell.has_left_wall = False
                current_cell.draw()
                next_cell.draw()
                # recursive call
                self.dfs_maze_generator(next_column, next_row)
    
    def reset_cells_visited(self):
        for column in self._cells:
            for cell in column:
                cell.visited = False
    
    def solve(self, algorithm="depth first search"):
        self.window.algorithm_label.configure(text=algorithm)
        if algorithm == "depth first search":
            return self.dfs_solver(0, 0)
        elif algorithm == "right hand rule":
            return self.right_hand_rule()
        elif algorithm == "breadth first search":
            return self.breadth_first_search()

    def dfs_solver(self, i, j):
        self.next_window_frame()
        current_cell = self._cells[i][j]
        current_cell.visited = True

        at_exit = i == self.num_cols - 1 and j == self.num_rows - 1
        if at_exit:
            print('solved')
            return True

        if "right" in current_cell.neighbours and not current_cell.has_right_wall:
            potential_cell = self._cells[i+1][j]
            if not potential_cell.visited and not potential_cell.has_left_wall:
                current_cell.draw_move(potential_cell)
                if self.dfs_solver(i+1, j):
                    return True
                else:
                    potential_cell.draw_move(current_cell, undo=True)

        if "left" in current_cell.neighbours and not current_cell.has_left_wall:
            potential_cell = self._cells[i-1][j]
            if not potential_cell.visited and not potential_cell.has_right_wall:
                current_cell.draw_move(potential_cell)
                if self.dfs_solver(i-1, j):
                    return True
                else:
                    potential_cell.draw_move(current_cell, undo=True)

        if "top" in current_cell.neighbours and not current_cell.has_top_wall:
            potential_cell = self._cells[i][j-1]
            if not potential_cell.visited and not potential_cell.has_bottom_wall:
                current_cell.draw_move(potential_cell)
                if self.dfs_solver(i, j-1):
                    return True
                else:
                    potential_cell.draw_move(current_cell, undo=True)

        if "bottom" in current_cell.neighbours and not current_cell.has_bottom_wall:
            potential_cell = self._cells[i][j+1]
            if not potential_cell.visited and not potential_cell.has_top_wall:
                current_cell.draw_move(potential_cell)
                if self.dfs_solver(i, j+1):
                    return True
                else:
                    potential_cell.draw_move(current_cell, undo=True)

        return False

    def right_hand_rule(self):
        i, j = 0, 0
        current_direction = "south"
        while True:
            self.next_window_frame()
            current_cell = self._cells[i][j]

            at_exit = i == self.num_cols - 1 and j == self.num_rows - 1
            if at_exit:
                print('solved')
                break

            if current_direction == "south":
                if not current_cell.has_left_wall:
                    i += -1
                    current_direction = "west"
                    current_cell.draw_move(self._cells[i][j])
                    continue
                elif current_cell.has_bottom_wall:
                    current_direction = "east"
                else:
                    j += 1
                    current_direction = "south"
                    current_cell.draw_move(self._cells[i][j])
                    continue

            if current_direction == "east":
                if not current_cell.has_bottom_wall:
                    j += 1
                    current_direction = "south"
                    current_cell.draw_move(self._cells[i][j])
                    continue
                elif current_cell.has_right_wall:
                    current_direction = "north"
                else:
                    i += 1
                    current_direction = "east"
                    current_cell.draw_move(self._cells[i][j])
                    continue

            if current_direction == "north":
                if not current_cell.has_right_wall:
                    i += 1
                    current_direction = "east"
                    current_cell.draw_move(self._cells[i][j])
                    continue
                elif current_cell.has_top_wall:
                    current_direction = "west"
                else:
                    j += -1
                    current_direction = "north"
                    current_cell.draw_move(self._cells[i][j])
                    continue

            if current_direction == "west":
                if not current_cell.has_top_wall:
                    j += -1
                    current_direction = "north"
                    current_cell.draw_move(self._cells[i][j])
                    continue
                elif current_cell.has_left_wall:
                    current_direction = "south"
                else:
                    i += -1
                    current_direction = "west"
                    current_cell.draw_move(self._cells[i][j])
                    continue

    def breadth_first_search(self):
        self.next_window_frame()
        i, j = 0, 0
        current_cell = self._cells[i][j]
        current_cell.visited = True
        queue = []
        for column in self._cells:
            for cell in column:
                cell.path_history = []
        current_cell.path_history.append((0, 0))
        while True:
            self.next_window_frame()
            if (i, j) == (self.num_cols - 1, self.num_rows - 1):
                print("solved")
                break

            if "top" in current_cell.neighbours:
                top_cell = self._cells[i][j-1]
                if not current_cell.has_top_wall and not top_cell.visited:
                    current_cell.draw_move(top_cell, undo=True)
                    top_cell.path_history = [k for k in current_cell.path_history]
                    queue.insert(0, (i, j-1))

            if "left" in current_cell.neighbours:
                left_cell = self._cells[i-1][j]
                if not current_cell.has_left_wall and not left_cell.visited:
                    current_cell.draw_move(left_cell, undo=True)
                    left_cell.path_history = [k for k in current_cell.path_history]
                    queue.insert(0, (i-1, j))

            if "bottom" in current_cell.neighbours:
                bottom_cell = self._cells[i][j + 1]
                if not current_cell.has_bottom_wall and not bottom_cell.visited:
                    current_cell.draw_move(bottom_cell, undo=True)
                    bottom_cell.path_history = [k for k in current_cell.path_history]
                    queue.insert(0, (i, j+1))

            if "right" in current_cell.neighbours:
                right_cell = self._cells[i + 1][j]
                if not current_cell.has_right_wall and not right_cell.visited:
                    current_cell.draw_move(right_cell, undo=True)
                    right_cell.path_history = [k for k in current_cell.path_history]
                    queue.insert(0, (i+1, j))

            i, j = queue.pop()
            current_cell = self._cells[i][j]
            current_cell.visited = True
            current_cell.path_history.append((i, j))
        history = self._cells[self.num_cols - 1][self.num_rows - 1].path_history
        last_pair = 0, 0
        for i in history:
            self.next_window_frame()
            column1, row1 = last_pair
            column2, row2 = i
            current_cell = self._cells[column1][row1]
            next_cell = self._cells[column2][row2]
            current_cell.draw_move(next_cell)
            last_pair = i









