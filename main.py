import pygame
import random
from math import log10, floor
import seaborn as sns


class Board:
    def __init__(self, width):
        self.width = width
        self.board = [[None] * width for _ in range(width)]
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.colors = []
        self.generate_colors()
        self.score = 0
        self.none = pygame.image.load(r'images\none.png')

    def generate_colors(self):
        self.colors = sns.color_palette("Spectral", 30)
        self.colors.extend(sns.color_palette("vlag", 30))
        self.colors.extend(reversed(sns.color_palette("cubehelix", 100)[40:]))
        for i, color in enumerate(self.colors):
            self.colors[i] = tuple(map(lambda x: x * 255, color))

    def print(self, text, x, y):
        printable = self.normalyze(text)
        top = 0.05
        left = 0.35
        scale = 0.6
        if len(printable) == 2:
            left = 0.25
        elif len(printable) == 3:
            left = 0.1
            scale = 0.55
        elif len(printable) == 4:
            top = 0.15
            left = 0.1
            scale = 0.45
        elif len(printable) == 5:
            top = 0.2
            left = 0.05
            scale = 0.3
        font = pygame.font.SysFont('Comic Sans MS', int(self.cell_size * scale))
        text = font.render(printable, False, (0, 0, 0))
        screen.blit(text, (self.left + (y + left) * self.cell_size, self.top + (x + top * (0.6 / scale)) * self.cell_size))

    def normalyze(self, t):
        if len(t) < 5:
            return t
        return t[0] + 'E' + str(floor(log10(int(t))))

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        pygame.draw.rect(screen, '#998f70', (self.left - 4, self.top - 4, self.width * self.cell_size + 10, self.width * self.cell_size + 10), 0)
        for i in range(self.width):
            for j in range(self.width):
                if self.board[i][j] is not None:
                    pygame.draw.rect(screen, self.colors[self.board[i][j]],
                                     (self.left + j * self.cell_size + 3,
                                      self.top + i * self.cell_size + 3,
                                      self.cell_size - 4, self.cell_size - 4), 0)
                    self.print(str(2 ** self.board[i][j]), i, j)
                else:
                    screen.blit(self.none, (self.left + j * self.cell_size + 1, self.top + i * self.cell_size + 1))

    def draw_rect(self, i, j, color):
                pygame.draw.rect(screen, color, (self.left + j * self.cell_size + 1,
                                                   self.top + i * self.cell_size + 1,
                                                   self.cell_size, self.cell_size), 1)

    def add(self, lost):
        left = set()
        for i in range(self.width):
            for j in range(self.width):
                if self.board[i][j] is None:
                    left.add((i, j))
        n = 1
        r = random.random()
        if r > 0.3:
            n = 2
        if r > 0.5:
            n = 3
        if r > 0.9:
            n = 4
        for i in range(n):
            if len(left) < 1:
                lost.show()
                return
            x, y = random.choice(list(left))
            self.board[x][y] = random.randrange(3)
            left.remove((x, y))

    def move(self, side):
        res = 0
        if side == 'up':
            for i in range(self.width):
                upd = 1
                while upd == 1:
                    upd = 0
                    for j in range(self.width):
                        if self.board[i][j] is not None:
                            pos = i - 1
                            while pos >= 0 and (self.board[pos][j] is None or self.board[pos][j] == self.board[pos + 1][j]):
                                if self.board[pos][j] == self.board[pos + 1][j]:
                                    self.board[pos + 1][j] += 1
                                    self.score += 2 ** self.board[pos + 1][j]
                                    self.board[pos][j] = None
                                self.board[pos][j] = self.board[pos + 1][j]
                                self.board[pos + 1][j] = None
                                pos -= 1
                                upd = 1
                    res = max(res, upd)
        elif side == 'down':
            for i in range(self.width - 1, -1, -1):
                upd = 1
                while upd == 1:
                    upd = 0
                    for j in range(self.width - 1, -1, -1):
                        if self.board[i][j] is not None:
                            pos = i + 1
                            while pos < self.width and (self.board[pos][j] is None or self.board[pos][j] == self.board[pos - 1][j]):
                                if self.board[pos][j] == self.board[pos - 1][j]:
                                    self.board[pos - 1][j] += 1
                                    self.score += 2 ** self.board[pos - 1][j]
                                    self.board[pos][j] = None
                                self.board[pos][j] = self.board[pos - 1][j]
                                self.board[pos - 1][j] = None
                                pos += 1
                                upd = 1
                    res = max(res, upd)
        elif side == 'left':
            for i in range(self.width):
                upd = 1
                while upd == 1:
                    upd = 0
                    for j in range(self.width):
                        if self.board[j][i] is not None:
                            pos = i - 1
                            while pos >= 0 and (self.board[j][pos] is None or self.board[j][pos] == self.board[j][pos + 1]):
                                if self.board[j][pos] == self.board[j][pos + 1]:
                                    self.board[j][pos + 1] += 1
                                    self.score += 2 ** self.board[j][pos + 1]
                                    self.board[j][pos] = None
                                self.board[j][pos] = self.board[j][pos + 1]
                                self.board[j][pos + 1] = None
                                pos -= 1
                                upd = 1
                    res = max(res, upd)
        elif side == 'right':
            for i in range(self.width - 1, -1, -1):
                upd = 1
                while upd == 1:
                    upd = 0
                    for j in range(self.width - 1, -1, -1):
                        if self.board[j][i] is not None:
                            pos = i + 1
                            while pos < self.width and (self.board[j][pos] is None or self.board[j][pos] == self.board[j][pos - 1]):
                                if self.board[j][pos] == self.board[j][pos - 1]:
                                    self.board[j][pos - 1] += 1
                                    self.score += 2 ** self.board[j][pos - 1]
                                    self.board[j][pos] = None
                                self.board[j][pos] = self.board[j][pos - 1]
                                self.board[j][pos - 1] = None
                                pos += 1
                                upd = 1
                    res = max(res, upd)
        else:
            return False
        return res

    def rebuild(self, n):
        self.width = n
        self.board = [[None] * n for _ in range(n)]
        self.score = 0

    def get_size(self):
        a = self.width * self.cell_size
        return [max(400, a + 50), max(400, a + 225)]

    def get_score(self):
        return self.score


