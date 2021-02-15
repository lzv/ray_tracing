"""Этот класс обслуживает объект bytearray, который содержит пиксели изображения

Методы класса PhotoImage выполняются долго, поэтому для частого доступа к байтам будет использоваться этот класс.
Раз в некоторое время эти байты будут отправляться в объект PhotoImage для показа пользователю."""

class ImageBytes:

    def __init__ (self, width, height):
        self.width = width
        self.height = height

        self.data = bytearray (width * height * 3) # по 3 байта на пиксель


    def _check_coords_ (self, x, y):
        """Проверяем, что координаты лежат в разрешенном диапазоне"""
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise IndexError ("Координаты выходят за границу диапазона")


    def __getitem__ (self, key):
        """Ключ должен быть последовательностью из двух int - эмуляция двумерного массива"""
        return self.get_pixel (key [0], key [1])


    def __setitem__ (self, key, value):
        """Ключ должен быть последовательностью из двух int - эмуляция двумерного массива"""
        self.set_pixel (key [0], key [1], value)


    def get_pixel (self, x, y):
        """Возвращает 3 байта - цвета указанного пикселя"""
        self._check_coords_ (x, y)
        start_byte = (y * self.width + x) * 3
        return self.data [start_byte : start_byte + 3]


    def set_pixel (self, x, y, pixel):
        """Записываем цвета указанного пикселя"""
        self._check_coords_ (x, y)
        start_byte = (y * self.width + x) * 3
        self.data [start_byte: start_byte + 3] = pixel  # в pixel должно быть ровно 3 компонента
