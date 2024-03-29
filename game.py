import random

class Game:
  def __init__(self, rows, cols):
    self.rows = rows
    self.cols = cols
    self.grid = [[0 for x in range(cols)] for y in range(rows)]
    self.final_turn = rows * cols

  def guess_next_move(self):
    found = False
    while not found:
      row = random.randrange(self.rows)
      col = random.randrange(self.cols)
      if self.grid[row][col] == 0:
        found = True
        self.grid[row][col] = 1
    return row, col

  def first_action(self):
    self.turn = 1
    row, col = self.guess_next_move()
    return 1, row, col

  def take_action(self, turn_s):
    self.turn = int(turn_s)
    row = ""
    col = ""

    if self.turn <= self.final_turn:
      row, col = self.guess_next_move()

    return str(self.turn).zfill(3), row, col

  def opponent_action(self, row, col):
    self.grid[int(row)-1][int(col)-1] = 1
