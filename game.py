# -*- coding: utf-8 -*-

# import modules
from sys import exit
from pygame import time
from pygame import init, quit
from pygame import display
from pygame import event
from pygame import QUIT, MOUSEBUTTONDOWN

from map import *
from config import *
from logic import WolvesAndSheep


if __name__ == '__main__':
    init()
    # Создаём окно
    screen = display.set_mode((WIDTH, HEIGHT))
    # Название окна
    display.set_caption('Wolves and Sheep')
    game = WolvesAndSheep(screen, BLOCKS, SIZE_BLOCK, MARGIN, WIDTH, HEIGHT, MAP, PALETTE)
    # Игровой цикл
    while RUNNING_GAME:
        time.delay(100)
        screen.fill(PALETTE[5])
        # События
        for item in event.get():
            # Закрытие окна
            if item.type == QUIT:
                quit()
                exit()
            # Нажатие кнопки мыши
            elif item.type == MOUSEBUTTONDOWN:
                if item.button == 1: # ЛКМ
                    if MENU:
                        MENU = game.get_position_mouse_for_menu()
                    else:
                        MENU = game.get_position_mouse_for_sheep()
        if MENU:
            # Рисуем меню
            game.draw_menu()
        else:
            # Рисуем карту
            game.draw_map()
            # Рисуем Волков и Овечку
            game.draw_sheep_and_wolves()
        # Обновляем рабочий экран
        display.update()
    quit()