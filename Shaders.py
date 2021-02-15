import abc


class Shader (abc.ABC):
    """Абстрактный класс для шейдеров - поверхностей фигур"""
    pass


    @abc.abstractmethod
    def get_color (self, scene, current_shape, p, in_vector, r_level):
        """Возвращает цвет с точки поверхности, с учетом отраженных лучей с других объектов"""
        pass


class ShaderDiffuse (Shader):
    """Шейдер для диффузного рассеивания"""

    def __init__ (self, color):
        self.color = color


    def get_color (self, scene, current_shape, p, in_vector, r_level):
        # определим освещенность текущей точки с учетом теней
        illumination = 0

        for light in scene.lights:
            # проверим, не загораживает ли этот источник света какой-нибудь объект
            if not scene.check_is_cross_exist (p, light.get_vec_from_point (p), 0.0000001):
                illumination += light.get_strength (p, current_shape.get_normal (p))

        # умножаем цвет на освещенность и возвращаем результат
        # можно было бы еще отследить луч по нормали и добавить цвет из него, но пока оставим так
        return [int (c * illumination) for c in self.color]


class ShaderGlossy (Shader):
    """Шейдер для зеркальных отражений"""

    def get_color (self, scene, current_shape, p, in_vector, r_level):
        # получим отраженный вектор
        out_vector = current_shape.get_reflection_vec (p, in_vector)
        # если луч пришел "из за горизонта", прекращаем трассировку
        if out_vector is None:
            return [0, 0, 0]
        # если отражение найдено, продолжаем трассировку луча с уменьшением уровня рекурсии
        return scene.get_color (p, out_vector, 0.0000001, r_level - 1)


class ShaderMix (Shader):
    """Шейдер для смешивания двух других шейдеров"""

    def __init__ (self, sh1, sh2, k):
        """При k=0 действует sh1, при k=1 действует sh2"""

        if k < 0: k = 0
        if k > 1: k = 1

        self.shader1 = sh1
        self.shader2 = sh2
        self.k = k


    def get_color (self, scene, current_shape, p, in_vector, r_level):
        # вычисляем оба цвета, затем смешиваем их
        color1 = self.shader1.get_color (scene, current_shape, p, in_vector, r_level)
        color2 = self.shader2.get_color (scene, current_shape, p, in_vector, r_level)

        return list (map (lambda a, b: int ((1 - self.k) * a + self.k * b), color1, color2))
