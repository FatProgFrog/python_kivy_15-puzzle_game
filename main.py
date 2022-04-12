from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from random import choice
from Tile import Tile
from kivy.uix.button import Button


'''
    0   1   2   3 ➝ x
0 [01][02][03][04]
1 [05][06][07][08]
2 [09][10][11][12]
3 [13][14][15][16]
↓
y
'''

class Main_menu(BoxLayout):
    '''
    Главное меню
    '''
    def __init__(self,):
        super().__init__()
        self.orientation = "vertical"
        self.cols = 2
        self.label_num = Label(text = str(self.cols))
        self.menu_new_game()

    def menu_win_game(self):
        '''
        Экран после победы
        '''
        self.clear_widgets()
        self.label_num = Label(text = str(self.cols))
        win_text = Label(text = "Вы победили!")
        spin = BoxLayout(orientation = "horizontal")
        button_minus = Button(text = "-")
        button_plus = Button(text = "+")
        button_minus.on_release = self.value_down
        button_plus.on_release = self.value_up
        
        self.add_widget(win_text)
        spin.add_widget(button_minus)
        spin.add_widget(self.label_num)
        spin.add_widget(button_plus)
        
        button_start = Button(text = "Начать новую игру")
        button_start.on_release = self.start_form
        self.add_widget(spin)
        self.add_widget(button_start)

    def menu_new_game(self):
        '''
        Стартовое меню
        '''
        spin = BoxLayout(orientation = "horizontal")
        button_minus = Button(text = "-")
        button_plus = Button(text = "+")
        button_minus.on_release = self.value_down
        button_plus.on_release = self.value_up

        spin.add_widget(button_minus)
        spin.add_widget(self.label_num)
        spin.add_widget(button_plus)
        
        button_start = Button(text = "Начать новую игру")
        button_start.on_release = self.start_form
        self.add_widget(spin)
        self.add_widget(button_start)

    def value_up(self):
        '''
        Увеличиваем сторону доски
        '''
        if self.cols < 12:
            self.cols += 1
            self.label_update()

    def value_down(self):
        '''
        Уменьшаем сторону доски
        '''
        if self.cols > 2:
            self.cols -= 1
            self.label_update()

    def label_update(self):
        '''
        Обновляем для пользователя
        '''
        self.label_num.text = str(self.cols)

    def start_form(self):
        '''
        Запуск самой игры
        '''
        self.clear_widgets()
        self.add_widget(Main_form(self.cols))


class Main_form(GridLayout):
    '''
    Главное окно
    '''
    def __init__(self, cols):
        super().__init__()
        self.cols = cols
        self.field_list = []                            #Поле по игрекам
        self.puzzle_tile = self.button_build()          #Получаем последнюю пятнашку
        self.shuffle()                                  #Взбалтываем, но не смешиваем
        
    def button_build(self) -> Tile:
        '''
        Собирает поле для пятнашек и возвращает закрытую пятнашку
        '''
        name = 1
        for y in range(0, self.cols):
            field_x = []
            for x in range(0, self.cols):
                puzzle_button = Tile(name, x, y, 2.3 / self.cols) #Волшебная цифра, которую делим на размер стороны поля, в размере шрифта, получена путём подбора
                puzzle_button.on_release = lambda button = puzzle_button: self.move_user(button)
                self.add_widget(puzzle_button)
                field_x.append(puzzle_button)
                if name == self.cols * self.cols:
                    puzzle_button.disabled = True
                    puzzle_button.text = ""
                    result = puzzle_button
                name += 1
            self.field_list.append(field_x)
        return result
                
    def add_puzzles(self):
        '''
        Размещение тайлов заново
        '''
        for y in self.field_list:
            for x in y:
                if x.text == str(self.cols * self.cols):
                    x.text = ""
                self.add_widget(x)

    def move_user(self, button: Tile):
        '''
        Перемещение пятнашки от самого пользователя
        '''
        self.move(button)
        if self.check_win_standart():
            self.clear_widgets()
            self.parent.menu_win_game()
            

    def move(self, button: Tile):
        '''
        Механика передвижения пятнашки
        '''
        if self.is_unit_difference(button):

            temp_name = self.puzzle_tile.get_name()
            self.puzzle_tile.set_name(button.get_name())
            self.puzzle_tile.disabled = False
            button.set_name(temp_name)
            button.disabled = True
            self.puzzle_tile = button

            self.field_list[self.puzzle_tile.get_y()][self.puzzle_tile.get_x()] = button
            self.field_list[button.get_y()][button.get_x()] = self.puzzle_tile

            self.clear_widgets()    #Очистка поля от тайлов
            self.add_puzzles()

    def is_unit_difference(self, button: Tile) -> bool:
        '''
        Проверка на соседнюю клетку, исключая диагональные
        '''
        tile_puzzle_x = self.puzzle_tile.get_x()
        tile_puzzle_y = self.puzzle_tile.get_y()
        button_x = button.get_x()
        button_y = button.get_y()
        if (tile_puzzle_x - button_x == 1 and tile_puzzle_y - button_y == 0 or          # Тайл справа
            tile_puzzle_x - button_x == -1 and tile_puzzle_y - button_y == 0 or         # Тайл слева
            tile_puzzle_x - button_x == 0 and tile_puzzle_y - button_y == 1 or          # Тайл снизу
            tile_puzzle_x - button_x == 0 and tile_puzzle_y - button_y == -1            # Тайл сверху
            ):
            return True
        else:
            return False

    def shuffle(self):
        '''
        Размешиваем сто раз каждую ячейку,
        но надо придумать что-нибудь получше
        '''
        for i in range(0, 100 * self.cols):
            difference = True
            while difference:
                button = choice(choice(self.field_list))
                if self.is_unit_difference(button):
                    self.move(button)
                    difference = False

    def check_win_standart(self) -> bool:
        '''
        Проверка на правильную комбинацию стандартного режима
        '''
        check = 1
        for y in self.field_list:
            for tile  in y:
                if int(tile.get_name()) != check:
                    return False
                check += 1
        return True

    


class PuzzleApp(App):

    def __init__(self) -> None:
        super().__init__()

    def build(self):
        return Main_menu()

if __name__ == "__main__":
    PuzzleApp().run()