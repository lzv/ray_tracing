"""Здесь находятся различные полезные функции, которые не связаны с векторами"""

import math


def quadratic_equation (a, b, c):
    """Решаем квадратное уравнение a * x^2 + b * x + c = 0. Возвращается кортеж с нулем, одним или двумя решениями"""

    d = b * b - 4 * a * c
    if d > 0:
        s = math.sqrt (d)
        return (-b + s) / (2 * a), (-b - s) / (2 * a)
    elif d == 0:
        return -b / (2 * a),
    else:
        return ()