class ListWidget:
    def __init__(self, geometry, paths):
        self.x, self.y = self.pos = (geometry[0], geometry[1])
        self.width = geometry[3]
        self.scale = geometry[2]
        self.choices = []
        self.cur = None
        self.waiting = False
        self.small = pygame.image.load(paths[0])
        self.big = pygame.image.load(paths[1])

    def draw(self, screen):
        font = pygame.font.SysFont('Comic Sans MS', self.scale * 3 // 5)
        if self.waiting is False:
            screen.blit(self.small, self.pos)
            text = font.render(self.cur, False, (0, 0, 0))
            screen.blit(text, (self.x, self.y))
        else:
            length = self.get_size()
            screen.blit(self.big, self.pos)
            for i in range(length):
                text = font.render(self.choices[i], False, (0, 0, 0))
                screen.blit(text, (self.x, self.y + i * self.scale))

    def set_choices(self, choices):
        self.choices = choices

    def get_size(self):
        return len(self.choices)

    def get_pos(self):
        return self.pos

    def get_scale(self):
        return self.scale

    def is_waiting(self):
        return self.waiting

    def choose(self, n):
        self.cur = self.choices[n]
        self.waiting = False

    def maximize(self):
        self.waiting = True

    def get_current(self):
        return self.cur

    def get_width(self):
        return self.width


def update(screen):
    screen.fill((255, 255, 255))
    board.render(screen)
    font = pygame.font.SysFont('Comic Sans MS', 30)
    text = font.render('Size:', False, (0, 0, 0))
    screen.blit(text, (25, 25))
    text = font.render('Gravity:', False, (0, 0, 0))
    screen.blit(text, (165, 25))
    text = font.render('Autorotating:', False, (0, 0, 0))
    screen.blit(text, (25, 100))
    size_list.draw(screen)
    moves_list.draw(screen)
    gravity_list.draw(screen)
    dialog.draw(screen, board.get_size())
    lost.draw(screen, board.get_size())
    font = pygame.font.SysFont('Comic Sans MS', 50)
    text = font.render('Score: ' + str(board.get_score()), False, (0, 0, 0))
    screen.blit(text, (25, board.get_size()[1]))
    pygame.display.flip()


class UpdateDialog:
    def __init__(self, text):
        self.display = False
        self.text = text

    def show(self):
        self.display = True

    def hide(self):
        self.display = False

    def draw(self, screen, size):
        if self.display:
            screen.fill('white')
            font = pygame.font.SysFont('Comic Sans MS', 40)
            text = font.render(self.text, False, (0, 0, 0))
            screen.blit(text, (size[0] // 2 - (10 * len(self.text)), size[1] // 2 - 80))
            pygame.draw.rect(screen, 'black', (size[0] // 2 - 100, size[1] // 2 + 10, 80, 40), 1)
            pygame.draw.rect(screen, 'black', (size[0] // 2 + 20, size[1] // 2 + 10, 80, 40), 1)
            text = font.render('Yes', False, (0, 0, 0))
            screen.blit(text, (size[0] // 2 - 90, size[1] // 2))
            text = font.render('No', False, (0, 0, 0))
            screen.blit(text, (size[0] // 2 + 30, size[1] // 2))

    def get_ans(self, click, size):
        x, y = click
        if size[0] // 2 - 100 <= x <= size[0] // 2 - 20 and size[1] // 2 + 10 <= y <= size[1] // 2 + 50:
            return True
        if size[0] // 2 + 20 <= x <= size[0] // 2 + 100 and size[1] // 2 + 10 <= y <= size[1] // 2 + 50:
            return False
        return None

    def is_active(self):
        return self.display


# prep
pygame.init()
pygame.font.init()
pygame.display.set_caption('Super 2048')
# consts
n = 12
side = 50
size = width, height = (n + 1) * side, (n + 6) * side
screen = pygame.display.set_mode(size)
# init
board = Board(n)
board.set_view(25, 200, 50)
size_list = ListWidget([100, 25, 50, 1], [r'images\none.png', r'images\sizes.png'])
size_list.set_choices([' ' + str(i) for i in range(5, 13)])
size_list.choose(7)
moves_list = ListWidget([225, 100, 50, 3], [r'images\move.png', r'images\moves.png'])
moves_list.set_choices(['   manual', '  rotation', '  up-down', ' left-right', '  random'])
moves_list.choose(0)
gravity_list = ListWidget([280, 25, 50, 1.8], [r'images\gravity.png', r'images\gravities.png'])
gravity_list.set_choices([' none', ' down', '  left', '   up', ' right'])
gravity_list.choose(0)
dialog = UpdateDialog('Are you sure?')
lost = UpdateDialog('Start new game?')
board.add(lost)
# run
running = True
cnt, p = 0, 10
flag = 0
while running:
    if lost.is_active():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                t = lost.get_ans(event.pos, board.get_size())
                if t:
                    board.rebuild(int(size_list.get_current().lstrip(' ')))
                    lost.hide()
                    board.add(lost)
                    moves_list.choose(0)
                    gravity_list.choose(0)
                elif t is False:
                    running = False
    elif size_list.get_current().lstrip(' ') != str(n):
        dialog.show()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if dialog.get_ans(event.pos, board.get_size()):
                    n = int(size_list.get_current().lstrip(' '))
                    size = width, height = max((n + 1) * side, 400), (n + 6) * side
                    screen = pygame.display.set_mode(size)
                    board.rebuild(n)
                    dialog.hide()
                    board.add(lost)
                elif dialog.get_ans(event.pos, board.get_size()) is False:
                    size_list.choose(n - 5)
                    dialog.hide()
    else:
        cnt += 1
        if cnt % p == 0:
            way = gravity_list.get_current().lstrip(' ')
            if way != 'none':
                flag += 1
                board.move(way)
                if flag == 1:
                    board.add(lost)
            else:
                flag = 0
            automatation = moves_list.get_current().lstrip(' ')
            if automatation != 'manual':
                sides = ['up', 'right', 'down', 'left']
                if automatation == 'random':
                    board.move(random.choice(sides))
                elif automatation == 'rotation':
                    board.move(sides[(cnt // p) % 4])
                elif automatation == 'up-down':
                    board.move(sides[((cnt // p) % 2) * 2])
                elif automatation == 'left-right':
                    board.move(sides[((cnt // p) % 2) * 2 + 1])
                board.add(lost)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if moves_list.get_current().lstrip(' ') == 'manual':
                    flag = False
                    if event.key == pygame.K_UP:
                        flag = board.move('up')
                    elif event.key == pygame.K_RIGHT:
                        flag = board.move('right')
                    elif event.key == pygame.K_DOWN:
                        flag = board.move('down')
                    elif event.key == pygame.K_LEFT:
                        flag = board.move('left')
                    if flag:
                        board.add(lost)
                    update(screen)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                lists = [size_list, moves_list, gravity_list]
                possible = True
                opened = None
                for l in lists:
                    if l.is_waiting():
                        possible = False
                        opened = l
                if possible:
                    for l in lists:
                        list_pos = l.get_pos()
                        scale = l.get_scale()
                        if list_pos[0] <= event.pos[0] <= list_pos[0] + scale * l.get_width() and\
                                list_pos[1] <= event.pos[1] <= list_pos[1] + scale:
                            l.maximize()
                else:
                    list_pos = opened.get_pos()
                    scale = opened.get_scale()
                    length = opened.get_size()
                    if list_pos[0] <= event.pos[0] <= list_pos[0] + scale * opened.get_width() and\
                            list_pos[1] <= event.pos[1] <= list_pos[1] + scale * length:
                        opened.choose((event.pos[1] - list_pos[1]) // scale)
                    if opened == gravity_list:
                        flag = 0
    update(screen)
pygame.quit()
