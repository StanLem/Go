# from tensorflow import keras


# Глобальные константы

SGF_TO_N = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9, 'k': 10, 'l': 11, 'm': 12,
  'n': 13, 'o': 14, 'p': 15, 'q': 16, 'r': 17, 's': 18, 't': 19, 'u': 20, 'v': 21, 'w': 22, 'x': 23, 'y': 24, 'z': 25}

N_TO_SGF = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h', 8: 'i', 9: 'j', 10: 'k', 11: 'l', 12: 'm',
  13: 'n', 14: 'o', 15: 'p', 16: 'q', 17: 'r', 18: 's', 19: 't', 20: 'u', 21: 'v', 22: 'w', 23: 'x', 24: 'y', 25: 'z'}

dimension = 9  # Размер сетки 1x1 - 26x26
'''net_wide = int(60*18/dimension)
border = int(100*18/dimension)
screen_scale = (dimension - 1) * net_wide + 2 * border'''

screen_scale = 1300  # Размер экрана
net_wide = int(screen_scale/(dimension+2))  # Ширина сетки
border = int(net_wide*1.5)  # Ширина окантовки

save_file = 'save.sgf'

WHITE = (210, 146, 80)
LIGHT = (250, 250, 250)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Глобальные переменные

auto_move = False  # Признак автоматического хода
turn_colour = 'B'  # Кто ходит: B - black, W - white
x, y = 0, 0  # Координаты курсора
alive_groups = []  # Неуязвимые группы любого цвета
alive_group_list = []
actual_group = []  # Группа в которую входит камень текущего хода
black_groups = []  # Группы камней в формате [группа1, 2, ...]
# где группа1 это [[камень1, 2, ...], [дыхание1, 2, ...], [протоглаз1, 2, ...], [глаз1, 2, ...]
black_group_list = []  # [black_groups на 1 ходу, black_groups на 2 ходу, ...]
black_group_eyes = []  # [[группа1, [протоглаз1, 2, ...], [глаз1, 2, ...]], [группа2, [...], [...]], ...]
black_group_eyes_list = []
black_index = []  # Получение группы по координате (квадрат с размерностью dimension со ссылкой на группу
komi = 6.5  # Компенсация за второй ход
rules = 'Japanese'
winner = []  # [цвет победителя, перевес по очкам]
black_score = 0  # Количество взятых чёрным игроком белых камней
black_score_list = []
black_territory = 0  # Количество очков территории под контролем чёрного игрока
white_groups = []  # Группы камней в формате [группа1, 2, ...]
# где группа1 это [[камень1, 2, ...], [дыхание1, 2, ...], [протоглаз1, 2, ...], [глаз1, 2, ...]
white_group_list = []
white_group_eyes = []
white_group_eyes_list = []
white_index = []  # Копия доски со ссылками на белую группу в каждой координате
white_score = komi
white_score_list = []
white_territory = 0
total_score = black_score - white_score
ally_groups = black_groups  # Группы цвета текущего хода
ally_index = black_index  # Индекс
enemy_groups = white_groups
enemy_index = white_index
influence = []  # (⬋, ⬉, ⬈, ⬊) Четырёх-векторное влияние
end_game = False

move_list = []  # Список всех ходов партии
move_count = 0  # Номер отображаемого хода в партии

# move_model = keras.models.load_model('AI/ai_fdddd_max_3')  # Подсказка хода

# win_model = keras.models.load_model('AI/AI_WIN-2-3-b1-e6_p50_38_a72')  # Предсказание победителя
# current_move = 'current_move.win'

field = []  # Расстановка камней на поле [[' ', 'B', ... 'W'], [...], ... [...]]
field_list = []  # Список расстановок на каждом ходу

dame_font = []
text_font = []
influence_font = []
background = []
screen = []
temp_background = background


