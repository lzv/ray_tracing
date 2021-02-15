import abc
import VUtils


class Light (abc.ABC):
    """Класс для источников света"""

    @abc.abstractmethod
    def get_strength (self, p, N):
        """Метод возвращает силу освещения в зависимости от положения точки и нормали к поверхности"""
        pass


    @abc.abstractmethod
    def get_vec_from_point (self, p):
        """Возвращает вектор из точки в направлении источника света"""
        pass


class LightPoint (Light):
    """Точечный источник света"""

    def __init__ (self, x, y, z, intensity):
        self.position = (x, y, z)
        self.intensity = intensity


    def get_strength (self, p, N):
        # находим вектор из точки в источник света
        L = VUtils.sub_vec (self.position, p)
        # длина переданной нормали должна быть 1, найденный L нормализуем
        # рассчитываем падение освещения в зависимости от угла между нормалью и направлением на источник света
        k = VUtils.dot_product (VUtils.normalize (L), N)
        # если скалярное произведение меньше нуля, значит источник света "за горизонтом"
        if k < 0:
            return 0
        # теперь учитываем расстояние между точкой и источником света
        # добавляем 1 в знаменатель, что бы свет не становился ярче на близких дистанциях
        distance = VUtils.vlen (L)
        return self.intensity * k / (1 + distance * distance)


    def get_vec_from_point (self, p):
        return VUtils.sub_vec (self.position, p)


class LightDirectional (Light):
    """Направленный источник света"""

    def __init__ (self, direction, intensity):
        self.direction = direction
        self.intensity = intensity


    def get_strength (self, p, N):
        # найдем нормализованный вектор обратного направления света
        vec = VUtils.normalize (VUtils.scale (self.direction, -1))
        # рассчитываем падение освещения в зависимости от угла между нормалью и направлением на источник света
        k = VUtils.dot_product (vec, N)
        # если скалярное произведение меньше нуля, значит источник света "за горизонтом"
        if k < 0:
            return 0
        # для направленного источника яркость не зависит от расстояния
        return self.intensity * k


    def get_vec_from_point (self, p):
        return VUtils.scale (self.direction, -1)
