import random

class Cell:
    """
    Represents a single cell in the Minesweeper game.
    """
    def __init__(self, x: int, y: int):
        self.x, self.y = x, y
        self.is_mine = False
        self.is_opened = False
        self.is_flagged = 0
        self.adjacent_mines = 0

class Board:
    """
    Represents the Minesweeper game board.
    """
    def __init__(self, rows: int, cols: int, num_mines: int):
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines
        self.cells = [[Cell(x, y) for y in range(cols)] for x in range(rows)]
    def place_mines(self):
        """
        Randomly places mines on the board.
        """
        mine_positions = random.sample(range(self.rows * self.cols), self.num_mines)
        for pos in mine_positions:
            row = pos // self.cols
            col = pos % self.cols
            self.cells[row][col].is_mine = True
    def calculate_adjacent_mines(self):
        """
        Calculates the number of adjacent mines for each cell.
        """
        for row in range(self.rows):
            for col in range(self.cols):
                if self.cells[row][col].is_mine:
                    continue
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if 0 <= row + i < self.rows and 0 <= col + j < self.cols:
                            if self.cells[row + i][col + j].is_mine:
                                self.cells[row][col].adjacent_mines += 1
    def open_cell(self, row: int, col: int):
        """
        Opens a cell and returns the status:
        -1: already opened
        -2: flagged
        0: safe cell opened
        1: mine opened
        2: empty cell opened (no adjacent mines)
        """
        if self.cells[row][col].is_opened:
            return -1
        if self.cells[row][col].is_flagged > 0:
            return -2
        self.cells[row][col].is_opened = True
        if self.cells[row][col].is_mine:
            return 1
        if self.cells[row][col].adjacent_mines == 0:
            return 2
        return 0
    def flag_cell(self, row: int, col: int):
        """
        Flags a cell and returns the status:
        -1: already opened
        0: unflagged
        1: flagged
        2: question mark (flagged twice)
        3: unflagged (reset to 0)
        """
        if self.cells[row][col].is_opened:
            return -1
        self.cells[row][col].is_flagged += 1
        if self.cells[row][col].is_flagged > 2:
            self.cells[row][col].is_flagged = 0
        return self.cells[row][col].is_flagged

class Game:
    """
    Represents the Minesweeper game logic and flow.
    """
    def __init__(self, rows: int, cols: int, num_mines: int):
        self.board = Board(rows, cols, num_mines)
        self.board.place_mines()
        self.board.calculate_adjacent_mines()
        self.is_game_over = False
        self.is_won = False
    def open_cell(self, row: int, col: int):
        """
        Handles the logic for opening a cell.
        """
        result = self.board.open_cell(row, col)
        if result == 1:
            self.is_game_over = True
            return 2
        elif result == 2:
            self._open_adjacent_cells(row, col)
            return 1
        if self._check_win_condition():
            self.is_game_over = True
            self.is_won = True
            return 3
        return result
    def flag_cell(self, row: int, col: int):
        """
        Handles the logic for flagging a cell.
        """
        status = self.board.flag_cell(row, col)
        return status
    def _open_adjacent_cells(self, row: int, col: int):
        """
        Recursively opens adjacent cells if they are empty.
        """
        for i in range(-1, 2):
            for j in range(-1, 2):
                new_row, new_col = row + i, col + j
                if 0 <= new_row < self.board.rows and 0 <= new_col < self.board.cols:
                    if not self.board.cells[new_row][new_col].is_opened and not self.board.cells[new_row][new_col].is_mine:
                        self.board.open_cell(new_row, new_col)
                        if self.board.cells[new_row][new_col].adjacent_mines == 0:
                            self._open_adjacent_cells(new_row, new_col)
    def _check_win_condition(self):
        """
        Checks if the game meets the win condition.

        Win condition:
        1. All non-mine cells have been opened.
        2. All mine cells are correctly flagged (is_flagged == 1).

        Returns:
            bool: True if the win condition is met, False otherwise.
        """
        for row in self.board.cells:
            for cell in row:
                if not cell.is_mine and not cell.is_opened:
                    return False
                if cell.is_mine and (cell.is_flagged != 1):
                    return False
        return True
