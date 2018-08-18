""" 
@author: Anuj Kumar
@email: cdac.anuj@gmail.com
@date: 
"""

from time import sleep

import pygame

from puzzle.Button import Button
from puzzle.tic_tac_toe import TicTacToe


class PlayGround:
    def __init__(self):
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        pygame.init()
        pygame.font.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((600, 600))
        pygame.display.set_caption('### TIC TAC TOE ###')
        self.screen.fill(self.black)

        pygame.display.update()
        self.sign = "X"
        self.tiles = []
        self.puzzle = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.empty = [i for i in range(0, 9) if self.puzzle[i] == 0]
        self.msg = "Your Turn"

    def tic_tac_toe(self):
        self.finish = False
        self.display_msg(self.msg)

        while not self.finish:

            tic_tac_toe = TicTacToe(self.puzzle)
            if tic_tac_toe.is_win(self.puzzle, 1) or tic_tac_toe.is_win(self.puzzle, 2):
                if tic_tac_toe.is_win(self.puzzle, 1):
                    self.display_msg("Computer Wins", (255, 0, 0))
                else:
                    self.display_msg("You Win", (0, 255, 0))
                sleep(3)
                self.puzzle = [0, 0, 0, 0, 0, 0, 0, 0, 0]
                self.empty = [i for i in range(0, 9) if self.puzzle[i] == 0]
                self.msg = "Your Turn"

            self.display_msg(self.msg)

            for event in pygame.event.get():

                pos = pygame.mouse.get_pos()
                row = ((pos[1] - 10) / 100) - 1
                col = ((pos[0] - 10) / 100) - 1

                if event.type == pygame.QUIT:
                    self.finish = True

                if pos[0] >= 110 and pos[0] <= 410 and pos[1] >= 110 and pos[1] <= 410:

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        c_row = ((pos[1] - 10) / 100) - 1
                        c_col = ((pos[0] - 10) / 100) - 1
                        c_index = (c_row * 3 + c_col)

                        if c_index in self.empty and self.puzzle[c_index] == 0:
                            self.tiles[c_index].text = self.sign
                            self.tiles[c_index].color = self.black
                            self.tiles[c_index].draw()
                            self.empty.remove(c_index)

                            if self.sign == "X":
                                self.sign = "O"
                                self.msg = "Computer's Turn"
                                self.puzzle[c_index] = 2
                                self.display_msg(self.msg)
            if 0 not in self.puzzle:
                self.display_msg("!!! DRAW !!!", (0, 255, 0))
                sleep(2)
                self.puzzle = [0, 0, 0, 0, 0, 0, 0, 0, 0]
                self.empty = [i for i in range(0, 9) if self.puzzle[i] == 0]
                self.msg = "Your Turn"
                self.sign = "X"
            else:
                if self.sign == "O":
                    self.sign = "X"
                    self.display_msg(self.msg)
                    self.puzzle = tic_tac_toe.best_move()
                    self.msg = "Your Turn"
            pygame.display.update()
            self.clock.tick(30)

    def draw_board(self):
        # Boundries
        pygame.draw.line(self.screen, self.white, [200, 100], [200, 400], 3)
        pygame.draw.line(self.screen, self.white, [300, 100], [300, 400], 3)
        pygame.draw.line(self.screen, self.white, [100, 200], [400, 200], 3)
        pygame.draw.line(self.screen, self.white, [100, 300], [400, 300], 3)

        for row in range(1, 4):
            for col in range(1, 4):
                tile = Button(self.screen, self.black, self.black, 100 * col + 10, 100 * row + 10, 80, 80, "")
                self.tiles.append(tile)

        for p, t in zip(self.puzzle, self.tiles):
            if p == 1:
                t.text = "O"
                t.color = self.black
                t.text_color = (255, 0, 0)
                t.draw()
            elif p == 2:
                t.text = "X"
                t.color = self.black
                t.text_color = (0, 255, 0)
            else:
                t.text = ""
            t.draw()

    def display_msg(self, msg, color=(255, 255, 255)):
        font = pygame.font.SysFont('Segoe Script', 40)
        text = font.render(msg, 1, color)
        self.screen.fill(self.black)
        self.draw_board()
        self.screen.blit(text, (100, 450))
        pygame.display.update()
        self.clock.tick(30)


if __name__ == '__main__':
    PlayGround().tic_tac_toe()
