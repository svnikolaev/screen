#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
from random import random

SCREEN_DIM = (800, 600)


class Vec2d():
    """Реализовать класс 2-мерных векторов Vec2d. В классе следует определить методы для основных математических
    операций, необходимых для работы с вектором: Vec2d.__add__ (сумма), Vec2d.__sub__ (разность),
    Vec2d.__mul__ (произведение на число). А также добавить возможность вычислять длину вектора с использованием
    функции len(a) и метод int_pair, который возвращает кортеж из двух целых чисел (текущие координаты вектора).
    """
    def __init__(self, x, y, speed_x=0, speed_y=0):
        self.x, self.y = x, y
        self.speed_x, self.speed_y = speed_x, speed_y

    def __add__(self, other):
        """возвращает сумму двух векторов"""
        return Vec2d(self.x + other.x, self.y + other.y,
                     self.speed_x + other.speed_x, self.speed_y + other.speed_y)

    def __sub__(self, other):
        """возвращает разность двух векторов"""
        return Vec2d(self.x - other.x, self.y - other.y,
                     self.speed_x - other.speed_x, self.speed_y - other.speed_y)

    def __mul__(self, k):
        """возвращает произведение вектора на число"""
        return Vec2d(self.x*k, self.y*k,
                     self.speed_x*k, self.speed_y*k)

    def __len__(self):
        """Реализация весьма экзотического запроса от заказчика"""
        a, b = self.get_A(), self.get_B()
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
    def __init__(self, gameDisplay, screen_dim=(800, 600)):
        self.vectors = []
        self.screen_dim = screen_dim
        self.gameDisplay = gameDisplay

    def reset(self):
        self.vectors = []

    def delete_point(self):
        del self.vectors[-1]

    def add_point(self, x, y, speed_x, speed_y):
        self.vectors.append(Vec2d(x, y, speed_x, speed_y))

    def set_points(self):
        """функция перерасчета координат опорных точек"""
        vectors = self.vectors
        screen_dim = self.screen_dim
        for p in range(len(vectors)):
            vectors[p] = vectors[p] + vectors[p].get_speed()
            if vectors[p].x > screen_dim[0] or vectors[p].x < 0:
                vectors[p].speed_x *= -1
            if vectors[p].y > screen_dim[1] or vectors[p].y < 0:
                vectors[p].speed_y *= -1
        self.vectors = vectors

    def draw_points(self, width=3, color=(255, 255, 255)):
        """функция отрисовки точек на экране"""
        vectors = self.vectors
        for p in vectors:
            pygame.draw.circle(self.gameDisplay, color,
                               (int(p.x), int(p.y)), width)


class Knot(Polyline):
    """Реализовать класс Knot (наследник класса Polyline), в котором добавление и пересчёт координат инициируют вызов
    функции get_knot для расчёта точек кривой по добавляемым «опорным» точкам.
    """
    def get_point(self, base_points, alpha, deg=None):
        if deg is None:
            deg = len(base_points) - 1
        if deg == 0:
            return base_points[0]
        return (base_points[deg] * alpha) + (self.get_point(base_points, alpha, deg - 1) * (1 - alpha))

    def get_points(self, base_points, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(self.get_point(base_points, i * alpha))
        return res

    def get_knot(self, count, width=3, color=(255, 255, 255)):
        vectors = self.vectors
        if len(vectors) < 3:
            return []
        res = []
        for i in range(-2, len(vectors) - 2):
            base_points = []
            base_points.append(
                (vectors[i] + vectors[i+1]) * 0.5
            )
            base_points.append(vectors[i+1])
            base_points.append(
                (vectors[i+1] + vectors[i+2]) * 0.5
            )
            res.extend(self.get_points(base_points, count))
        self.draw_curve(res, width=width, color=color)

    def draw_curve(self, res, width=3, color=(255, 255, 255)):
        """функция отрисовки кривой на экране"""
        vectors = res
        for p_n in range(-1, len(vectors) - 1):
            pygame.draw.line(self.gameDisplay, color,
                             (int(vectors[p_n].x), int(vectors[p_n].y)),
                             (int(vectors[p_n + 1].x), int(vectors[p_n + 1].y)), width)


class Game:
    def __init__(self, steps=10, color=pygame.Color(0), caption="MyScreenSaver", screen_dim=(800, 600)):
        self.steps = steps
        self.show_help = False
        self.pause = True
        self.show_closed_curve = True
        self.hue = 0
        self.color = color
        self.gameDisplay = pygame.display.set_mode(screen_dim)
        self.a_polyline = Knot(self.gameDisplay, screen_dim)
        self.caption = caption
        self.screen_dim = screen_dim

    def start(self):
        pygame.init()
        pygame.display.set_caption(self.caption)
        working = True
        while working:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    working = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        working = False
                    if event.key == pygame.K_r:
                        self.a_polyline.reset()
                    if event.key == pygame.K_p:
                        self.pause = not self.pause
                    if event.key == pygame.K_h:  # Show or hide closed curve
                        self.show_closed_curve = not self.show_closed_curve
                    if event.key == pygame.K_KP_PLUS:
                        self.set_less_basepoints(1)
                    if event.key == pygame.K_UP:
                        self.set_less_basepoints(1)
                    if event.key == pygame.K_F1:
                        self.show_help = not self.show_help
                    if event.key == pygame.K_KP_MINUS:
                        self.set_steps_down(1)
                    if event.key == pygame.K_DOWN:
                        self.set_steps_down(1)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    speed = 0.5
                    self.a_polyline.add_point(event.pos[0], event.pos[1],
                                              random()*speed, random()*speed)
            self.next_step()
        pygame.display.quit()
        pygame.quit()

    def next_step(self):
        self.gameDisplay.fill((0, 0, 0))
        self.hue = (self.hue + 1) % 360
        self.color.hsla = (self.hue, 100, 50, 100)
        self.a_polyline.draw_points()
        if self.show_closed_curve:
            self.a_polyline.get_knot(self.steps, 3, self.color)
        if not self.pause:
            self.a_polyline.set_points()
        if self.show_help:
            self.draw_help()
        pygame.display.flip()

    def set_less_basepoints(self, steps):
        self.steps += steps

    def set_steps_down(self, steps):
        self.steps -= steps if self.steps > 1 else 0

    def get_steps(self):
        return self.steps

    def draw_help(self):
        """функция отрисовки экрана справки программы"""
        steps = self.get_steps()
        self.gameDisplay.fill((50, 50, 50))
        font1 = pygame.font.SysFont("courier", 24)
        font2 = pygame.font.SysFont("serif", 24)
        data = []
        data.append(["F1", "Show Help"])
        data.append(["R", "Restart"])
        data.append(["P", "Pause/Play"])
        data.append(["H", "Hide/Show curve"])
        data.append(["Num+", "More points"])
        data.append(["UP", "More points"])
        data.append(["Num-", "Less points"])
        data.append(["DOWN", "Less points"])
        data.append(["", ""])
        data.append([str(steps), "Current points"])
        pygame.draw.lines(self.gameDisplay, (255, 50, 50, 255), True, [
            (0, 0), (800, 0), (800, 600), (0, 600)], 5)
        for i, text in enumerate(data):
            self.gameDisplay.blit(font1.render(
                text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
            self.gameDisplay.blit(font2.render(
                text[1], True, (128, 128, 255)), (200, 100 + 30 * i))


# =======================================================================================
# Основная программа
# =======================================================================================
if __name__ == "__main__":
    client = Game(caption="MyScreenSaver", screen_dim=SCREEN_DIM)
    client.start()
    exit(0)
