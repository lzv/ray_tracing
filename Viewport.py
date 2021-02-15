"""Здесь будут храниться параметры вьюпорта. Он находится на расстоянии 1 от камеры и перпендикулярен ее направлению, верх совпадает с верхом камеры"""

import random
import VUtils


class Viewport:

    def __init__ (self, width, height, camera):
        self.width = width
        self.height = height
        self.camera = camera

        # может быть не int
        self.center_x = width / 2
        self.center_y = height / 2

        self.scene_height = 1    # высота равна 1 в единицах сцены, ширина рассчитывается пропорционально
        self.scene_width = width / height


    def get_vector_from_camera (self, x, y, sample_number):
        """Преобразуем координаты на вьюпорте в вектор, выходящий из камеры

        При начале в положении камеры, вектор будет заканчиваться в соответствующем пикселе вьюпорта.
        Для поддержки сэмплов, вектор будет иметь рандомное смещение в пределах пиксела, кроме первого сэмпла"""

        # первый сэмпл пойдет точно в центр пикселя, остальные получат рандомные смещения в его пределах
        if sample_number > 0:
            x += random.random () - 0.5
            y += random.random () - 0.5

        # система координат сдвигается в центр, ось y направляется вверх
        x = x - self.center_x
        y = self.center_y - y

        # вычисляем координаты в единицах сцены
        x = (x / self.width) * self.scene_width
        y = (y / self.height) * self.scene_height

        # У камеры есть вектор от ее позиции до центра вьюпорта.
        # Прибавив к нему вектор от центра вьюпорта до самой точки, мы получим искомый результат.
        return VUtils.add_vec (
            self.camera.front_vector,
            VUtils.add_vec (
                VUtils.scale (self.camera.top_vector, y),
                VUtils.scale (self.camera.right_vector, x)
            )
        )
