import abc
import VUtils
import OtherUtils


class Shape (abc.ABC):
    """Абстрактный класс для фигур в сцене. Эти классы описывают только форму поверхности"""

    @abc.abstractmethod
    def get_cross_point (self, o, vec, min_t):
        """Возвращает точки пересечения или пустой кортеж

        Вектор vec выходит из точки o. Точки, лежащие на луче, удовлетворяют условию o + t * vec.
        Метод ищет точки пересечения с формой при t > min_t. Найденные точки возвращаются в кортеже,
        элемент которого - пара из t и координат найденной точки."""
        pass


    @abc.abstractmethod
    def get_normal (self, point):
        """Возвращает нормаль к поверхности в заданной точке. Принадлежность точки к поверхности не проверяется"""
        pass


    @abc.abstractmethod
    def get_reflection_vec (self, p, vec):
        """Возвращает вектор, отраженный от поверхности в точке p, но если угол с нормалью не больше 90"""
        pass


class ShapeSphere (Shape):
    """Класс для сфер"""

    def __init__ (self, x, y, z, r):
        self.center = [x, y, z]
        self.radius = r


    def get_cross_point (self, o, vec, min_t):
        # вектор из центра сферы в позицию камеры
        co = VUtils.sub_vec (o, self.center)

        # найдем компоненты для квадратного уравнения
        a = VUtils.dot_product (vec, vec)
        b = 2 * VUtils.dot_product (vec, co)
        c = VUtils.dot_product (co, co) - self.radius * self.radius

        # находим решения с учетом min_t
        result = [t for t in OtherUtils.quadratic_equation (a, b, c) if t > min_t]

        # возвращаем найденные t и соответствующие координаты точек
        return [(t, VUtils.add_vec (o, VUtils.scale (vec, t))) for t in result]


    def get_normal (self, point):
        # строим вектор от центра к указанной точке и нормализуем
        return VUtils.normalize (VUtils.sub_vec (point, self.center))


    def get_reflection_vec (self, p, vec):
        return VUtils.mirror_vector_under_90 (vec, self.get_normal (p))

