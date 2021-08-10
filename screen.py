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
    # def __init__(self, x, y):
    #     self.value = (x, y)

    def __add__(self, other):
        """возвращает сумму двух векторов"""
        return self.value[0] + other[0], self.value[1] + other[1]

    def __sub__(self, other):
        """возвращает разность двух векторов"""
        return self.value[0] - other[0], self.value[1] - other[1]

    def __mul__(self, k):
        """возвращает произведение вектора на число"""
        return self.value[0] * k, self.value[1] * k

    # def __len__(self):
    #     pass
    
    def int_pair(self):
        pass

    def __repr__(self):
        return f"<class Vec2d with x:{x} and y:{y}>"


class Polyline():
    """Реализовать класс замкнутых ломаных Polyline с методами отвечающими за добавление в ломаную точки (Vec2d) c её
    скоростью, пересчёт координат точек (set_points) и отрисовку ломаной (draw_points). Арифметические действия с
    векторами должны быть реализованы с помощью операторов, а не через вызовы соответствующих методов.
    """
    def __init__(self, points=[], speeds=[]):
        self.points = points
        self.speeds = speeds
    
    def reset(self):
        self.points = []
        self.speeds = []

    def set_points(self):
        points, speeds = self.points, self.speeds
        """функция перерасчета координат опорных точек"""
        for p in range(len(points)):
            points[p] = self.add(points[p], speeds[p])
            if points[p][0] > SCREEN_DIM[0] or points[p][0] < 0:
                speeds[p] = (- speeds[p][0], speeds[p][1])
            if points[p][1] > SCREEN_DIM[1] or points[p][1] < 0:
                speeds[p] = (speeds[p][0], -speeds[p][1])
        self.points, self.speeds = points, speeds

    # def draw_points(self):
        # pass

    def draw_points(self, points, style="points", width=3, color=(255, 255, 255)):
        # points = self.points
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
    def sub(self, x, y):
        """возвращает разность двух векторов"""
        return x[0] - y[0], x[1] - y[1]

    def add(self, x, y):
        """возвращает сумму двух векторов"""
        return x[0] + y[0], x[1] + y[1]

    def length(self, x):
        """возвращает длину вектора"""
        return math.sqrt(x[0] * x[0] + x[1] * x[1])

    def mul(self, v, k):
        """возвращает произведение вектора на число"""
        return v[0] * k, v[1] * k

    def get_point(self, base_points, alpha, deg=None):
        if deg is None:
            deg = len(base_points) - 1
        if deg == 0:
            return base_points[0]
        return self.add(self.mul(base_points[deg], alpha), self.mul(self.get_point(base_points, alpha, deg - 1), 1 - alpha))

    def get_points(self, base_points, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(self.get_point(base_points, i * alpha))
        return res

    def get_knot(self, count, style="points", width=3, color=(255, 255, 255)):
        points = self.points
        if len(points) < 3:
            return []
        res = []
        for i in range(-2, len(points) - 2):
            ptn = []
            ptn.append(self.mul(self.add(points[i], points[i + 1]), 0.5))
            ptn.append(points[i + 1])
            ptn.append(self.mul(self.add(points[i + 1], points[i + 2]), 0.5))

            res.extend(self.get_points(ptn, count))
        # super().draw_points(res, style=style, width=width, color=color)
        self.draw_points(res, style="line", width=width, color=color)
        # return res


class Game:
    def __init__(self, steps=10, working=True, show_help=False, pause=True,
                 hue=0, color=pygame.Color(0)):
        self.steps = steps
        self.working = working
        self.show_help = show_help
        self.pause = pause
        self.hue = hue
        self.color = color
        # a_polyline = Polyline(points=[], speeds=[])
        self.a_polyline = Knot(points=[], speeds=[])

    def start(self):
        working = self.working
        show_help = self.show_help
        pause = self.pause
        hue = self.hue
        color = self.color
        a_polyline = self.a_polyline
        while working:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    working = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        working = False
                    if event.key == pygame.K_r:
                        a_polyline.reset()
                    if event.key == pygame.K_p:
                        pause = not pause
                        if a_polyline.points and a_polyline.speeds:
                            print('points', type(a_polyline.points[0]), a_polyline.points)
                            print('speeds', type(a_polyline.speeds[0]), a_polyline.speeds)
                            print()
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
                    a_polyline.points.append(event.pos)
                    a_polyline.speeds.append((random.random() * 2, random.random() * 2))

            gameDisplay.fill((0, 0, 0))
            hue = (hue + 1) % 360
            color.hsla = (hue, 100, 50, 100)
            a_polyline.draw_points(a_polyline.points)
            a_polyline.get_knot(self.steps, "line", 3, color)
            # a_polyline.draw_points(get_knot(a_polyline.points, self.steps), "line", 3, color)
            if not pause:
                # a_polyline.set_points(points, speeds)
                a_polyline.set_points()
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
    client.start()

    pygame.display.quit()
    pygame.quit()
    exit(0)
