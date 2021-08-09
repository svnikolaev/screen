#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import random
import math

SCREEN_DIM = (800, 600)


class Vec2d():
    """Реализовать класс 2-мерных векторов Vec2d [1]. В классе следует определить методы для основных математических
    операций, необходимых для работы с вектором: Vec2d.__add__ (сумма), Vec2d.__sub__ (разность),
    Vec2d.__mul__ (произведение на число). А также добавить возможность вычислять длину вектора с использованием
    функции len(a) и метод int_pair, который возвращает кортеж из двух целых чисел (текущие координаты вектора).

    [1] Вектор определяется координатами x, y — точка конца вектора.
    Начало вектора всегда совпадает с центом координат (0, 0).
    """
    def __init__(self):
        pass

    def __add__(self):
        pass

    def __sub__(self):
        pass

    def __mul__(self):
        pass

    def len(self, a):
        pass

    def int_pair(self):
        pass


class Polyline():
    """Реализовать класс замкнутых ломаных Polyline с методами отвечающими за добавление в ломаную точки (Vec2d) c её
    скоростью, пересчёт координат точек (set_points) и отрисовку ломаной (draw_points). Арифметические действия с
    векторами должны быть реализованы с помощью операторов, а не через вызовы соответствующих методов.
    """
    def __init__(self):
        pass

    def set_points(self):
        pass

    def draw_points(self):
        pass


class Knot(Polyline):
    """Реализовать класс Knot (наследник класса Polyline), в котором добавление и пересчёт координат инициируют вызов
    функции get_knot для расчёта точек кривой по добавляемым «опорным» точкам [2].

    [2] Здесь стоит уточнить, что стоит различать понятия точек, используемых в описании задания.
    Существуют два вида: «опорные» и «сглаживания». Первые задают положение углов замкнутой ломаной и служат основой
    для вычисления вторых. Количество точек «сглаживания» определяет насколько плавными будут обводы углов ломаной.
    Вы можете поэкспериментировать с изменением количества точек сглаживания (см. команды программы) и понаблюдать,
    как изменяется отрисовка линии при различных значениях (текущее количество точек «сглаживания» можно посмотреть
    на экране справки).
    """
    def __init__(self):
        pass

    def get_knot(self):
        pass


# =======================================================================================
# Функции для работы с векторами
# =======================================================================================
def sub(x, y):
    """"возвращает разность двух векторов"""
    return x[0] - y[0], x[1] - y[1]


def add(x, y):
    """возвращает сумму двух векторов"""
    return x[0] + y[0], x[1] + y[1]


def length(x):
    """возвращает длину вектора"""
    return math.sqrt(x[0] * x[0] + x[1] * x[1])


def mul(v, k):
    """возвращает произведение вектора на число"""
    return v[0] * k, v[1] * k


def vec(x, y):
    """возвращает пару координат, определяющих вектор (координаты точки конца вектора),
    координаты начальной точки вектора совпадают с началом системы координат (0, 0)"""
    return sub(y, x)


# =======================================================================================
# Функции отрисовки
# =======================================================================================
def draw_points(points, style="points", width=3, color=(255, 255, 255)):
    """функция отрисовки точек на экране"""
    if style == "line":
        for p_n in range(-1, len(points) - 1):
            pygame.draw.line(gameDisplay, color,
                             (int(points[p_n][0]), int(points[p_n][1])),
                             (int(points[p_n + 1][0]), int(points[p_n + 1][1])), width)

    elif style == "points":
        for p in points:
            pygame.draw.circle(gameDisplay, color,
                               (int(p[0]), int(p[1])), width)


# =======================================================================================
# Функции, отвечающие за расчет сглаживания ломаной
# =======================================================================================
def get_point(points, alpha, deg=None):
    if deg is None:
        deg = len(points) - 1
    if deg == 0:
        return points[0]
    return add(mul(points[deg], alpha), mul(get_point(points, alpha, deg - 1), 1 - alpha))


def get_points(base_points, count):
    alpha = 1 / count
    res = []
    for i in range(count):
        res.append(get_point(base_points, i * alpha))
    return res


def get_knot(points, count):
    if len(points) < 3:
        return []
    res = []
    for i in range(-2, len(points) - 2):
        ptn = []
        ptn.append(mul(add(points[i], points[i + 1]), 0.5))
        ptn.append(points[i + 1])
        ptn.append(mul(add(points[i + 1], points[i + 2]), 0.5))

        res.extend(get_points(ptn, count))
    return res


def set_points(points, speeds):
    """функция перерасчета координат опорных точек"""
    for p in range(len(points)):
        points[p] = add(points[p], speeds[p])
        if points[p][0] > SCREEN_DIM[0] or points[p][0] < 0:
            speeds[p] = (- speeds[p][0], speeds[p][1])
        if points[p][1] > SCREEN_DIM[1] or points[p][1] < 0:
            speeds[p] = (speeds[p][0], -speeds[p][1])


class Game:
    def __init__(self, steps=35, working=True, show_help=False, pause=True, 
                 hue=0, color=pygame.Color(0)):
        self.steps = steps
        self.working = working
        self.show_help = show_help
        self.pause = pause
        self.hue = hue
        self.color = color
        points = []
        speeds = []
        while working:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    working = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        working = False
                    if event.key == pygame.K_r:
                        points = []
                        speeds = []
                    if event.key == pygame.K_p:
                        pause = not pause
                    if event.key == pygame.K_KP_PLUS:
                        self.set_steps_up(1)
                    if event.key == pygame.K_UP:
                        self.set_steps_up(1)
                    if event.key == pygame.K_F1:
                        show_help = not show_help
                    if event.key == pygame.K_KP_MINUS:
                        self.set_steps_down(1)
                    if event.key == pygame.K_DOWN:
                        self.set_steps_down(1)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    points.append(event.pos)
                    speeds.append((random.random() * 2, random.random() * 2))

            gameDisplay.fill((0, 0, 0))
            hue = (hue + 1) % 360
            color.hsla = (hue, 100, 50, 100)
            draw_points(points)
            draw_points(get_knot(points, steps), "line", 3, color)
            if not pause:
                set_points(points, speeds)
            if show_help:
                self.draw_help()
            pygame.display.flip()

    def set_steps_up(self, steps):
        self.steps += steps

    def set_steps_down(self, steps):
        self.steps -= steps if self.steps > 1 else 0

    def get_steps(self):
        return self.steps

    def draw_help(self):
        """функция отрисовки экрана справки программы"""
        steps = self.get_steps()
        gameDisplay.fill((50, 50, 50))
        font1 = pygame.font.SysFont("courier", 24)
        font2 = pygame.font.SysFont("serif", 24)
        data = []
        data.append(["F1", "Show Help"])
        data.append(["R", "Restart"])
        data.append(["P", "Pause/Play"])
        data.append(["Num+", "More points"])
        data.append(["Num-", "Less points"])
        data.append(["", ""])
        data.append([str(steps), "Current points"])

        pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
            (0, 0), (800, 0), (800, 600), (0, 600)], 5)
        for i, text in enumerate(data):
            gameDisplay.blit(font1.render(
                text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
            gameDisplay.blit(font2.render(
                text[1], True, (128, 128, 255)), (200, 100 + 30 * i))


# =======================================================================================
# Основная программа
# =======================================================================================
if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    client = Game()

    pygame.display.quit()
    pygame.quit()
    exit(0)
