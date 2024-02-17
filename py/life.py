import pprint
import curses
import time
import sys

class Game:

    def __init__(self, filename):
        self.world = World(filename=filename)

    def iterate(self):
        self.world.iterate()

    def __str__(self):
        return self.world.__str__()

class World:

    def __init__(self, filename=None, previous=None):
        if filename:
            self.cells = self._init_from_file(filename)
        else:
            self.cells = self._init_from_previous(previous)

    def _init_from_file(self, filename):
        cells = []
        with open(filename, 'r') as file:
            lines = file.readlines()
        for row_index, line in enumerate(lines):
            row = []
            for col_index, char in enumerate(line):
                if char == '\n':
                    continue
                alive = True if char == 'o' else False
                row.append(Cell(alive, row_index, col_index))
            cells.append(row)
        row_len = len(cells) - 1
        col_len = len(cells[0]) - 1
        for row in cells:
            for cell in row:
                cell.set_neighbors(cells, row_len, col_len)
                # cell.print_neighbors()
        return cells

    def _init_from_previous(self, previous):
        pass

    def iterate(self):
        for row in self.cells:
            for cell in row:
                cell.iterate()

    def __str__(self):
        current_iteration = len(self.cells[0][0].alive) - 1
        msg = f'iteration {current_iteration}\n'
        for row in self.cells:
            for cell in row:
                msg += 'o' if cell.alive[current_iteration] else '.'
            msg += '\n'
        msg += '\n'
        return msg
 

class Cell:

    def __init__(self, alive, row, col):
        self.alive = [alive]
        self.row = row
        self.col = col
        self.neighbors = []

    def set_neighbors(self, world, row_len, col_len):
        if self.row-1 >= 0:
            if self.col-1 >= 0:
                self.neighbors.append(world[self.row-1][self.col-1])
            self.neighbors.append(world[self.row-1][self.col])
            if self.col+1 <= col_len:
                self.neighbors.append(world[self.row-1][self.col+1])
        if self.col-1 >= 0:
            self.neighbors.append(world[self.row][self.col-1])
        if self.col+1 <= col_len:
            self.neighbors.append(world[self.row][self.col+1])
        if self.row+1 <= row_len:
            if self.col-1 >= 0:
                self.neighbors.append(world[self.row+1][self.col-1])
            self.neighbors.append(world[self.row+1][self.col])
            if self.col+1 <= col_len:
                self.neighbors.append(world[self.row+1][self.col+1])

    def print_neighbors(self):
        print(f'self: {self.row} {self.col}')
        for index, neighbor in enumerate(self.neighbors):
            print(f'neighbor {index}: {neighbor.row} {neighbor.col}')
        print()

    def iterate(self):
        alive_neighbors = 0
        next_alive = False
        current_iteration = len(self.alive) - 1
        current_alive = self.alive[current_iteration]
        for neighbor in self.neighbors:
            if neighbor.alive[current_iteration]:
                alive_neighbors += 1
        if alive_neighbors <= 1:
            next_alive = False
        elif (alive_neighbors == 2 or alive_neighbors == 3) and current_alive:
            next_alive = True
        elif alive_neighbors == 3 and not current_alive:
            next_alive = True
        else:  # 4+ neighbors
            next_alive = False
        self.alive.append(next_alive)

game = Game('init.txt')
print(game)
for i in range(5):
    game.iterate()
    print(game)

# stdscr = curses.initscr()
# 
# for index, line in enumerate(lines):
#     stdscr.addstr(index, 0, line)
# 
# stdscr.refresh()
# time.sleep(3)
# 
# curses.endwin()
# 
# 0 or 1 neighbors = death by underpopulation
# 2 or 3 neighbors = OK
# 4 or more neighbors = death by overpopulation
#
# A dead cell with exactly 3 neighbors becomes alive by reproduction
