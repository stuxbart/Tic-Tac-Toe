import pygame

WINDOW_SIZE = (500, 600)
FIELD_SIZE = (int(WINDOW_SIZE[0]/3), int(WINDOW_SIZE[0]/3))
BOTTOM_BAR_HEIGHT = WINDOW_SIZE[1] - WINDOW_SIZE[0]
BOTTOM_BAR_FONT_SIZE = int(BOTTOM_BAR_HEIGHT/2)

pygame.init()
pygame.font.init()

X_PLAYER_IMG = pygame.image.load("./img/x_player.png")
X_PLAYER_IMG = pygame.transform.smoothscale(X_PLAYER_IMG, FIELD_SIZE)
O_PLAYER_IMG = pygame.image.load("./img/o_player.png")
O_PLAYER_IMG = pygame.transform.smoothscale(O_PLAYER_IMG, FIELD_SIZE)


class Field:
    def __init__(self, x, y, w, h):
        self.mark = ''
        self.used = False
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def check_clicked(self, x, y, mark):

        if self.x < x < self.x + self.w and self.y < y < self.y + self.h:
            if not self.used:
                self.mark = mark
                self.used = True
                return 1
            else:
                return -1
        return 0

    def draw(self, window):
        if self.mark == 'x':
            window.blit(X_PLAYER_IMG, (self.x, self.y, self.w, self.h))
        elif self.mark == 'o':
            window.blit(O_PLAYER_IMG, (self.x, self.y, self.w, self.h))

    def reset(self):
        self.mark = ''
        self.used = False


class Board:
    def __init__(self, width, height):
        self.field_width = int(width / 3)
        self.field_height = int(height / 3)
        self.fields = [
            [Field(x * self.field_width, y * self.field_height, self.field_width, self.field_height)
             for x in range(3)] for y in range(3)]

    def clicked(self, x, y, mark):
        for row in self.fields:
            for f in row:
                res = f.check_clicked(x, y, mark)
                if res == 1:
                    return 1
                elif res == 0:
                    pass
                elif res == -1:
                    return -1
        return 0

    def check_win(self):

        for i in range(3):
            if self.fields[i][0].mark == self.fields[i][1].mark == self.fields[i][2].mark != '':
                return self.fields[i][0].mark

        for i in range(3):
            if self.fields[0][i].mark == self.fields[1][i].mark == self.fields[2][i].mark != '':
                return self.fields[0][i].mark

        if self.fields[0][0].mark == self.fields[1][1].mark == self.fields[2][2].mark != '':
            return self.fields[0][0].mark

        if self.fields[2][0].mark == self.fields[1][1].mark == self.fields[0][2].mark != '':
            return self.fields[2][0].mark

        all_used = True
        for row in self.fields:
            for f in row:
                if not f.used:
                    all_used = f.used
        if all_used:
            return 'd'

        return ''

    def draw(self, window):
        self.draw_grid(window)
        for row in self.fields:
            for f in row:
                f.draw(window)

    def draw_grid(self, window):
        for i in range(2):
            x = self.field_width * (1 + i)
            y1 = 0
            y2 = self.field_height * 3
            pygame.draw.line(window, (0, 0, 0), (x, y1), (x, y2), 5)

        for i in range(2):
            y = self.field_width * (1 + i)
            x1 = 0
            x2 = self.field_height * 3
            pygame.draw.line(window, (0, 0, 0), (x1, y), (x2, y), 5)

    def reset(self):
        for row in self.fields:
            for f in row:
                f.reset()


class BottomInfoBar:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.current_state = ''

        self.font = pygame.font.SysFont("Arial", BOTTOM_BAR_FONT_SIZE)
        self.surface = None
        self.text_pos = []

    def update(self):
        t_width, t_height = self.font.size(self.current_state)
        x = self.x + self.w / 2 - t_width / 2
        y = self.y + self.h / 2 - t_height / 2
        self.text_pos = (int(x), int(y))
        self.surface = self.font.render(self.current_state, True, (0, 0, 0))

    def player_turn(self, mark):
        self.current_state = mark.upper() + ' Turn'
        self.update()

    def player_win(self, mark):
        self.current_state = mark.upper() + " Win"
        self.update()

    def print_draw(self):
        self.current_state = "Draw"
        self.update()

    def draw(self, window):
        if self.surface:
            window.blit(self.surface, self.text_pos)


class Window:
    def __init__(self):
        self.width = WINDOW_SIZE[0]
        self.height = WINDOW_SIZE[1]
        self.bottom_bar_height = BOTTOM_BAR_HEIGHT

        self.win = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Tic Tac Toe")

        self.board = Board(self.width, self.height - self.bottom_bar_height)

        self.bottom_info_bar = BottomInfoBar(0, self.height - self.bottom_bar_height,
                                             self.width, self.bottom_bar_height)

        self.running = True

        self.players = ['x', 'o']
        self.current_turn = 0
        self.lock_board = False
        self.bottom_info_bar.player_turn(self.players[self.current_turn])

    def run(self):

        while self.running:
            self.check_input()
            self.draw()
            pygame.display.update()

    def check_input(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                result = self.board.clicked(x, y, self.players[self.current_turn])

                if self.lock_board:
                    self.reset_game()
                    self.lock_board = False
                    self.bottom_info_bar.player_turn(self.players[self.current_turn])
                else:
                    if result == 1:

                        if self.current_turn == 0:
                            self.current_turn = 1
                            self.bottom_info_bar.player_turn(self.players[self.current_turn])
                        elif self.current_turn == 1:
                            self.current_turn = 0
                            self.bottom_info_bar.player_turn(self.players[self.current_turn])

                        res = self.board.check_win()

                        if res == self.players[0]:
                            self.bottom_info_bar.player_win(self.players[0])
                            self.lock_board = True

                        elif res == self.players[1]:
                            self.bottom_info_bar.player_win(self.players[1])
                            self.lock_board = True

                        elif res == 'd':
                            self.bottom_info_bar.print_draw()
                            self.lock_board = True

                    elif result == 0:
                        pass
                    elif result == -1:
                        pass

    def draw(self):
        self.win.fill((250, 250, 250))
        self.board.draw(self.win)
        self.bottom_info_bar.draw(self.win)

    def reset_game(self):
        self.board.reset()


def main():
    window = Window()
    window.run()


if __name__ == "__main__":
    main()
