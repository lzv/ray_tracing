import tkinter as tk
from Scene import *
from ImageBytes import *


class RenderCanvas:
    """Класс представляет собой основной хранитель данных и управляющий процессом рендера"""

    bounces = 4          # количество отскоков луча до прекращения трассировки
    allow_render = False # разрешение на работу рендера

    def __init__ (self, parent, width, height):
        # создаем объект Canvas
        self.width = width
        self.height = height
        self.canvas = tk.Canvas (parent, width = width, height = height, bg = 'gray', borderwidth = 0)

        # создаем объект PhotoImage, т.к. это единственная возможность рисовать по пикселям,
        # не создавая объекты в Canvas, что будет очень долго и потребует много памяти.
        # Хотя и через PhotoImage.put () тоже не очень быстро, но все же получше.
        self.pimg = tk.PhotoImage (width = self.width, height = self.height)
        self.canvas.create_image (1, 1, image = self.pimg, anchor = 'nw')  # как ни странно, координаты 1 а не 0, иначе справа внизу получится рамка

        # Здесь же будет находиться и сцена
        self.scene = Scene (self.width, self.height)

        # Так же объект с байтами для изображения
        self.ibytes = ImageBytes (self.width, self.height)


    def run_render (self, samples, info_label, end_action):
        for sample_number in range (samples):
            if not self.allow_render:
                break

            info_text = 'Рендер сэмпла ' + str (sample_number + 1) + ': '

            for y in range (self.height):
                if not self.allow_render:
                    break

                for x in range (self.width):
                    if not self.allow_render:
                        break

                    info_label ['text'] = info_text + str ((y * self.width + x) / (self.width * self.height / 100)) [0:4] + "%"

                    color = self.scene.get_color_begin (x, y, sample_number, self.bounces)

                    # поправим цвета, если какая-то компонента больше 255
                    max_comp = max (color)
                    if max_comp > 255:
                        color = [int (comp * 255 / max_comp) for comp in color]

                    if sample_number == 0:
                        self.ibytes [x, y] = color
                    else:
                        old_color = self.ibytes [x, y]
                        self.ibytes [x, y] = map (lambda a, b: int ((a * sample_number + b) / (sample_number + 1)), old_color, color)

            # после каждого сэмпла обновляем картинку
            self.write_bytes_to_image ()

        end_action ()


    def get_ibyte_in_html (self, x, y):
        """Преобразуем пиксель из объекта ImageBytes в html-представление цвета"""
        result = '#'

        for color in self.ibytes [x, y]:
            color = hex (color) [2:4]                   # color всегда будет в промежутке [0, 255]
            if len (color) == 1: color = '0' + color

            result += color

        return result


    def write_bytes_to_image (self):
        """Записываем данные из объекта ImageBytes в PhotoImage для отображения пользователю"""
        rows = []

        for y in range (self.height):
            row = []
            for x in range (self.width):
                row.append (self.get_ibyte_in_html (x, y))
            rows.append ("{" + " ".join (row) + "}")

        # вероятно, это будет работать быстрей, чем вызывать put () для каждого пикселя
        self.pimg.put (" ".join (rows), (0, 0))


    def grid (self, *args, **kwargs):
        self.canvas.grid (*args, **kwargs)
