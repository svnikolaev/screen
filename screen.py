#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import random
import math

from pygame.constants import SRCALPHA

SCREEN_DIM = (800, 600)


class Vec2d():
    """Реализовать класс 2-мерных векторов Vec2d [1]. В классе следует определить методы для основных математических
    операций, необходимых для работы с вектором: Vec2d.__add__ (сумма), Vec2d.__sub__ (разность),
    Vec2d.__mul__ (произведение на число). А также добавить возможность вычислять длину вектора с использованием
    функции len(a) и метод int_pair, который возвращает кортеж из двух целых чисел (текущие координаты вектора).

    [1] Вектор определяется координатами x, y — точка конца вектора.
    Начало вектора всегда совпадает с центом координат (0, 0).
    """
    def __init__(self, x, y, speed_x=0, speed_y=0):
        self.x, self.y = x, y
        self.speed_x, self.speed_y = speed_x, speed_y

    def __add__(self, other):
        """возвращает сумму двух векторов"""
        return Vec2d(
            self.x + other.x, self.y + other.y,
            self.speed_x + other.speed_x, self.speed_y + other.speed_y
        )

    def __sub__(self, other):
        """возвращает разность двух векторов"""
        return Vec2d(
            self.x - other.x, self.y - other.y,
            self.speed_x - other.speed_x, self.speed_y - other.speed_y
        )

    def __mul__(self, k):
        """возвращает произведение вектора на число"""
        return Vec2d(
            self.x * k, self.y * k,
            self.speed_x * k, self.speed_y * k
        )

    def __len__(self):
        """Реализация весьма экзотического запроса от заказчика"""
        a = self.get_A()
        b = self.get_B()
        ab = ((b[0] - a[0])**2 + (b[1] - a[1])**2) ** 0.5
        return int(ab)

    def get_A(self):
        return self.x, self.y

    def get_B(self):
        return self.x + self.speed_x, self.y + self.speed_y

    def int_pair(self):
        return self.get_A()

    def get_speed(self):
        return Vec2d(self.speed_x, self.speed_y)

    def __repr__(self):
        return (f"Vector(x: {self.x}, y: {self.y}"
                f", speed_x: {self.speed_x}, speed_y: {self.speed_y})")


class Polyline():
    """Реализовать класс замкнутых ломаных Polyline с методами отвечающими за добавление в ломаную точки (Vec2d) c её
    скоростью, пересчёт координат точек (set_points) и отрисовку ломаной (draw_points). Арифметические действия с
    векторами должны быть реализованы с помощью операторов, а не через вызовы соответствующих методов.
    """
    def __init__(self):
        self.vectors = []

    def reset(self):
        self.vectors = []

    def add_point(self, x, y, speed_x, speed_y):
        self.vectors.append(Vec2d(x, y, speed_x, speed_y))
        # self.speeds.append(Vec2d(speed_x, speed_y))

    def set_points(self):
        """функция перерасчета координат опорных точек"""
        vectors = self.vectors
        # points, speeds = self.points, self.speeds
        for p in range(len(vectors)):
            vectors[p] = vectors[p] + vectors[p].get_speed()
            if vectors[p].x > SCREEN_DIM[0] or vectors[p].x < 0:
                vectors[p].speed_x *= -1
            if vectors[p].y > SCREEN_DIM[1] or vectors[p].y < 0:
                vectors[p].speed_y *= -1
        self.vectors = vectors

    # def draw_points(self):
        # pass

    def draw_points(self, style="points", width=3, color=(255, 255, 255)):
        """функция отрисовки точек на экране"""
        vectors = self.vectors
        if style == "line":
            for p_n in range(-1, len(vectors) - 1):
                pygame.draw.line(gameDisplay, color,
                                 (int(vectors[p_n].x), int(vectors[p_n].y)),
                                 (int(vectors[p_n + 1].x), int(vectors[p_n + 1].y)), width)

        elif style == "points":
            for p in vectors:
                pygame.draw.circle(gameDisplay, color,
                                   (int(p.x), int(p.y)), width)


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
        return (base_points[deg] * alpha) + (self.get_point(base_points, alpha, deg - 1) * (1 - alpha) )

    def get_points(self, base_points, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(self.get_point(base_points, i * alpha))
        return res

    def get_knot(self, count, style="points", width=3, color=(255, 255, 255)):
        vectors = self.vectors
        if len(vectors) < 3:
            return []
        res = []
        for i in range(-2, len(vectors) - 2):
            base_points = []
            base_points.append(
                (vectors[i] + vectors[i+1]) * 0.5
            )
            # base_points.append(self.mul(self.add(points[i], points[i + 1]), 0.5))
            base_points.append(vectors[i+1])
            # base_points.append(points[i + 1])
            base_points.append(
                (vectors[i+1] + vectors[i+2]) * 0.5
            )
            # base_points.append(self.mul(self.add(points[i + 1], points[i + 2]), 0.5))
            res.extend(self.get_points(base_points, count))
        # super().draw_points(res, style=style, width=width, color=color)
        self.draw_lines(res, width=width, color=color)
        # return res
    
    def draw_lines(self, res, width=3, color=(255, 255, 255)):
        """функция отрисовки точек на экране"""
        vectors = res
        for p_n in range(-1, len(vectors) - 1):
            pygame.draw.line(gameDisplay, color,
                                (int(vectors[p_n].x), int(vectors[p_n].y)),
                                (int(vectors[p_n + 1].x), int(vectors[p_n + 1].y)), width)


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
        self.a_polyline = Knot()

    def start(self):
        working = self.working
        show_help = self.show_help
        pause = self.pause
        hue = self.hue
        color = self.color
        a_polyline = self.a_polyline
        show_closed_curve = True
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
                    if event.key == pygame.K_h:  # Show or hide closed curve
                        show_closed_curve = not show_closed_curve
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
                    """точка состоит из двух координат и двух цифр скорости points[0], speeds[0]
                    коорд.|скорость
                    точка 1
                    x 318 1.9721851954434146
                    y 118 0.6528092485848631
                    точка 2
                    x 188 0.17410999563958884
                    y 344 1.98854464906785
                    точка 3
                    x 466 0.9328028895220815
                    y 319 0.6620230434127816
                    """
                    speed_mod = 0.5
                    a_polyline.add_point(event.pos[0], event.pos[1], random.random() * speed_mod, random.random() * speed_mod)
                    # print(f'<class Vec2d with x: {event.pos[0]}, y: {event.pos[1]},'
                    #       + f' speed_x: {random.random() * speed_mod}, speed_y: {random.random() * speed_mod}>')
                    # a_polyline.points.append(event.pos)
                    # a_polyline.speeds.append((random.random() * speed_mod, random.random() * speed_mod))
                    # print(f'точка {len(a_polyline.points)}')
                    # print('x', a_polyline.points[-1][0], a_polyline.speeds[-1][0])
                    # print('y', a_polyline.points[-1][1], a_polyline.speeds[-1][1])

            # TODO put it in next_step()
            gameDisplay.fill((0, 0, 0))
            hue = (hue + 1) % 360
            color.hsla = (hue, 100, 50, 100)
            a_polyline.draw_points()
            if show_closed_curve:
                a_polyline.get_knot(self.steps, "line", 3, color)
            if not pause:
                a_polyline.set_points()
            if show_help:
                self.draw_help()
            pygame.display.flip()
            # TODO ^ ^ ^

    def next_step(self):
        pass

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
