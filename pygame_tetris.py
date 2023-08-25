import pygame as pg
import random

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 800
HEIGHT = 21
WIDTH = 11
WALL = "#"
EMPTY = "."
BLOCK = "X"
CELL_SIZE = 35
COLORS = [
    (0, 255, 255),  # Cyan
    (0, 0, 255),    # Blue
    (255, 165, 0),  # Orange
    (255, 255, 0),  # Yellow
    (0, 255, 0),    # Green
    (128, 0, 128),  # Purple
    (255, 0, 0)     # Red
]

# Initialize Pygame
pg.init()

# Rotation function
def rotate(px, py, r):
    mod = r % 4
    if mod == 0: return 4 * py + px
    elif mod == 1: return 12 + py - 4 * px
    elif mod == 2: return 15 - 4 * py - px
    elif mod == 3: return 3 - py + 4 * px
    else: raise ValueError("Something wrong with the Rotation algo")

# Tetromino shapes
tetromino = [
    "..X...X...X...X.",
    "..X..XX...X.....",
    ".....XX..XX.....",
    "..X..XX..X......",
    ".X...XX...X.....",
    ".X...X...XX.....",
    "..X...X..XX....."
]

# Class for the game board
class Board:
    def __init__(self):
        self.board = self.init_board()
        self.x, self.y = self.get_begin_x_y()
        self.color = COLORS[random.randint(0, 6)]
        self.fall_interval = 1000  # milliseconds (adjust as needed)
        self.last_fall_time = pg.time.get_ticks()
        self.rotation = 0
        self.game_over = False
        self.tetris = self.random_tetris(tetromino)

    def init_x_y(self):
        self.color = COLORS[random.randint(0, 6)]
        self.x, self.y = self.get_begin_x_y()
        self.clear_lines()
        self.is_game_over(self.tetris)
        self.log_board()

    def get_begin_x_y(self):
        x = (WIDTH // 2) - 2
        y = -2
        return (x, y)

    def init_board(self):
        board = []
        for _ in range(HEIGHT):
            row = [WALL if i == 0 or i == WIDTH - 1 else EMPTY for i in range(WIDTH)]
            board.append(row)
        board.append([WALL for _ in range(WIDTH)])
        return board

    def is_game_over(self, tetris):
        for y in range(4):
            for x in range(4):
                if tetris[rotate(x, y, self.rotation)] == BLOCK:
                    if self.y + y >= 0 and self.board[self.y + y][self.x + x] != EMPTY:
                        self.game_over = True
                        return

    def valid_move(self, tetris, r, xp, yp):
        if xp < 0 or xp > WIDTH - 4: return False
        if yp < 0: return True
        for y in range(4):
            for x in range(4):
                if tetris[rotate(x, y, r)] == BLOCK and self.board[yp + y][xp + x] != EMPTY:
                    return False
        return True

    def delete_piece(self, tetris):
        for y in range(4):
            for x in range(4):
                if self.y + y >= 0 and tetris[rotate(x, y, self.rotation)] == BLOCK:
                    self.board[self.y + y][self.x + x] = EMPTY

    def spawn_piece(self, tetris):
        for y in range(4):
            for x in range(4):
                if self.y + y >= 0 and tetris[rotate(x, y, self.rotation)] == BLOCK:
                    self.board[self.y + y][self.x + x] = self.color

    def print_board(self, screen):
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                if cell == WALL:
                    pg.draw.rect(screen, (255, 255, 255), (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                elif isinstance(cell, tuple):
                    pg.draw.rect(screen, cell, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                elif cell == EMPTY:
                    pg.draw.rect(screen, (0, 0, 0), (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pg.display.flip()

    def move_down(self):
        self.delete_piece(self.tetris)
        if not self.valid_move(self.tetris, self.rotation, self.x, self.y + 1):
            self.spawn_piece(self.tetris)
            self.tetris = self.random_tetris(tetromino)
            self.init_x_y()
        else:
            self.y += 1
            self.spawn_piece(self.tetris)

    def move_left(self):
        self.delete_piece(self.tetris)
        if self.valid_move(self.tetris, self.rotation, self.x - 1, self.y):
            self.x -= 1
        self.spawn_piece(self.tetris)

    def move_right(self):
        self.delete_piece(self.tetris)
        if self.valid_move(self.tetris, self.rotation, self.x + 1, self.y):
            self.x += 1
        self.spawn_piece(self.tetris)

    def hard_drop(self):
        self.delete_piece(self.tetris)
        while self.valid_move(self.tetris, self.rotation, self.x, self.y + 1):
            self.y += 1
        self.spawn_piece(self.tetris)

    def random_tetris(self, tetris_list):
        return tetris_list[random.randint(0, 6)]

    def update(self):
        current_time = pg.time.get_ticks()
        if current_time - self.last_fall_time >= self.fall_interval:
            self.move_down()
            self.last_fall_time = current_time

    def rotate(self):
        self.delete_piece(self.tetris)
        if self.valid_move(self.tetris, self.rotation + 1, self.x, self.y):
            self.rotation = (self.rotation + 1) % 4
        self.spawn_piece(self.tetris)

    def log_board(self):
        print(f"x= {self.x},  y= {self.y}")
        print('=' * WIDTH)
        print('=' * WIDTH)
        for row in self.board:
            for col in row:
                print(col, end=' ')
            print()

    def clear_lines(self):
        lines_to_clear = []
        for y in range(HEIGHT):
            if all(cell != EMPTY for cell in self.board[y]):
                lines_to_clear.append(y)
        if lines_to_clear:
            for y in lines_to_clear:
                for x in range(1, WIDTH - 1):
                    self.board[y][x] = EMPTY
                for y_above in range(y, 0, -1):
                    self.board[y_above] = self.board[y_above - 1][:]

def main():
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill(pg.Color('black'))
    game_over = False
    board = Board()

    while not game_over:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                game_over = True
                break
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_d:
                    board.move_right()
                if e.key == pg.K_q:
                    board.move_left()
                if e.key == pg.K_z:
                    board.rotate()
                if e.key == pg.K_s:
                    board.move_down()
                if e.key == pg.K_SPACE:
                    board.hard_drop()
                    board.tetris = board.random_tetris(tetromino)
                    board.init_x_y()

        if board.game_over:
            game_over = True
            break

        if pg.time.get_ticks() - board.last_fall_time >= board.fall_interval:
            board.move_down()
            board.last_fall_time = pg.time.get_ticks()

        board.update()
        board.print_board(screen)
        pg.display.flip()

    pg.quit()

if __name__ == "__main__":
    main()
