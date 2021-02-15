from RenderCanvas import *
from tkinter import ttk
import re
import threading


class MainWindow:
    width = 1800
    height = 900
    title = 'Рендер - трассировщик лучей'
    other_thread = None

    def __init__ (self):
        # созднаем и настраиваем главное окно
        self.root = tk.Tk ()
        self.root.option_add ('*tearOff', tk.FALSE)
        self.root.title (self.title)
        self.root.resizable (False, False)
        self.root.iconphoto (True, tk.PhotoImage (file = 'icon.png'))

        # делаем, что бы окно появилось посередине экрана
        screen_size = [self.root.winfo_screenwidth (), self.root.winfo_screenheight ()]
        screen_center = [x // 2 for x in screen_size]
        self.root.geometry (str (self.width) + 'x' + str (self.height) + '+'
                            + str (screen_center [0] - self.width // 2) + '+' + str (screen_center [1] - self.height // 2))

        # создаем объект, где будет происходить рендер
        self.rcanvas = RenderCanvas (self.root, int (self.width / 1.5), self.height - 40)
        self.rcanvas.grid (column = 0, row = 0, rowspan = 5, padx = 20, pady = 20)

        # Настроим валидацию для поля ввода
        validate_fun = lambda val: re.match ('^[0-9]*$', val) is not None
        validate_command = (self.root.register (validate_fun), '%P')

        # разместим поле ввода и подпись к нему
        self.sample_count = tk.IntVar (self.root, value = 1)
        ttk.Label (self.root, text = "Количество сэмплов на пиксель:", background = "#f2f1f0").grid (column = 1, row = 0, pady = 20)
        ttk.Entry (self.root, textvariable = self.sample_count, width = 8, validate = 'key', validatecommand = validate_command)\
            .grid (column = 2, row = 0, padx = 20, pady = 20)

        # кнопка для запуска и остановки рендера
        self.button = ttk.Button (self.root, text = "Начать", command = self.start_render)
        self.button.grid (column = 1, row = 1, columnspan = 2)

        self.info_label = ttk.Label (self.root, text = "Для начала рендера нажмите кнопку Начать", background = "#f2f1f0", wraplength = 550)
        self.info_label.grid (column = 1, row = 2, columnspan = 2, pady = 20, sticky = 'w')

        # Делаем последнюю строку grid растяжимой, что бы в остальных все было компактно
        self.root.rowconfigure (4, weight = 1)


    def start_render (self):
        self.button ['text'] = 'Остановить'
        self.button ['command'] = self.stop_render
        self.rcanvas.allow_render = True
        self.other_thread = threading.Thread (
            target = self.rcanvas.run_render,
            args = (self.sample_count.get (), self.info_label, self.restore_state)
        )
        self.other_thread.start ()


    def stop_render (self):
        self.button ['text'] = 'Остановка...'
        self.button.state (['disabled'])
        self.rcanvas.allow_render = False


    def restore_state (self):
        self.button ['text'] = 'Начать'
        self.button ['command'] = self.start_render
        self.button.state (['!disabled'])
        self.info_label ['text'] = 'Рендер завершен'
        self.rcanvas.allow_render = False
        self.other_thread = None


    def run_loop (self):
        self.root.mainloop ()
