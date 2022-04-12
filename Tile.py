'''
Класс для реализации тайла
'''
from kivy.uix.button import Button

class Tile(Button):
    '''
    Класс одного тайла (одной пятнашки)
    '''
    def __init__(self, name = 1, x = 0, y = 0, font_size = 0.6) -> None:
        super().__init__()
        self._name = name
        self.text = str(name)
        self._font_size_on_cols = font_size #Размер, зависящий от размера стороны поля
        self.font_size = self.width * self.height / 100 * self._font_size_on_cols
        self._x = x
        self._y = y

    #Геттеры
    def get_name(self) -> str:
        return str(self._name)

    def get_x(self) -> int:
        return self._x

    def get_y(self) -> int:
        return self._y

    def get_on_list(self, size_row) -> int:
        '''
        Вывод положения в одномерном массиве
        '''
        result = self.get_y * size_row + self._x
        return result
    
    #Сеттеры
    def set_name(self, value) -> None:
        self.text = str(value)
        self._name = value

    def set_x(self, value) -> None:
        self._x  = value

    def set_y(self, value) -> None:
        self._y = value

    def set_on_list(self, value, size_row) -> None:
        '''
        Преобразование из одномерного массива в двумерный
        '''
        self._y = value // size_row
        self._x = value % size_row - 1

    #Дополнительные методы

    def font_change(self):
        '''
        Метод сделан для адаптивности шрифта
        '''
        self.font_size = self.width * self.height / 100 * self.font_size