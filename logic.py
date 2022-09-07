# -*- coding: utf-8 -*-

# import modules
from sys import exit
from pygame import font, image, transform
from pygame import quit
from pygame import draw
from pygame import mouse


class WolvesAndSheep:
    def __init__(self, _screen, _count, _size, _margin, _w, _h, _map, _colors):
        self.screen = _screen
        self.count = _count
        self.size = _size
        self.margin = _margin
        self.w = _w
        self.h = _h
        self.map = _map
        self.COLORS = _colors
        self.style1 = font.SysFont('Consolas', 10)
        self.style2 = font.SysFont('Consolas', int(self.size / 2))
        self.w_img = transform.scale(image.load('pictures/wolf.png').convert_alpha(), (self.size, self.size))
        self.s_img = transform.scale(image.load('pictures/sheep.png').convert_alpha(), (self.size, self.size))
        self.menu = (
            (0, 'Wolves and Sheep'),
            (1, 'Start game'),
            (2, 'Exit game'),
        )
        self.COUNT = len(self.menu)

    def draw_menu(self):
        # Список позиций пунктов МЕНЮ [ x, y, width, height ]
        self.pos = []
        # Отрисовываем ФОН
        draw.rect(self.screen, self.COLORS[5], (0, 0, self.w, self.h))
        # Получаем координаты МЫШИ
        x, y = mouse.get_pos()
        # Формируем компоненты МЕНЮ
        for i in range(self.COUNT):
            text = self.style2.render(self.menu[i][1], True, self.COLORS[2])
            if self.menu[i][0] == 0:
                text = self.style2.render(self.menu[i][1], True, self.COLORS[0])
            text_w, text_h = text.get_size()
            self.pos += [
                # [ x, y, width, height ]
                [
                    (self.w - text_w) / 2,
                    (self.h - text_h*self.COUNT)/2 + i*(text.get_size()[1]+5),
                    text_w,
                    text_h
                ]
            ]
            # Определяем, находится ли курсор в зоне МЕНЮ
            if self.pos[i][0] <= x <= self.pos[i][0] + self.pos[i][2] and \
                    self.pos[i][1] <= y <= self.pos[i][1] + self.pos[i][3] and self.menu[i][0] != 0:
                text = self.style2.render(self.menu[i][1], True, self.COLORS[1])
            self.screen.blit(text, (self.pos[i][0], self.pos[i][1]))

    def draw_map(self):
        for i in range(self.count):
            for j in range(self.count):
                # Получаем позицию для каждого блока (чтобы его нарисовать)
                x, y = self.pos_x_and_y(j, i)
                # Рисуем карту в шахматном порядке
                COLOR = self.COLORS[3]
                if i % 2 == 0 and j % 2 == 0:
                    COLOR = self.COLORS[4]
                if i % 2 != 0 and j % 2 != 0:
                    COLOR = self.COLORS[4]
                draw.rect(self.screen, COLOR, (x, y, self.size, self.size))

    def draw_sheep_and_wolves(self):
        for i in range(self.count):
            for j in range(self.count):
                # Отрисовываем область, куда можно ходить
                if self.map[i][j] == 2:
                    if i != 0 and j != 0 and self.map[i - 1][j - 1] != 1:
                        x, y = self.pos_x_and_y(j - 1, i - 1)
                        draw.rect(self.screen, self.COLORS[7], (x, y, self.size, self.size), 1)
                    if i != 0 and j != self.count - 1 and self.map[i - 1][j + 1] != 1:
                        x, y = self.pos_x_and_y(j + 1, i - 1)
                        draw.rect(self.screen, self.COLORS[7], (x, y, self.size, self.size), 1)
                    if i != self.count - 1 and j != 0 and self.map[i + 1][j - 1] != 1:
                        x, y = self.pos_x_and_y(j - 1, i + 1)
                        draw.rect(self.screen, self.COLORS[7], (x, y, self.size, self.size), 1)
                    if i != self.count - 1 and j != self.count - 1 and self.map[i + 1][j + 1] != 1:
                        x, y = self.pos_x_and_y(j + 1, i + 1)
                        draw.rect(self.screen, self.COLORS[7], (x, y, self.size, self.size), 1)
                # Получаем позицию для каждого блока (чтобы его нарисовать)
                x, y = self.pos_x_and_y(j, i)
                # Выставляем картинки ВОЛКОВ и ОВЕЧКИ
                if self.map[i][j] == 1: self.screen.blit(self.w_img, (x, y))
                if self.map[i][j] == 2: self.screen.blit(self.s_img, (x, y))

    def pos_x_and_y(self, j, i):
        # Кортеж позиции блока по x & y из i & j
        return (j*self.size + (j+1) * self.margin,  i*self.size + (i+1) * self.margin)

    def get_position_wolf(self): # Получаем текущую позицию ВОЛКА
        self.pos_wolf = []
        for i in range(self.count):
            for j in range(self.count):
                if self.map[i][j] == 1:
                    # Формируем список значений, для победы
                    self.pos_wolf += [ i ]
        # Возврат минимальной позиции ВОЛКА в строке
        return min(self.pos_wolf)

    def get_position_sheep(self):
        # Получаем текущую позицию ОВЕЧКИ
        for i in range(self.count):
            for j in range(self.count):
                if self.map[i][j] == 2:
                    x, y = self.pos_x_and_y(j, i)
                    return ( x, y, i, j )

    def goto_left_up(self):
        # Движение ОВЕЧКИ по диагонали [влево-вверх]
        for i in range(self.count):
            for j in range(self.count):
                if self.map[i][j] == 2 and self.map[i - 1][j - 1] != 1:
                    self.map[i][j] = 0
                    self.map[i - 1][j - 1] = 2
                    return True
        return False

    def goto_right_up(self):
        # Движение ОВЕЧКИ по диагонали [вправо-вверх]
        for i in range(self.count):
            for j in range(self.count):
                if self.map[i][j] == 2 and self.map[i - 1][j + 1] != 1:
                    self.map[i][j] = 0
                    self.map[i - 1][j + 1] = 2
                    return True
        return False

    def goto_left_down(self):
        # Движение ОВЕЧКИ по диагонали [влево-вниз]
        for i in range(self.count):
            for j in range(self.count):
                if self.map[i][j] == 2 and self.map[i + 1][j - 1] != 1:
                    self.map[i][j] = 0
                    self.map[i + 1][j - 1] = 2
                    return True
        return False

    def goto_right_down(self):
        # Движение ОВЕЧКИ по диагонали [вправо-вниз]
        for i in range(self.count):
            for j in range(self.count):
                if self.map[i][j] == 2 and self.map[i + 1][j + 1] != 1:
                    self.map[i][j] = 0
                    self.map[i + 1][j + 1] = 2
                    return True
        return False

    def get_position_mouse_for_menu(self):
        # Определяем попадание по пунктам меню
        # Получаем координаты МЫШИ
        x, y = mouse.get_pos()
        # Определяем, находится ли курсор в зоне МЕНЮ
        for i in range(self.COUNT):
            if self.pos[i][0] <= x <= self.pos[i][0] + self.pos[i][2] and \
                    self.pos[i][1] <= y <= self.pos[i][1] + self.pos[i][3]:
                if self.menu[i][0] == 1:
                    # Запускаем игру
                    # self.map = self.begin_map
                    self.map = [
                        [1, 0, 1, 0, 1, 0, 1, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 2, 0, 0, 0, 0],
                    ]
                    if self.COUNT > 3:
                        # Убираем из меню всё ненужное
                        self.menu = self.menu[:3]
                    return False
                if self.menu[i][0] == 2:
                    # Выходим из игры
                    quit()
                    exit()
        return True

    def get_position_mouse_for_sheep(self):
        # Передвижение ОВЕЧКИ
        # Получаем координаты МЫШИ
        mouse_x, mouse_y = mouse.get_pos()
        # Получаем координаты ОВЕЧКИ
        sx, sy, i, j = self.get_position_sheep()
        # Определяем куда можно ходить ОВЕЧКЕ, исходя из текущей позиции
        size = self.size + self.margin
        if sx - size <= mouse_x <= sx and sy - size <= mouse_y <= sy:
            # Если ОВЕЧКА сходила, то ходит ВОЛК
            if self.goto_left_up(): return self.bot_wolf_next() # Ход ВОЛКА
        if sx + size <= mouse_x <= sx + size * 2 and sy - size <= mouse_y <= sy:
            # Если ОВЕЧКА сходила, то ходит ВОЛК
            if self.goto_right_up(): return self.bot_wolf_next() # Ход ВОЛКА
        if sx - size <= mouse_x <= sx and sy + size <= mouse_y <= sy + size * 2:
            # Если ОВЕЧКА сходила, то ходит ВОЛК
            if self.goto_left_down(): return self.bot_wolf_next() # Ход ВОЛКА
        if sx + size <= mouse_x <= sx + size * 2 and sy + size <= mouse_y <= sy + size * 2:
            # Если ОВЕЧКА сходила, то ходит ВОЛК
            if self.goto_right_down(): return self.bot_wolf_next()  # Ход ВОЛКА
        return False

    def bot_wolf_next(self): # Определяет в какую сторону пойдёт ВОЛК
        # Получаем координаты ВОЛКА
        wolf_i = self.get_position_wolf()
        # Получаем координаты ОВЕЧКИ
        sheep_x, sheep_y, sheep_i, sheep_j = self.get_position_sheep()
        # Определяем, ВЫИГРАЛА ли ОВЕЧКА
        if sheep_i <= wolf_i:
            self.menu += ((0, 'You win!'))
            return True
        # Цикл для поиска ВОЛКА и передвижения по карте
        break_of_the_loop = False
        for i in range(self.count):
            if break_of_the_loop: break
            for j in range(self.count):
                # j - позиция ВОЛКА
                # sheep_j - позиция ОВЕЧКИ
                if self.map[i][j] == 1:
                    # Определяем, куда пойдёт ВОЛК
                    if sheep_j > j and sheep_i >= i:
                        break_of_the_loop = self.bot_wolf_move_2(i, j)
                        if break_of_the_loop: break
                    if sheep_j < j and sheep_i >= i:
                        break_of_the_loop = self.bot_wolf_move_1(i, j)
                        if break_of_the_loop: break
                    if sheep_j == j and sheep_i > i:
                        break_of_the_loop = self.bot_wolf_move_3(i, j, sheep_i)
                        if break_of_the_loop: break
                    # Поражение ОВЕЧКИ
                    if sheep_i == self.count - 1:
                        if sheep_j == self.count - 1 and self.map[sheep_i - 1][sheep_j - 1] == 1:
                            self.menu += ( (0, 'You lose :('), )
                            return True
                        if self.map[sheep_i - 1][sheep_j - 1] == 1 and self.map[sheep_i - 1][sheep_j + 1] == 1:
                            self.menu += ( (0, 'You lose :('), )
                            return True
        return False

    def move_right(self, i, j):
        # Движение ВОЛКА [вправо]
        self.map[i][j] = 0
        self.map[i + 1][j + 1] = 1
        return True

    def move_left(self, i, j):
        # Движение ВОЛКА [влево]
        self.map[i][j] = 0
        self.map[i + 1][j - 1] = 1
        return True

    def bot_wolf_move_1(self, i, j):
        # Пережвижение ВОЛКА [влево]
        if i != self.count - 1:
            if 1 < j < self.count - 2:
                if self.map[i + 1][j - 1] == 2 or self.map[i + 1][j + 1] == 2: return False
                if self.map[i + 1][j - 1] != 1: return self.move_left(i, j)
                return False
            if j == self.count - 2:
                if self.map[i + 1][j - 1] == 2 or self.map[i + 1][j + 1] == 2: return False
                if self.map[i][j - 2] != 1 and self.map[i + 2][j] == 2 and i < self.count - 1: return self.move_left(i, j)
                if self.map[i + 1][j - 1] != 1: return self.move_left(i, j)
                return False
            if j == self.count - 1:
                if self.map[i + 1][j - 1] == 2 or self.map[i + 1][j - 1] == 1: return False
                return self.move_left(i, j)
            return False
        return False

    def bot_wolf_move_2(self, i, j):
        # Пережвижение ВОЛКА [вправо]
        if i != self.count - 1:
            if 1 < j < self.count - 2:
                if self.map[i + 1][j - 1] == 2 or self.map[i + 1][j + 1] == 2: return False
                if self.map[i][j + 2] == 1 and self.map[i + 2][j + 2] == 2: return False
                if self.map[i + 1][j + 1] != 1: return self.move_right(i, j)
                return False
            if j == 0:
                if self.map[i + 1][j + 1] == 2 or self.map[i + 1][j + 1] == 1: return False
                return self.move_right(i, j)
            if j == 1:
                if self.map[i + 1][j - 1] == 2 or self.map[i + 1][j + 1] == 2: return False
                if self.map[i][j + 2] != 1 and self.map[i + 2][j] == 2 and i < self.count - 1: return self.move_right(i, j)
                if self.map[i + 1][j + 1] != 1: return self.move_right(i, j)
                return False
            return False
        return False

    def bot_wolf_move_3(self, i, j, sheep_i):
        # Передвижение ВОЛКА [вправо или влево]
        if sheep_i - i == 2:
            if 0 < j < self.count - 1:
                if self.map[i + 1][j - 1] == 2 or self.map[i + 1][j + 1] == 2: return False
                if self.map[i + 1][j + 1] != 1 and self.map[i + 1][j - 1] != 1: return False
                if self.map[i + 1][j + 1] != 1: return self.move_right(i, j)
                if self.map[i + 1][j - 1] != 1: return self.move_left(i, j)
                return False
            if j == 0:
                if self.map[i + 1][j + 1] == 2 or self.map[i + 1][j + 1] == 1: return False
                return self.move_right(i, j)
            if j == self.count - 1:
                if self.map[i + 1][j - 1] == 2 or self.map[i + 1][j - 1] == 1: return False
                return self.move_left(i, j)
            return False
        if sheep_i - i > 2:
            if 0 < j < self.count - 1:
                if self.map[i + 1][j + 1] != 1 and self.map[i + 1][j - 1] != 1: return False
                if self.map[i + 1][j - 1] != 1: return self.move_left(i, j)
                if self.map[i + 1][j + 1] != 1: return self.move_right(i, j)
                return False
            if j == 0:
                if self.map[i + 1][j + 1] == 2 or self.map[i + 1][j + 1] == 1: return False
                return self.move_right(i, j)
            if j == self.count - 1:
                if self.map[i + 1][j - 1] == 2 or self.map[i + 1][j - 1] == 1: return False
                return self.move_left(i, j)
            return False
        return False