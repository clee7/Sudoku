'''
This program allows the user to interactively play the game of Sudoku.
'''

import sys


class SudokuError(Exception):
    pass


class SudokuMoveError(SudokuError):
    pass


class SudokuCommandError(SudokuError):
    pass


class Sudoku:

    '''Interactively play the game of Sudoku.'''

    def __init__(self):
        board = []
        for i in range(9):
            board.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.board = board
        self.movelst = []
        # TODO

    def load(self, filename):
        with open(filename, 'r') as text_file:
            linecount = 0
            board = []
            for line in text_file:
                line = line.strip('\n')
                row = []
                if len(line) != 9:
                    raise IOError('line must have length of 9.')
                linecount += 1
                for num in line:
                    if int(num) not in range(0, 10):
                        raise IOError('characters in line must be from 0 to 9')
                    row.append(int(num))
                board.append(row)
            if linecount != 9:
                raise IOError('There must be 9 rows')
        self.board = board
        self.movelst = []

        # TODO

    def save(self, filename):
        with open(filename, 'w') as text_file:
            board = self.board
            for i in range(0, 9):
                for char in board[i]:
                    text_file.write(str(char))
                text_file.write('\n')

        # TODO

    def show(self):
        '''Pretty-print the current board representation.'''
        print
        print '   1 2 3 4 5 6 7 8 9 '
        for i in range(9):
            if i % 3 == 0:
                print '  +-----+-----+-----+'
            sys.stdout.write('%d |' % (i + 1))
            for j in range(9):
                if self.board[i][j] == 0:
                    sys.stdout.write(' ')
                else:
                    sys.stdout.write('%d' % self.board[i][j])
                if j % 3 != 2:
                    sys.stdout.write(' ')
                else:
                    sys.stdout.write('|')
            print
        print '  +-----+-----+-----+'
        print

    def move(self, row, col, val):
        if row not in range(1, 10):
            raise SudokuMoveError('Invalid row coordinate.')
        elif col not in range(1, 10):
            raise SudokuMoveError('Invalid column coordinate.')
        elif self.board[row - 1][col - 1] != 0:
            raise SudokuMoveError('Location occupied.')
        elif val in self.board[row - 1]:
            raise SudokuMoveError('Row conflict.')
        for i in range(9):
            if val == self.board[i][col - 1]:
                raise SudokuMoveError('Column conflict.')
        a = (row - 1) / 3
        b = (col - 1) / 3
        for i in range(a * 3, a * 3 + 3):
            for j in range(b * 3, b * 3 + 3):
                if val == self.board[i][j]:
                    raise SudokuMoveError('Box conflict.')
        self.board[row - 1][col - 1] = val
        self.movelst.append((row, col, val))
        # TODO

    def undo(self):
        row, col, val = self.movelst.pop()
        self.board[row - 1][col - 1] = 0
        # TODO

    def solve(self):
        while True:
            try:
                s = raw_input('sudoku >')
                if s == 'q':
                    return
                elif s == 'u':
                    self.undo()
                    self.show()
                elif s == '':
                    raise SudokuCommandError('Invalid command.')
                elif s[0] == 's':
                    lst = s.split()
                    filename = lst[1]
                    self.save(filename)
                elif len(s) == 3:
                    for i in range(3):
                        if s[i] not in '0123456789':
                            raise SudokuCommandError('Invalid command.')
                    self.move(int(s[0]), int(s[1]), int(s[2]))
                    self.show()
                else:
                    raise SudokuCommandError('Invalid command.')
            except SudokuCommandError as e:
                print 'Invalid command:' + str(e) + ' Please try again.'
            except SudokuMoveError as e:
                print 'Invalid move:' + str(e) + ' Please try again.'

if __name__ == '__main__':
    s = Sudoku()

    while True:
        filename = raw_input('Enter the sudoku filename: ')
        try:
            s.load(filename)
            break
        except IOError, e:
            print e
    s.show()
    s.solve()
