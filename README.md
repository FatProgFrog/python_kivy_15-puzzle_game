# python_kivy_15-puzzle_game

Игра "Пятнашки": визуал создан на фреймворке kivy без использования языка kv

Визуальная часть программы состоит из: 

```
Главное меню ┒
|	составной элемент "spin" ┒
|	|	Кнопка "-", понижающая значение количества ячеек стороны игровой доски; минимальное значение 2
|	|	Label, отображающий количество ячеек стороны игровой доски
|	|	Кнопка "+", понижающая значение количества ячеек стороны игровой доски; максимальное значение 12
|	Кнопка "Начать новую игру"
|
Доска с игрой ┒
|	    0   1   2   3 ➝ x	#Пример доски, количество ячеек стороны которой равно 4 
|	0 [01][02][03][04]
|	1 [05][06][07][08]
|	2 [09][10][11][12]
|	3 [13][14][15][16]	#16-й элемент неактивен, его значение равно "" пустой строке
|	↓
|	y
|
Меню победы ┒  #В игре проиграть невозможно
	Label с текстом "Вы победили!"
	составной элемент "spin" ┒
	|	Кнопка "-", понижающая значение количества ячеек стороны игровой доски; минимальное значение 2
	|	Label, отображающий количество ячеек стороны игровой доски
	|	Кнопка "+", понижающая значение количества ячеек стороны игровой доски; максимальное значение 12
	Кнопка "Начать новую игру"
```

В программе я использовал класс Main_menu, наследованный от BoxLayout,
в котором реализованна сборка главного меню и меню победы.
Класс Main_form, наследованный от GridLayout, содержит в себе
основную механику игры в пятнашки: Составление поля, система смешивания, проверка на победу.
Отдельным файлом вывел класс Tile, наследованный от Button, который выступает в роли одного элемента доски.

Система смешивания перемешивает элементы так, как это делал бы пользователь, 
но в произвольном порядке, что позволяет избежать нерешаемых комбинаций.

Проект был создан для понимания взаимодействий классов между собой и для поиска необходимых методов реализации.
