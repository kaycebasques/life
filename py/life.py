import pprint
import curses
import time
import sys

class Game:

    def __init__(self, filename):
        self.world = World(filename=filename)

    # def __str__(self):
    #     world = ''
    #     for line in self.world:
    #         for cell in line:
    #             world += 'o' if cell.alive else ' '
    #         world += '\n'
    #     return world

class World:

    def __init__(self, filename=None, previous=None):
        if filename:
            self.world = self._init_from_file(filename)
        else:
            self.world = self._init_from_previous(previous)

    def _init_from_file(self, filename):
        world = []
        with open(filename, 'r') as file:
            lines = file.readlines()
        for row_index, line in enumerate(lines):
            row = []
            for col_index, char in enumerate(line):
                if char == '\n':
                    continue
                alive = True if char == 'o' else False
                row.append(Cell(alive, row_index, col_index))
            world.append(row)
        row_len = len(world) - 1
        col_len = len(world[0]) - 1
        for row in world:
            for cell in row:
                cell.set_neighbors(world, row_len, col_len)
                cell.print_neighbors()
        return world

    def _init_from_previous(self, previous):
        pass

class Cell:

    def __init__(self, alive, row, col):
        self.alive = alive
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

game = Game('init.txt')
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
