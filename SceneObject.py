class SceheObject:
    """Это класс для объектов сцены. Объект содержит в себе форму и шейдер его поверхности"""

    def __init__ (self, shape, shader):
        self.shape = shape
        self.shader = shader
