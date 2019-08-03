class Square():

    def __init__(self):
        self.numMines = 0;
        self.observed = False;

    def __str__(self):
        if self.observed:
            return str(self.numMines % 10 if self.numMines != 'X' else 'X')
        else:
            return ' '

import random
class Board():

    def rowInRange(self, row):
        return 0 <= row < self.size

    def colInRange(self, col):
        return 0 <= col < self.size

    def inRange(self, rowcol):
        return self.rowInRange(rowcol[0]) and self.colInRange(rowcol[1])

    def getAdjs(self, row, col):
        d = [-1, 0, 1]
        return filter(self.inRange, [(row + rd, col + cd) for cd in d for rd in d])

    def countAdjs(self, row, col):
        return len([rowcol for rowcol in self.getAdjs(row, col) if self.board[rowcol[0]][rowcol[1]].numMines == 'X'])

    def findNums(self):
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col].numMines != 'X':
                    self.board[row][col].numMines = self.countAdjs(row, col)

    def __init__(self, size, mines):
        self.size = size
        self.needClear = size * size - mines
        
        mines = random.sample(range(size * size), mines)

        self.board = [[Square() for cols in range(size)] for rows in range(size)]
        for mine in mines:
            self.board[mine // self.size][mine % self.size].numMines = 'X'

        self.findNums()
        
    def printBoard(self):
        print('  ' + '|'.join([str(col % 10) for col in range(self.size)]))
        for row in range(self.size):
            print(str(row % 10) + '|' + '|'.join([str(x) for x in self.board[row]]) + '|')
    

    def dfsObservable(self, row, col, visited):
        queue = [(row, col)]

        while queue:

            r, c = queue.pop()
            visited.add((r, c))
            adjs = self.getAdjs(r,c)

            for r, c in adjs:
                if (r, c) not in visited:
                    visited.add((r, c))
                    self.board[r][c].observed = True
                    if not self.board[r][c].numMines:
                        queue.append((r,c))

    def makeObservable(self, row, col, visited):
        self.board[row][col].observed = True
        visited.add((row, col))
        if not self.board[row][col].numMines:
            self.dfsObservable(row, col, visited)
            
                
import sys
if __name__ == '__main__':

    size = int(sys.argv[1])
    mines = int(sys.argv[2])
    board = Board(size, mines)
    picked = set()

    while True:
        board.printBoard()

        row = -1
        col = -1
        try:
            while not board.rowInRange(row):
                row = int(input('Pick a row '))
            while not board.colInRange(col):
                col = int(input('Pick a col '))
        except ValueError:
            print('Valid input is numeric!')
            continue

        if (row, col) in picked:
            print('Already picked that!')
            continue

        board.makeObservable(row, col, picked)

        if board.board[row][col].numMines == 'X':
            print('GAME OVER!')
            break
        if board.needClear == len(picked):
            print('You WIN!')
            break

    board.printBoard()
