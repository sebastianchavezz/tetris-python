import random
import os

WIDTH = 12
HEIGHT = 21
EMPTY = '.'


def rotate(px, py, r):
    mod = r % 4
    if mod == 0: return 4*py + px
    elif mod == 1: return 12 + py - 4*px
    elif mod == 2 : return 15 - 4*py - px
    elif mod == 3: return 3 - py + 4*px
    else : raise ValueError("Something wrong")

class Board:
    def __init__(self) -> None:
        self.board = self.init_board()
        self.startX = (WIDTH // 2)-2  
        self.startY = 0
        self.rotation = 3
        self.score = 0

    def init_board(self, col=WIDTH, row=HEIGHT, char=EMPTY):
        x = []
        for j in range(HEIGHT):
            y = []
            for i in range(WIDTH):
                if i == 0 or i == WIDTH-1: y.append("#")
                else: y.append(EMPTY)
            x.append(y)
        x.append(["#" for _ in range(WIDTH)])
        return x
    
    def doesItFit(self, tetromino, nRotation, nPosx, nPosy):
        for py in range(4):
            for px in range(4):
                pi = rotate(px, py, nRotation)
                if tetromino[pi] == 'X'and self.board[nPosy+py][nPosx+px] is not EMPTY: return False
        return True

    def spawn_tremino(self, tetris):
        maxY = self.startY
        for y in range(4):
            for x in range(4):
                pi = rotate(x, y, self.rotation)
                if tetris[pi] == 'X':
                    maxY = max(maxY, self.startY + y)
                    board_x = self.startX + x
                    if board_x >= 0 and board_x < WIDTH: self.board[self.startY + y][board_x] = tetris[pi]

        for y in range(self.startY, maxY + 1):
            if y < HEIGHT - 1: self.board[y][-1] = "#"

    def update_screen(self):
        for row in range(4):
            for col in range(4):
                x = col + self.startX
                y = row + self.startY
                if x > 0 and x < WIDTH -1: self.board[y][x] = EMPTY
                else: self.board[y][x] = "#"

    def move_right(self, tetris):
        self.update_screen()
        if self.doesItFit(tetris, self.rotation, self.startX + 1, self.startY):
            self.startX += 1
        self.spawn_tremino(tetris)

    def move_left(self, tetris):
        self.update_screen()
        if self.doesItFit(tetris, self.rotation, self.startX - 1, self.startY):
            self.startX -= 1
        self.spawn_tremino(tetris)

    def rotate(self, tetris):
        self.update_screen()
        if self.doesItFit(tetris, self.rotation + 1, self.startX, self.startY):
            print(self.startX)
            self.rotation = (self.rotation + 1) % 4
        self.spawn_tremino(tetris)

    def clear_lines(self):
        lines_to_clear = []
        for y in range(HEIGHT):
            if all(cell != EMPTY for cell in self.board[y]):
                lines_to_clear.append(y)
        if lines_to_clear:
            num_lines_cleared = len(lines_to_clear)
            self.score += num_lines_cleared * 100 * (num_lines_cleared + 1) // 2
            for y in lines_to_clear:
                for x in range(1, WIDTH - 1):
                    self.board[y][x] = EMPTY

                for y_above in range(y, 0, -1):
                    self.board[y_above] = self.board[y_above - 1][:]
        else: self.score += 2

    def print_board(self):
        os.system("clear")
        print("======= Tetris =======")
        for row in self.board:
            print("#", end=" ")
            for col in row[1:-1]:
                if col == EMPTY:
                    print(".", end=" ")
                else:
                    print(col, end=" ")
            print("#")
        print("======== Score: =======")
        print("#", end="")
        score_str = str(self.score).center(WIDTH - 6)  # Adjusted width
        print(score_str, end="")
        print("#")
        print("====== Controls ======")
        print("  q - Move Left")
        print("  d - Move Right")
        print("  r - Rotate")
        print("  s - Hard Drop")
        print("score:", self.score)
        print("input z-q-d-r-s-space:")
    
    def hard_drop(self, tetris):
        self.update_screen()
        newY = self.startY
        while self.doesItFit(tetris, self.rotation, self.startX, newY + 1):
            newY += 1
        self.startY = newY
        self.spawn_tremino(tetris)
        self.startX = (WIDTH // 2) - 2  # Reset tetromino starting X coordinate
        self.startY = 0  # Reset tetromino starting Y coordinate
        self.rotation = 3  # Reset tetromino rotation
        self.clear_lines()

def main():
    game = True
    tetromino = []
    tetromino.append("..X...X...X...X.")
    tetromino.append("..X..XX...X.....")
    tetromino.append(".....XX..XX.....")
    tetromino.append("..X..XX..X......")
    tetromino.append(".X...XX...X.....") 
    tetromino.append(".X...X...XX.....")
    tetromino.append("..X...X..XX.....")
    board = Board()

    while game:
        random_number = random.randint(0, 6)  # Generate a new random tetromino
        tetris = tetromino[random_number]
        board.spawn_tremino(tetris)
        board.print_board()
        
        while True:
            user_input = input("input z-r-d-s: ")
            if user_input == "q": board.move_left(tetris)
            elif user_input == "d": board.move_right(tetris)
            elif user_input == "r": board.rotate(tetris)
            elif user_input == "s":
                board.hard_drop(tetris)
                if not board.doesItFit(tetris, board.rotation, board.startX, board.startY):
                    print("Game Over! Your score:", board.score)
                    game = False  # Set the game to end
                break  # Break out of the inner loop to generate a new tetromino
            board.print_board()

if __name__ == '__main__':
    main()