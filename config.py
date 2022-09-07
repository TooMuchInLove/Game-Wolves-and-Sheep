# -*- coding: utf-8 -*-

# Кол-во блоков в ширину и высоту
BLOCKS = 8
# Размер блока [квадратный]
SIZE_BLOCK = 70
# Отступы
MARGIN = 2
# Ширина рабочего окна
WIDTH = MARGIN + (SIZE_BLOCK + MARGIN) * BLOCKS
# Высота рабочего окна
HEIGHT = WIDTH
# Запуск игры
RUNNING_GAME = True
# Вызов меню игры
MENU = True

# Палитра цветов
PALETTE = (
    (  0, 200,   0), # 0. Ярко-зелёный
    (153, 154, 153), # 1. Хмуро-серый
    (255, 255, 255), # 2. Белый
    ( 40, 181,  45), # 3. Светло-зелёный
    (  0, 125,   4), # 4. Тёмно-зелёный
    ( 26,  26,  26), # 5. Чёрно-сероватый
    (  0,   0,   0), # 6. Чёрный
    (250, 239,   4), # 7. Жёлтый
)