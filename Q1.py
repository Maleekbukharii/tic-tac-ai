import numpy as np
import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 450, 450
LINE_WIDTH = 10
BOARD_ROWS, BOARD_COLS = 3, 3
CELL_SIZE = WIDTH // BOARD_COLS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


class TicTacToe:
    def __init__(self):
        self.board = np.full((3, 3), '-')  # Updated to 3x3
        self.current_player = 'X'
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Tic-Tac-Toe 3x3")
        self.window.fill(WHITE)
        self.draw_grid()

    def draw_grid(self):
        for row in range(1, BOARD_ROWS):
            pygame.draw.line(self.window, BLACK, (0, row * CELL_SIZE), (WIDTH, row * CELL_SIZE), LINE_WIDTH)
        for col in range(1, BOARD_COLS):
            pygame.draw.line(self.window, BLACK, (col * CELL_SIZE, 0), (col * CELL_SIZE, HEIGHT), LINE_WIDTH)
        pygame.display.update()

    def draw_move(self, row, col):
        center_x = col * CELL_SIZE + CELL_SIZE // 2
        center_y = row * CELL_SIZE + CELL_SIZE // 2
        if self.current_player == 'X':
            pygame.draw.line(self.window, RED, (center_x - 50, center_y - 50), (center_x + 50, center_y + 50),
                             LINE_WIDTH)
            pygame.draw.line(self.window, RED, (center_x + 50, center_y - 50), (center_x - 50, center_y + 50),
                             LINE_WIDTH)
        else:
            pygame.draw.circle(self.window, BLACK, (center_x, center_y), 50, LINE_WIDTH)
        pygame.display.update()

    def make_move(self, row, col):
        if self.board[row, col] == '-':
            self.board[row, col] = self.current_player
            self.draw_move(row, col)
            if self.is_winner(self.current_player):
                print(f"{self.current_player} wins!")
                pygame.quit()
                sys.exit()
            elif '-' not in self.board:
                print("It's a draw!")
                pygame.quit()
                sys.exit()
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            if self.current_player == 'O':
                pygame.time.delay(500)
                self.ai_move()

    def is_winner(self, player):
        for row in self.board:
            if all(cell == player for cell in row):
                return True
        for col in range(3):
            if all(self.board[row][col] == player for row in range(3)):
                return True
        if all(self.board[i][i] == player for i in range(3)) or all(self.board[i][2 - i] == player for i in range(3)):
            return True
        return False

    def minimax(self, depth, is_maximizing, alpha, beta):
        if self.is_winner('X'):
            return -10 + depth
        if self.is_winner('O'):
            return 10 - depth
        if '-' not in self.board:
            return 0

        if is_maximizing:
            max_eval = -float('inf')
            for row in range(3):
                for col in range(3):
                    if self.board[row, col] == '-':
                        self.board[row, col] = 'O'
                        eval = self.minimax(depth + 1, False, alpha, beta)
                        self.board[row, col] = '-'
                        max_eval = max(max_eval, eval)
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            break
            return max_eval
        else:
            min_eval = float('inf')
            for row in range(3):
                for col in range(3):
                    if self.board[row, col] == '-':
                        self.board[row, col] = 'X'
                        eval = self.minimax(depth + 1, True, alpha, beta)
                        self.board[row, col] = '-'
                        min_eval = min(min_eval, eval)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break
            return min_eval

    def best_move(self):
        best_val = -float('inf')
        best_move = None
        for row in range(3):
            for col in range(3):
                if self.board[row, col] == '-':
                    self.board[row, col] = 'O'
                    move_val = self.minimax(0, False, -float('inf'), float('inf'))
                    self.board[row, col] = '-'
                    if move_val > best_val:
                        best_val = move_val
                        best_move = (row, col)
        return best_move

    def ai_move(self):
        move = self.best_move()
        if move:
            self.make_move(move[0], move[1])


# Running the game
if __name__ == "__main__":
    game = TicTacToe()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and game.current_player == 'X':
                x, y = event.pos
                row = y // CELL_SIZE
                col = x // CELL_SIZE
                game.make_move(row, col)
    pygame.quit()
