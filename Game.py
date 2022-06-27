# -*- coding: utf-8 -*-

import sys
import pygame as pg
from Logic import WolvesAndSheep

BLOCKS = 8 # Кол-во блоков в ширину и высоту
SIZE_BLOCK = 70 # Размер блока [квадратный]
MARGIN = 2 # Отступы
WIDTH = MARGIN + (SIZE_BLOCK + MARGIN) * BLOCKS # Ширина рабочего окна
HEIGHT = WIDTH # Высота рабочего окна
RUNNING_GAME = True # Запуск игры
MENU = True # Вызов меню игры

COLORS = ( # Кортеж цветов [палитра]
    (  0, 200,   0), # 0. Ярко-зелёный
    (153, 154, 153), # 1. Хмуро-серый
    (255, 255, 255), # 2. Белый
    (153, 102,  52), # 3. Светло-коричневый
    (101,  51,   0), # 4. Тёмно-коричневый
    ( 26,  26,  26), # 5. Чёрно-сероватый
    (  0,   0,   0), # 6. Чёрный
    (250, 239,   4), # 7. Жёлтый
)

MAP = [ # Игровая карта
    [ 1, 0, 1, 0, 1, 0, 1, 0 ],
    [ 0, 0, 0, 0, 0, 0, 0, 0 ],
    [ 0, 0, 0, 0, 0, 0, 0, 0 ],
    [ 0, 0, 0, 0, 0, 0, 0, 0 ],
    [ 0, 0, 0, 0, 0, 0, 0, 0 ],
    [ 0, 0, 0, 0, 0, 0, 0, 0 ],
    [ 0, 0, 0, 0, 0, 0, 0, 0 ],
    [ 0, 0, 0, 2, 0, 0, 0, 0 ],
]

if __name__ == '__main__':
    pg.init() # Инициализация (нужна)
    screen = pg.display.set_mode((WIDTH, HEIGHT)) # Создаём окно
    pg.display.set_caption('Wolves and Sheep') # Название окна
    game = WolvesAndSheep(screen, BLOCKS, SIZE_BLOCK, MARGIN, WIDTH, HEIGHT, MAP, COLORS)

    while RUNNING_GAME: # Запуск игры
        pg.time.delay(100)
        screen.fill(COLORS[5])
        for event in pg.event.get(): # События
            if event.type == pg.QUIT: # Закрытие окна
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN: # Нажатие кнопки мыши
                if event.button == 1: # ЛКМ
                    if MENU:
                        MENU = game.get_position_mouse_for_menu()
                    else:
                        MENU = game.get_position_mouse_for_sheep()
        if MENU:
            game.draw_start_menu() # Рисуем меню
        else:
            game.draw_map() # Рисуем карту
            game.draw_sheep_and_wolves() # Рисуем Волков и Овечку
        pg.display.update() # Обновляем рабочий экран
    pg.quit()