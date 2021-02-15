from Camera import *
from Viewport import *
from SceneObject import *
from Shapes import *
from Lights import *
from Shaders import *


class Scene:
    """Это класс для сцены - он содержит в себе все объекты сцены, включая камеру и настройки viewport-а"""

    def __init__ (self, width, height):

        # уровень окружающего света, который светит на все точки
        self.ambient_light = 0.1

        # указываем позицию камеры, ее направление и направление вверх
        self.camera = Camera ([0, 0, 0], [0, 0, 1], [0, 1, 0])

        # создаем объект Viewport
        self.viewport = Viewport (width, height, self.camera)

        self.lights = [
            LightPoint (1.5, 0, 5, 1.5),
            LightDirectional ((2, -2, 2), 0.9)
        ]

        self.scene_objects = [
            SceheObject (
                ShapeSphere (1, -1, 6, 1),
                ShaderDiffuse ((255, 0, 0))
            ),
            SceheObject (
                ShapeSphere (-1, 1, 6, 1),
                ShaderDiffuse ((0, 255, 0))
            ),
            SceheObject (
                ShapeSphere (1, 1, 6, 1),
                ShaderMix (
                    ShaderDiffuse ((0, 0, 255)),
                    ShaderGlossy (),
                    0.8
                )
            ),
            SceheObject (
                ShapeSphere (-1, -1, 6, 1),
                ShaderMix (
                    ShaderDiffuse ((0, 255, 255)),
                    ShaderGlossy (),
                    0.2
                )
            )
        ]


    def get_closest_cross_object (self, o, vec, min_t):
        """Возвращает кортеж с точкой пересечения и объектом, с которым пересечение произошло"""
        # t, точка пересечения и объект сцены
        result = [0, None, None]

        for co in self.scene_objects:
            for point in co.shape.get_cross_point (o, vec, min_t):
                if result [0] == 0 or result [0] > point [0]:
                    result [0] = point [0]
                    result [1] = point [1]
                    result [2] = co

        return result


    def check_is_cross_exist (self, o, vec, min_t):
        """Проверяем, есть ли пересечения луча с объектами сцены"""
        for co in self.scene_objects:
            if len (co.shape.get_cross_point (o, vec, min_t)) > 0:
                return True

        return False


    def get_color_begin (self, x, y, sample_number, bounces):
        """Возвращает цвет, видимый из камеры, для пикселя вьюпорта с указанными координатами"""

        vec = self.viewport.get_vector_from_camera (x, y, sample_number)
        return self.get_color (self.camera.position, vec, 1, bounces)


    def get_color (self, o, vec, min_t, r_level):
        """Возвращает цвет, который видит вектор vec, исходящий из точки o.

        Вектор vec выходит из точки o. Пересечения ищутся для точек o + t * vec при t > min_t.
        Если r_r_level = 0, то возвращаем черный цвет.
        Если пересечения не найдены, возвращаем окружающее освещение."""

        if r_level == 0:
            return [0, 0, 0]

        # ищем ближайшее пересечение с объектом
        cross_object = self.get_closest_cross_object (o, vec, min_t)

        # пересечений не найдено, возвращаем окружающее освещение
        if cross_object [1] is None:
            return [int (255 * self.ambient_light), int (255 * self.ambient_light), int (255 * self.ambient_light)]

        # найден объект, получаем цвет точки с его поверхности
        return cross_object [2].shader.get_color (self, cross_object [2].shape, cross_object [1], vec, r_level)
