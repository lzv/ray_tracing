import VUtils


class Camera:
    """Это класс, описывающий камеру"""

    def __init__ (self, position, front_vector, top_vector):
        """Векторы должны быть единичной длины"""
        self.position = position
        self.front_vector = VUtils.normalize (front_vector)
        self.top_vector = VUtils.normalize (top_vector)

        # Вектор, направленный вправо, перпендикулярный имеющимся двум и единичной длины
        # Пригодится для вычислений векторов, выходящих из камеры
        # Умножаем на -1, т.к. из за левой системы координат он будет смотреть влево, чего нам не надо
        self.right_vector = VUtils.scale (VUtils.cross_product (front_vector, top_vector), -1)
