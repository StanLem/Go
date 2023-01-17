import time
import globals as gl
from copy import deepcopy as copy
import draw
import numpy as np
import tkinter as tk
import tkinter.filedialog as fd


def add_black_groups_list():
    if gl.black_groups:
        gl.black_group_list.append(copy(gl.black_groups))
    else:
        gl.black_group_list.append([[[], []]])


def add_group(x, y):
    dame = []
    if y != 0: # Запоминаем соседние точки
        up_neighbour = gl.field[x][y-1]
        if up_neighbour == ' ':
            dame.append((x, y-1))
    else:
        up_neighbour = 'x'
    if y != gl.dimension-1:
        down_neighbour = gl.field[x][y+1]
        if down_neighbour == ' ':
            dame.append((x, y+1))
    else:
        down_neighbour = 'x'
    if x != 0:
        left_neighbour = gl.field[x-1][y]
        if left_neighbour == ' ':
            dame.append((x-1, y))
    else:
        left_neighbour = 'x'
    if x != gl.dimension-1:
        right_neighbour = gl.field[x+1][y]
        if right_neighbour == ' ':
            dame.append((x+1, y))
    else:
        right_neighbour = 'x'

    gl.ally_groups.append([[(x, y)], dame]) # Создаём новую группу для точки x, y

    for group in gl.ally_groups:   # Запоминаем новую группу
        for dot in group[0]:
            if dot == (x, y):
                gl.actual_group = group
                gl.ally_index[x][y] = gl.actual_group

        # Добавляем всех соседей в группу с новой точкой
    if (up_neighbour == 'B' and gl.turn_colour == 'B') or (up_neighbour == 'W' and gl.turn_colour == 'W'):
        add_neighbour((x, y-1))
    if (down_neighbour == 'B' and gl.turn_colour == 'B') or (down_neighbour == 'W' and gl.turn_colour == 'W'):
        add_neighbour((x, y+1))
    if (left_neighbour == 'B' and gl.turn_colour == 'B') or (left_neighbour == 'W' and gl.turn_colour == 'W'):
        add_neighbour((x-1, y))
    if (right_neighbour == 'B' and gl.turn_colour == 'B') or (right_neighbour == 'W' and gl.turn_colour == 'W'):
        add_neighbour((x+1, y))

    del_dame()


def add_field_list():
    gl.field_list.append([])
    for n in range(0, gl.dimension):
        gl.field_list[-1].append([])
    for line in range(0, gl.dimension):
        for column in range(0, gl.dimension):
            gl.field_list[-1][line].append(gl.field[line][column])


def add_neighbour(neighbour):
    ally_group = gl.ally_index[neighbour[0]][neighbour[1]]
    for dot in ally_group[0]: # IndexError: list index out of range - 1 dame rotate capture
        if dot not in gl.actual_group[0]:
            gl.actual_group[0].append(dot) # ERROR freeze FIXED
            gl.ally_index[dot[0]][dot[1]] = gl.actual_group # ERROR Freeze FIXED
        else:
            return False
    for dame in ally_group[1]:
        if dame not in gl.actual_group[1] and dame != gl.actual_group[0][0]:
            gl.actual_group[1].append(dame)
    for group in range(len(gl.ally_groups)):
        if gl.ally_groups[group] == ally_group:
            del gl.ally_groups[group]
            break


def add_white_groups_list():
    if gl.white_groups:
        gl.white_group_list.append(copy(gl.white_groups))
    else:
        gl.white_group_list.append([[[], []]])


def ai_move():
    1 == 1
    '''x = field_to_tensor(gl.field)
    x = np.expand_dims(x, axis=0)
    y = gl.move_model.predict(x)

    max_ten = [[(0, 0)], [y[0][0]]]
    i = 1
    for elem in y[0]:
        for j in range(0, len(max_ten[0])):
            if elem > max_ten[1][j]:
                max_ten[0].insert(j, (i // 19, i % 19))
                max_ten[1].insert(j, elem)
                if len(max_ten[0]) > 10:
                    del max_ten[0][-1]
                    del max_ten[1][-1]
                break
        i += 1

    draw.ai_move(max_ten)
    print(max_ten)
    print()
    i = 0
    line = []
    for elem in y[0]:
        if elem >= max_ten[1][-1]:
            line.append(0)
        else:
            line.append(7)
        if i == 18:
            print(line)
            line = []
            i = 0
        else:
            i += 1'''


def ai_move_algo():

    max_score_move = (-1, -1)
    score = gl.black_score + gl.black_potential if gl.turn_colour == 'B' else gl.white_score + gl.white_potential
    max_score = score
    max_attack_move = (-1, -1)
    enemy_dame = 0
    enemy_weak = 0
    for group in gl.enemy_groups:
        enemy_dame += len(group[1])
        if len(group[1]) == 1:
            enemy_weak += 1
    max_defence_move = (-1, -1)
    ally_dame = 0
    ally_weak = 0
    for group in gl.ally_groups:
        ally_dame += len(group[1]) # Снижаем стоимость собственных групп по сравнению с группами противника
        if len(group[1]) == 1:
            ally_weak += 1
    change_dame = ally_dame - enemy_dame
    weak_change = ally_weak
    max_weak_change = weak_change
    max_change_dame = change_dame
    a = 1
    b = 2
    c = 0
    current_points = a*abs(score) + b*change_dame - c*weak_change
    max_points = current_points
    max_points_move = (-1, -1)

    for x in range (0, gl.dimension):
        for y in range (0, gl.dimension):
            dot = (x, y)
            if gl.field[x][y] == ' ':
                if move(x, y):
                    score = gl.black_score + gl.black_potential if gl.turn_colour == 'W' else gl.white_score + gl.white_potential
                        # W - Так как цвет после хода изменился
                    change_dame = 0
                    for group in gl.ally_groups:
                        change_dame += len(group[1])
                        if len(group[1]) == 1:
                            weak_change += 1
                    for group in gl.enemy_groups:
                        change_dame -= len(group[1])

                    current_points = a*abs(score) + b*change_dame - c*weak_change

                    if current_points > max_points:
                        max_points = current_points
                        max_points_move = dot
                    backward()

    if max_points_move != (-1, -1):
        print('points', max_points)
        move(max_points_move[0], max_points_move[1])
    #elif max_attack_move != (-1, -1):
        #move(max_attack_move[0], max_attack_move[1])
    #elif max_score_move != (-1, -1):
        #move(max_score_move[0], max_score_move[1])
    else:
        pass_move()

    draw.all()


def backward(): # Отобразить предыдущий ход партии
    if gl.move_count > 1 and gl.move_count <= len(gl.move_list):
        gl.move_count -= 1
        set_globals(gl.move_count - 1)
        gl.end_game = False


def change_colour(): # Изменения цветовых переменных после завершения хода

    if gl.turn_colour == 'B':
        gl.turn_colour = 'W'
        gl.ally_groups = gl.white_groups
        gl.ally_index = gl.white_index
        gl.enemy_groups = gl.black_groups
        gl.enemy_index = gl.black_index
    else:
        gl.turn_colour = 'B'
        gl.ally_groups = gl.black_groups
        gl.ally_index = gl.black_index
        gl.enemy_groups = gl.white_groups
        gl.enemy_index = gl.white_index


def choose_file():

    root = tk.Tk()
    '''root.lift()
    root.attributes('-topmost', True)
    root.after_idle(root.attributes, '-topmost', False)'''

    filetypes = (("Партия Го", "*.sgf"),
                 ("Текстовый файл", "*.txt"),
                 ("Изображение", "*.jpg *.gif *.png"),
                 ("Любой", "*"))
    filename = fd.askopenfilename(title="Открыть файл",
                                  initialdir="C:/Users/Станислав/PycharmProjects/Fractal/My_Projects/Go",
                                  filetypes=filetypes)
    root.destroy()
    return filename


def chose_dir():

    root = tk.Tk()
    folder = fd.askdirectory(title="Выбрать папку",
                             initialdir="C:/Users/Станислав/PycharmProjects/Fractal/My_Projects/Go")
    root.destroy()
    return folder


def count_influence():

    gl.influence = []
    for n in range(0, gl.dimension):
        gl.influence.append([])
        for m in range (0, gl.dimension):
            gl.influence[n].append([0, 0, 0, 0])

    update_influence(gl.black_groups, 1)
    update_influence(gl.white_groups, -1)


def count_territory():

    gl.black_potential = 0
    gl.white_potential = 0
    for x in range(0, gl.dimension):
        for y in range(0, gl.dimension):
            sum = gl.influence[x][y][0] + gl.influence[x][y][1] + gl.influence[x][y][2] + gl.influence[x][y][3]
            if sum > 0:
                gl.black_potential += 1
            elif sum < 0:
                gl.white_potential += 1


def count_score():

    count_influence()
    count_territory()
    # total_score = gl.black_score + gl.black_potential - white_score - gl.white_potential
    gl.total_score = gl.black_score - gl.white_score


def count_eyes():  # Неуязвимые группы попадают в список gl.alive_groups

    gl.alive_groups = []

    def mark_group_eyes(color_groups):

        color_group_eyes = []  # Будем пересоздавать список групп с глазами
        all_proto_eye_list = []
        proto_eye_groups_list = []  # [proto, [group1, group2, ...]]  Список протоглаз и окружающих его групп
        color = 'B' if color_groups == gl.black_groups else 'W'

        for group in color_groups:

            eye_list = []
            proto_eye_list = []

            for dame in group[1]:  # Проверяем, какие дыхания группы являются глазами

                eye = 0  # Если со всех сторон дыхание окружено друзьями, то оно является глазом
                proto_eye = 0  # если только с 4-х главных сторон - протоглазом
                wall = 0  # Наличие стенок рядом с дыханием

                if dame[0] != 0:  # Слева не стена
                    if gl.field[dame[0] - 1][dame[1]] == color:  # Проверяем камень слева
                        eye += 1
                        proto_eye += 1
                    if dame[1] != 0:  # Сверху не стена
                        if gl.field[dame[0] - 1][dame[1] - 1] == color:  # Проверяем камень слева сверху
                            eye += 1
                else:
                    wall += 1  # Обозначаем стену слева

                if dame[1] != 0:  # Сверху не стена
                    if gl.field[dame[0]][dame[1] - 1] == color:  # Проверяем камень сверху
                        eye += 1
                        proto_eye += 1
                    if dame[0] != gl.dimension - 1:  # Справа не стена
                        if gl.field[dame[0] + 1][dame[1] - 1] == color:  # Проверяем камень сверху справа
                            eye += 1
                else:
                    wall += 1  # Обозначаем стену сверху

                if dame[1] != gl.dimension - 1:  # Снизу не стена
                    if gl.field[dame[0]][dame[1] + 1] == color:  # Проверяем камень снизу
                        eye += 1
                        proto_eye += 1
                    if dame[0] != 0:  # Слева не стена
                        if gl.field[dame[0] - 1][dame[1] + 1] == color:  # Проверяем камень снизу слева
                            eye += 1
                else:
                    wall += 1  # Обозначаем стену снизу

                if dame[0] != gl.dimension - 1:  # Справа не стена
                    if gl.field[dame[0] + 1][dame[1]] == color:  # Проверяем камень справа
                        eye += 1
                        proto_eye += 1
                    if dame[1] != gl.dimension - 1:  # Снизу не стена
                        if gl.field[dame[0] + 1][dame[1] + 1] == color:  # Проверяем камень снизу справа
                            eye += 1
                else:
                    wall += 1  # Обозначаем стену справа

                if wall + proto_eye == 4:  # Похоже на глаз - протоглаз
                    if (wall == 0 and eye >= 7) or \
                            (wall == 1 and eye == 5) or \
                            (wall == 2 and eye == 3):  # Сформированный глаз
                        eye_list.append(dame)
                    proto_eye_list.append(dame)
                    if dame not in all_proto_eye_list:
                        all_proto_eye_list.append(dame)
                        proto_eye_groups_list.append([dame, [group]])  # Добавление пар протоглаз-группа

            color_group_eyes.append([group, proto_eye_list, eye_list])  # Заново формируем список групп с глазами

            for proto in proto_eye_list:  # Обновление групп в списке протоглаз
                for eye_group in proto_eye_groups_list:
                    if proto == eye_group[0]:
                        if group not in eye_group[1]:
                            eye_group[1].append(group)

        proto_eye_connected_list = []  # Список списков соединённых протоглазами групп
        # Можно решить с помощью рекурсии *
        part_connected_list = []  # Список соединённых протоглаз
        connected_proto = []  # Список уже просмотренных протоглаз

        for proto in all_proto_eye_list:
            if proto not in connected_proto:
                connected_proto.append(proto)
                part_connected_list.append(proto)
                for group in color_group_eyes:
                    for proto in part_connected_list:
                        if proto in group[1]:  # Если у группы есть этот пг
                            for proto_ in group[1]:  # то добавляем все её пг в список
                                if proto_ not in part_connected_list:
                                    part_connected_list.append(proto_)
                                    connected_proto.append(proto_)
                proto_eye_connected_list.append(part_connected_list)
                part_connected_list = []

        '''connected_groups = []  # [Список групп, Общие протоглаза]
        copy_color_group_eyes = copy(color_group_eyes)
        for group1 in color_group_eyes:
            copy_color_group_eyes.remove(group1)
            for group2 in copy_color_group_eyes:
                connection = []
                for proto in group1[1]:
                    if proto in group2[1]:
                        connection.append(proto)
                connected_groups.append([[group1, group2], connection])'''

        eye_list = []

        for proto_group in proto_eye_connected_list:  # Если все соединённые протоглазами группы имеют по 2 протоглаза

            group_to_check_list = []  # Список групп у которых должно быть по 2 протоглаза
            group_checked_list = []  # Список групп у которых есть 2 протоглаза

            proto_group_ = copy(proto_group)  # Техническая замена, будем менять вплоть до нуля итерируемое значение

            # Удалить из группы все глаза, соединённые со слабой группой (меньше одного протоглаза)

            def delete_false_proto(group_of_proto, to_delete_list):

                for proto in group_of_proto:
                    to_delete = False
                    for proto_group__ in proto_eye_groups_list:
                        if proto == proto_group__[0]:  # Признак слабой группы
                            for group in proto_group__[1]:
                                for group_ in color_group_eyes:
                                    if group == group_[0]:
                                        num_of_invalid_protos = 0
                                        for proto_ in group_[1]:
                                            if proto_ in to_delete_list:
                                                num_of_invalid_protos += 1
                                        if len(group_[1]) - num_of_invalid_protos <= 1:
                                            to_delete = True
                    if to_delete and proto not in to_delete_list:  # Группа
                        to_delete_list.append(proto)

                for proto in to_delete_list:
                    if proto in group_of_proto:
                        group_of_proto.remove(proto)

                return group_of_proto, to_delete_list

            before = []
            after = copy(proto_group_)
            to_delete_list = []
            while before != after:
                before = copy(after)
                after, to_delete_list = delete_false_proto(copy(before), to_delete_list)
            proto_group_ = after

            if proto_group_:

                for ch_group in color_groups:
                    for ch_dame in ch_group[1]:
                        if ch_dame in proto_group_ and ch_group not in group_to_check_list:
                            group_to_check_list.append(ch_group)
                            break

                for ch_group in group_to_check_list:
                    for eyed_group in color_group_eyes:
                        if ch_group == eyed_group[0]:
                            if len(eyed_group[1]) >= 2:  # Количество протоглаз у всех групп должно быть не меньше 2
                                group_checked_list.append(ch_group)

                if len(group_to_check_list) == len(group_checked_list):
                    for proto in proto_group_:
                        eye_list.append(proto)

        for proto in eye_list:
            for gr_num in range(0, len(color_group_eyes)):  # proto является глазом
                if proto in color_group_eyes[gr_num][1] and proto not in color_group_eyes[gr_num][2]:
                    color_group_eyes[gr_num][2].append(proto)  # Обозначаем proto как Глаз

        return color_group_eyes

    gl.black_group_eyes = mark_group_eyes(gl.black_groups)
    gl.black_group_eyes_list.append(copy(gl.black_group_eyes))

    gl.white_group_eyes = mark_group_eyes(gl.white_groups)
    gl.white_group_eyes_list.append(copy(gl.white_group_eyes))

    sum_group = gl.black_group_eyes + gl.white_group_eyes

    for group_to_add in sum_group:
        if len(group_to_add[2]) >= 2:  # Все группы с 2 глазами считаются живыми
            gl.alive_groups.append(group_to_add[0])


def cut_history_tail():

    while gl.move_count < len(gl.move_list):  # Удаление всех ходов с номером > текущего хода
        del gl.alive_group_list[-1]
        del gl.black_group_eyes_list[-1]
        del gl.black_group_list[-1]
        del gl.black_score_list[-1]
        del gl.field_list[-1]
        del gl.move_list[-1]
        del gl.white_group_eyes_list[-1]
        del gl.white_group_list[-1]
        del gl.white_score_list[-1]


def del_dame():  # Удаляем лишние дыхания и умершие группы
    deleted = 0
    for group in range(len(gl.enemy_groups)):
        for dame in gl.enemy_groups[group][1]:
            if dame == gl.actual_group[0][0]:
                gl.enemy_groups[group].append([]) # ERROR 'tuple' object has no attribute 'append'
                for dame_ in gl.enemy_groups[group][1]:
                    if dame_ != gl.actual_group[0][0]:
                        gl.enemy_groups[group][2].append(dame_) # Создаём новый список дыханий
                del gl.enemy_groups[group][1] # Удаляем старый список дыханий
                if len(gl.enemy_groups[group][1])==0: # Если дыханий не остаётся - удаляем группу
                    if gl.turn_colour == 'B':
                        gl.black_score += len(gl.enemy_groups[group][0])
                    else:
                        gl.white_score += len(gl.enemy_groups[group][0])
                    for dot in gl.enemy_groups[group][0]:# Очистка поля
                        gl.field[dot[0]][dot[1]] = ' '
                        gl.enemy_index[dot[0]][dot[1]] = []
                        restore_dame(dot)
                    del gl.enemy_groups[group]
                    deleted = 1
                    break
        else:
            continue
        break
    if deleted == 1:
        del_dame()


def field_to_tensor(field_):
    tensor_ = []
    for raw in range(0, 19):
        tensor_.append([])
        for col in range(0, 19):
            if field_[raw][col] == ' ':
                tensor_[raw].append([1, 0, 0])
            elif field_[raw][col] == 'B':
                tensor_[raw].append([0, 1, 0])
            else:  # 2
                tensor_[raw].append([0, 0, 1])
    return tensor_


def forward(): # Отобразить следующий ход партии
    if len(gl.move_list) > gl.move_count:
        gl.move_count += 1
        set_globals(gl.move_count - 1)


def load_party(filename):

    draw.massage(' Загрузка партии')

    if filename != '':
        print('Open party', filename)
        file = open(filename, 'r', encoding='UTF-8')
        try:
            file = file.read()
        except UnicodeDecodeError:
            print('UnicodeDecodeError')
            return False
        if len(file) == 0:
            print('file is empty')
            return False
        if '[t' in file:
            print('>19 field')
            return False
        if 't]' in file:
            print('>19 field')
            return False
        file = file.replace('\n', '')
        file = file.replace('AB[', ';AB[')  # AB обозначает фору
        file = file.split(';')

        new_game()
        try:
            gl.komi = file[1].split('KM[')[1]
            gl.komi = gl.komi.split(']')[0]
            gl.komi = float(gl.komi)  # Если не указано коми, устанавливаем значение по умолчанию
        except IndexError:
            print('komi default')
            gl.komi = 7.5
        except ValueError:
            print('komi default')
            gl.komi = 7.5
        gl.white_score = gl.komi

        for word in file:
            gl.auto_move = True

            if word[0] == 'B' or word[0] == 'W':
                x = gl.SGF_TO_N[word[2]]  # вылет при загрузке первой партии alpha zero 40 vs self (поле 20 на 20)
                y = gl.SGF_TO_N[word[3]]
                if word[0] == gl.turn_colour:
                    move(x, y)
                else:
                    pass_move()
                    move(x, y)
            elif word[0] == 'A' and word[1] == 'B':
                x = gl.SGF_TO_N[word[3]]
                y = gl.SGF_TO_N[word[4]]
                move(x, y)
                change_colour()
                x = gl.SGF_TO_N[word[7]]
                y = gl.SGF_TO_N[word[8]]
                move(x, y)
            else:
                print(filename, word)

        gl.auto_move = False
        return True
    else:
        print('file choose canceled')
        return False



def load_party_for_mine(filename):

    draw.massage(filename)

    if filename != '':
        print('Open party', filename)
        file = open(filename, 'r', encoding='UTF-8')
        try:
            file = file.read()
        except UnicodeDecodeError:
            print('UnicodeDecodeError')
            return False
        if '[t' in file:
            print('>19 field')
            return False
        if 't]' in file:
            print('>19 field')
            return False
        file = file.replace('\n', '')
        file = file.replace('AB[', ';AB[')
        file = file.split(';')

        new_game()
        try:  # Выбираем только партии с коми
            gl.komi = file[1].split('KM[')[1]
            gl.komi = gl.komi.split(']')[0]
            gl.komi = float(gl.komi)  # Если не указано коми, то не собираем данные
        except IndexError:
            print('komi error')
            return False
        except ValueError:
            print('komi error')
            return False
        gl.white_score = gl.komi
        try:
            gl.rules = file[1].split('RU[')[1]
            gl.rules = gl.rules.split(']')[0]
            if 'apanese' in gl.rules:
                gl.rules = 'Japanese'
                print('invalid rules', gl.rules)
                return False
            elif 'hinese' in gl.rules:
                gl.rules = 'Chinese'
            elif 'orea' in gl.rules:
                gl.rules = 'Korean'
                print('invalid rules', gl.rules)
                return False
            else:
                print('invalid rules', gl.rules)
                return False
        except IndexError:
            print('no rules')
        try:
            win_c = file[1].split('RE[')[1]
            win_c = win_c.split(']')[0]  # Получаем содержимое блока RE[ ]
            if '+' in win_c:
                # print('+ notation')
                # return False # Уже собрал данные в нотации +
                win_c = win_c.split('+')  # для нотации B+2, W+R
                gl.winner.append(win_c[0])
                gl.winner.append(int(win_c[1]))  # Если не указан счёт, то не собираем данные
            elif '胜' in win_c and '中' not in win_c:
                win_c = win_c.replace('胜', '')  # иероглиф победа
                if '白' in win_c:
                    gl.winner.append('W')
                    win_c = win_c.split('白')[1]  # Избавляемся от комментария вначале
                elif '黑' in win_c:
                    gl.winner.append('B')
                    win_c = win_c.split('黑')[1]  # Избавляемся от комментария вначале
                else:
                    print('error win', win_c)
                    return False
                if win_c == '' or '棋超时' in win_c:
                    print('error win', win_c)
                    return False
                else:  # Если есть очки, то считываем значение
                    if '目' in win_c or '点' in win_c:
                        win_c = win_c.split('!')[0]  # Отбрасываем восклицания и комменты после них
                        win_c = win_c.replace('目', '')
                        win_c = win_c.replace('点', '')
                    half = 0.0
                    if '半' in win_c:  # признак добавочной половины очка
                        half = 0.5
                        win_c = win_c.replace('半', '')
                    win_c = win_c.replace('子', '')  # Убираем предлог 'с'
                    if '又' in win_c:
                        win_c = win_c.split('又')[0]  # Отбрасываем всё что справа от 又, это 0.5
                        half = 0.5
                    if win_c == '':
                        win_c = 0.0
                    elif '/' in win_c:
                        win_c = 0.5
                    try:
                        win_c = float(win_c)  # Если число записано иероглифом
                    except ValueError:
                        win_c = win_c.replace('三十一', '31')
                        win_c = win_c.replace('二十一', '21')
                        win_c = win_c.replace('十一', '11')
                        win_c = win_c.replace('一', '1')
                        win_c = win_c.replace('十二', '12')
                        win_c = win_c.replace('二', '2')
                        win_c = win_c.replace('三', '3')
                        win_c = win_c.replace('四', '4')
                        win_c = win_c.replace('五', '5')
                        win_c = win_c.replace('六', '6')
                        win_c = win_c.replace('十七', '17')
                        win_c = win_c.replace('七', '7')
                        win_c = win_c.replace('八', '8')
                        win_c = win_c.replace('九', '9')
                        win_c = win_c.replace('十', '10')
                    gl.winner.append(float(win_c) + half)
            else:
                print('win error', win_c)
                return False
        except IndexError:
            print('error win')
            return False
        except ValueError:
            print('error win', win_c)
            return False

        for word in file:
            if word[0] == 'B' or word[0] == 'W':
                x = gl.SGF_TO_N[word[2]]  # вылет при загрузке первой партии alpha zero 40 vs self (поле 20 на 20)
                y = gl.SGF_TO_N[word[3]]
                if word[0] == gl.turn_colour:
                    move(x, y)
                else:
                    pass_move()
                    move(x, y)
            elif word[0] == 'A' and word[1] == 'B':
                x = gl.SGF_TO_N[word[3]]
                y = gl.SGF_TO_N[word[4]]
                move(x, y)
                change_colour()
                x = gl.SGF_TO_N[word[7]]
                y = gl.SGF_TO_N[word[8]]
                move(x, y)
            else:
                print(filename, word)
        return True
    else:
        print('file choose canceled')


def mine_data(mypath):

    if mypath:
        from os import listdir
        from os.path import isfile, join
        games = [f for f in listdir(mypath) if isfile(join(mypath, f))]

        enable = True  # Начиная с какого номера майнить если установлено False
        for game in games:  # text
            '''if game == '15001.sgf' and not enable:
                enable = True
            if game == '25000.sgf':
                break'''
            if enable:
                if load_party_for_mine(mypath + '/' + game):
                    # for move_number in range(0, int(0.1*len(gl.move_list))): # 10% последних ходов считаем победными
                    for rotation in range(0, 8):  # Вращаем во все стороны
                        save_moves_win('DATA/go_wins_jap.txt')
                        rotate()
                        if rotation == 3:
                            mirror()
                        # back()
        print('data mined')
    else:
        print('data mine canceled')


def mirror(): # Отразить позицию по оси y
    if len(gl.move_list) > 0:
        mirror_field()
        gl.black_groups = mirror_groups(gl.black_groups)
        gl.black_group_list[gl.move_count - 1] = copy(gl.black_groups)
        gl.white_groups = mirror_groups(gl.white_groups)
        gl.white_group_list[gl.move_count - 1] = copy(gl.white_groups)
        gl.field_list[gl.move_count-1] = copy(gl.field)
        mirror_move()
        change_colour() # Обновление переменных индексов
        change_colour()


def mirror_field(): # Отразить позицию по оси y: (n-1-x, y) -> (x, y)
    field_ = []
    for raw in range(0, gl.dimension):
        field_.append([])
        for col in range(0, gl.dimension):
            field_[raw].append(gl.field[gl.dimension-1-raw][col])
    gl.field = field_


def mirror_groups(groups): # Отразить позицию по оси y: (x, y) -> (n-1-x, y)
    groups_ = []
    for group in groups:
        dots = []
        dames = []
        for dot in group[0]:
            dots.append((gl.dimension-1-dot[0], dot[1]))
        for dame in group[1]:
            dames.append((gl.dimension-1-dame[0], dame[1]))
        groups_.append([dots, dames])
    return groups_


def mirror_move(): # Отразить позицию по оси y: (x, y) -> (n-1-x, y)
    if gl.move_list[gl.move_count-1] != 'pass':
        x = gl.move_list[gl.move_count-1][0]
        y = gl.move_list[gl.move_count-1][1]
        gl.move_list[gl.move_count-1] = (gl.dimension - 1 - x, y)


def move(x, y):

    cut_history_tail()  # Удаление всех сохранённых шагов после нового хода

    if gl.field[x][y] == " ":  # Проверка на заполненность поля
        if validation(x, y):  # Проверка на самоубийственный ход
            add_group(x, y)
            gl.field[x][y] = gl.turn_colour
        else:
            return False

        gl.move_list.append((x, y))
        gl.field_list.append(copy(gl.field))

        if post_validation() == False:  # Проверки на повторение хода
            undo()
            return False

        add_black_groups_list()
        add_white_groups_list()
        # count_eyes()  # Сильно нагружает проц при загрузке партии
        gl.black_group_eyes_list.append(copy(gl.black_group_eyes))  # вместо count_eyes
        gl.white_group_eyes_list.append(copy(gl.white_group_eyes))  # вместо count_eyes
        gl.alive_group_list.append(copy(gl.alive_groups))
        count_score()
        gl.black_score_list.append(gl.black_score)
        gl.white_score_list.append(gl.white_score)
        change_colour()
        gl.move_count += 1
        if not gl.auto_move:
            save_game()
        return True
    else:
        return False


def move_dot(dot):
    return move(dot[0], dot[1])  # ERROR 'NoneType' object is not subscriptable


def new_game():
    reset_globals()
    draw.massage(' Новая игра')


def pass_move():

    if not gl.end_game:
        print('pass', gl.turn_colour)
        cut_history_tail()
        set_globals(gl.move_count-1)

        if gl.move_list != [] and gl.move_list[-1] == 'pass':
            count_territory()
            gl.end_game = True

        gl.move_list.append('pass')
        gl.move_count += 1
        gl.field_list.append(copy(gl.field))
        gl.black_group_list.append(copy(gl.black_groups))
        gl.black_group_eyes_list.append((copy(gl.black_group_eyes)))
        gl.black_score_list.append(gl.black_score)
        gl.white_group_list.append(copy(gl.white_groups))
        gl.white_group_eyes_list.append(copy(gl.white_group_eyes))
        gl.white_score_list.append(gl.white_score)
        gl.alive_group_list.append(copy(gl.alive_groups))

        change_colour()


def post_validation():  # Валидация после постановки камня
    if len(gl.move_list) > 7:
        for dot in gl.move_list[-3:-1]:
            if dot == 'pass':
                return True
        if gl.field_list[len(gl.move_list)-3] == gl.field:
            return False  # Запрещается повторение позиций


def recount_groups(): # calc all groups, dames, indexes
    # Для каждого камня
    return 0


def reset_globals():

    gl.alive_groups = []
    gl.alive_group_list = []
    gl.turn_colour = 'B'
    gl.white_groups = []
    gl.white_group_list = []
    gl.white_group_eyes = []
    gl.white_group_eyes_list = []
    gl.white_index = []  # Копия доски со ссылками на группы
    for n in range(0, gl.dimension):
        gl.white_index.append([([])] * gl.dimension)
    gl.black_groups = []
    gl.black_group_list = []
    gl.black_group_eyes = []
    gl.black_group_eyes_list = []
    gl.black_index = []
    for n in range(0, gl.dimension):
        gl.black_index.append([([])] * gl.dimension)
    gl.komi = 6.5
    gl.winner = []
    gl.white_score = gl.komi
    gl.white_score_list = []
    gl.black_score = 0
    gl.black_score_list = []
    gl.total_score = gl.black_score - gl.white_score

    gl.field = []
    for n in range(0, gl.dimension):
        gl.field.append([(' ')] * gl.dimension)
    gl.move_list = []
    gl.move_count = 0
    gl.field_list = []
    gl.influence = []
    for n in range(0, gl.dimension):
        gl.influence.append([])
        for m in range(0, gl.dimension):
            gl.influence[n].append([0, 0, 0, 0])
    gl.end_game = False
    gl.temp_background = gl.background
    gl.ally_groups = gl.black_groups
    gl.enemy_groups = gl.white_groups
    gl.ally_index = gl.black_index
    gl.enemy_index = gl.white_index


def restore_dame(dot):
    #up
    if dot[1] != 0:
        gr = gl.ally_index[dot[0]][dot[1]-1]
        if gr != []:
            if gr[1] != []:
                if gr[1][-1] != dot:
                    gr[1].append(dot)
            else:
                gr[1].append(dot)
    #down
    if dot[1] != gl.dimension-1:
        gr = gl.ally_index[dot[0]][dot[1]+1]
        if gr != []:
            if gr[1] != []:
                if gr[1][-1] != dot:
                    gr[1].append(dot)
            else:
                gr[1].append(dot)
    #left
    if dot[0] != 0:
        gr = gl.ally_index[dot[0]-1][dot[1]]
        if gr != []:
            if gr[1] != []:
                if gr[1][-1] != dot:
                    gr[1].append(dot)
            else:
                gr[1].append(dot)
    #right
    if dot[0] != gl.dimension-1:
        gr = gl.ally_index[dot[0]+1][dot[1]]
        if gr != []:
            if gr[1] != []:
                if gr[1][-1] != dot:
                    gr[1].append(dot)
            else:
                gr[1].append(dot)


def rotate():  # Повернуть позицию на 90° по часовой
    if len(gl.move_list) > 0:
        rotate_field()
        gl.black_groups = rotate_groups(gl.black_groups)
        gl.black_group_list[gl.move_count - 1] = copy(gl.black_groups)
        gl.white_groups = rotate_groups(gl.white_groups)
        gl.white_group_list[gl.move_count - 1] = copy(gl.white_groups)
        gl.field_list[gl.move_count-1] = copy(gl.field)
        rotate_move()
        change_colour()  # Обновление переменных индексов
        change_colour()  # Возвращаем назад очередь хода


def rotate_field(): # Повернуть позицию на 90° по часовой: (y, n-1-x) -> (x, y)
    field_ = []
    for raw in range(0, gl.dimension):
        field_.append([])
        for col in range(0, gl.dimension):
            field_[raw].append(gl.field[col][gl.dimension-1-raw])
    gl.field = field_


def rotate_groups(groups): # Повернуть позицию на 90° по часовой: (x, y) -> (n-1-y, x)
    groups_ = []
    for group in groups:
        dots = []
        dames = []
        for dot in group[0]:
            dots.append((gl.dimension-1-dot[1], dot[0]))
        for dame in group[1]:
            dames.append((gl.dimension-1-dame[1], dame[0]))
        groups_.append([dots, dames])
    return groups_


def rotate_move(): # Повернуть позицию на 90° по часовой: (x, y) -> (n-1-y, x)
    if gl.move_list[gl.move_count-1] != 'pass':
        x = gl.move_list[gl.move_count-1][0]
        y = gl.move_list[gl.move_count-1][1]
        gl.move_list[gl.move_count-1] = (gl.dimension - 1 - y, x) # TypeError: unsupported operand type(s) for -: 'int' and 'str'


def save_game():
    with open('save.sgf', 'w', encoding='UTF-8') as f:
        f.write('(;PB[player1]\nPW[player2]\nKM['+str(gl.komi)+']\nDT['+time.strftime('%Y-%m-%d')+']\nRU['+gl.rules+']\n')
        color = 'B'
        for move in gl.move_list:
            x = move[0]
            y = move[1]
            if move != 'pass':
                move_str = ';'+ color +'['+ gl.N_TO_SGF[x] + gl.N_TO_SGF[y] +']'
                f.write(move_str)
            color = 'B' if color == 'W' else 'W'
        f.write(')')

def save_inputs_for_win_ai(field):

    x = []
    for raw in range(0, gl.dimension):
        for line in range(0, gl.dimension):
            if field[raw][line] == ' ':
                x.append(0.)
            elif field[raw][line] == 'B':
                x.append(0.5)
            else:  # 2
                x.append(1.)
    if gl.turn_colour == 'B':
        x.append(1.)
        x.append(0.)
    else:
        x.append(0.)
        x.append(1.)
    x.append(float(gl.black_score))
    x.append(float(gl.white_score))
    return np.expand_dims(x, axis=0)


def save_moves_best_move():  # a1, a2 ... a361 [0, 1, 2] field ; x, y [0 ... 18] coords

    data = open('go_data_all_men.txt', 'a')
    i = 0
    for field_ in gl.field_list:
        for line in field_:
            for col in line:
                if col == ' ':
                    data.write('0')
                elif col == 'B':
                    data.write('1')
                else:
                    data.write('2')
        data.write(';')
        data.write(str(gl.move_list[i][0]))
        data.write(',')
        data.write(str(gl.move_list[i][1]))
        data.write('\n')
        i += 1
    data.close()


def save_moves_win(data):  # input: a1, a2 ... a361 [0, 1, 2] field; black_move; white_move; black_score; white_score;
    # output: s [float] score; b, w [float] winner

    f = open(data, 'a')
    for line in range(0, gl.dimension):  # field
        for col in range(0, gl.dimension):
            if gl.field[line][col] == ' ':
                f.write('0')
            elif gl.field[line][col] == 'B':
                f.write('1')
            else:
                f.write('2')
    f.write(';1') if gl.turn_colour == 'B' else f.write(';0')
    f.write('1;') if gl.turn_colour == 'W' else f.write('0;')
    f.write(str(gl.black_score) + ';')
    f.write(str(abs(gl.white_score)) + ';')
    f.write(str(abs(gl.winner[1])) + ';')  # total score
    if gl.winner[0] == 'B':
        f.write('1')
        f.write('0')
    else:
        f.write('0')
        f.write('1')
    f.write('\n')
    f.close()


def save_moves_dame(data):  # input: a1, a2 ... a361 [0, 1, 2] field; black_move; white_move; black_score; white_score;
    # output: s [float] score; b, w [float] winner

    f = open(data, 'a')
    for line in range(0, gl.dimension):  # field
        for col in range(0, gl.dimension):
            if gl.field[line][col] == ' ':
                f.write('0')
            elif gl.field[line][col] == 'B':
                f.write('1')
            else:
                f.write('2')
    # !!! Дописать !!!

    f.close()


def set_globals(move_number):

    # set field
    for x in range(0, gl.dimension):
        for y in range(0, gl.dimension):
            gl.field[x][y] = copy(gl.field_list[move_number][x][y])
            # list index out of range при загрузке L дважды
            # При нажатии вниз после l и n

    # set groups
    gl.black_groups = copy(gl.black_group_list[move_number])  # list index out of range
    for group in gl.black_groups:
        for dot in group[0]:
            gl.black_index[dot[0]][dot[1]] = group

    gl.black_group_eyes = copy(gl.black_group_eyes_list[move_number])

    gl.white_groups = copy(gl.white_group_list[move_number])
    for group in gl.white_groups:
        for dot in group[0]:
            gl.white_index[dot[0]][dot[1]] = group

    gl.white_group_eyes = copy(gl.white_group_eyes_list[move_number])

    gl.alive_groups = copy(gl.alive_group_list[move_number])

    # set color and color dependencies
    if move_number % 2 != 0:
        gl.turn_colour = 'B'
        gl.ally_groups = gl.black_groups
        gl.ally_index = gl.black_index
        gl.enemy_groups = gl.white_groups
        gl.enemy_index = gl.white_index
    else:
        gl.turn_colour = 'W'
        gl.ally_groups = gl.white_groups
        gl.ally_index = gl.white_index
        gl.enemy_groups = gl.black_groups
        gl.enemy_index = gl.black_index

    # set scores
    gl.black_score = gl.black_score_list[move_number]
    gl.white_score = gl.white_score_list[move_number]
    count_score()


def to_start(): # Переход к началу партии
    if len(gl.move_list) > 0:
        gl.move_count = 1
        set_globals(gl.move_count-1)
        gl.end_game = False


def to_end(): # Переход к концу партии
    gl.move_count = len(gl.move_list)
    if gl.move_count != 0:
        set_globals(gl.move_count-1)


def undo(): # Отменить невалидный ход
    del gl.field_list[-1]
    del gl.move_list[-1]
    set_globals(gl.move_count - 1)


def update_influence(groups, increment):

    gl.ally_colour = 'B' if increment == 1 else 'W'
    for group in groups:
        for dot in set().union(group[0], group[1]):  # Влияние распространяется от точек и от их дыханий
            if len(group[1]) >= 3:
                x = dot[0]
                y = dot[1]
                while True:  # ⬋
                    x -= 1
                    y += 1
                    if x >= 0 and y < gl.dimension:
                        if gl.field[x + 1][y] != ' ' and gl.field[x][y - 1] != ' ':
                            break  # Блокируется распространение сквозь другие точки
                        if x - 1 >= 0:
                            if gl.field[x - 1][y] != ' ':
                                break
                        if y + 1 < gl.dimension:
                            if gl.field[x][y + 1] != ' ':
                                break  # Не проходит рядом с другими точками
                        if gl.field[x][y] == ' ':
                            gl.influence[x][y][0] += increment
                        else:
                            break
                    else:
                        break
                x = dot[0]
                y = dot[1]
                while True:  # ⬉
                    x -= 1
                    y -= 1
                    if x >= 0 and y >= 0:
                        if gl.field[x + 1][y] != ' ' and gl.field[x][y + 1] != ' ':
                            break
                        if x - 1 >= 0:
                            if gl.field[x - 1][y] != ' ':
                                break
                        if y - 1 >= 0:
                            if gl.field[x][y - 1] != ' ':
                                break  # Не проходит рядом с другими точками
                        if gl.field[x][y] == ' ':
                            gl.influence[x][y][1] += increment
                        else:
                            break
                    else:
                        break
                x = dot[0]
                y = dot[1]
                while True:  # ⬈
                    x += 1
                    y -= 1
                    if x < gl.dimension and y >= 0:
                        if gl.field[x - 1][y] != ' ' and gl.field[x][y + 1] != ' ':
                            break
                        if x + 1 < gl.dimension:
                            if gl.field[x + 1][y] != ' ':
                                break
                        if y - 1 >= 0:
                            if gl.field[x][y - 1] != ' ':
                                break  # Не проходит рядом с другими точками
                        if gl.field[x][y] == ' ':
                            gl.influence[x][y][2] += increment
                        else:
                            break
                    else:
                        break
                x = dot[0]
                y = dot[1]
                while True:  # ⬊
                    x += 1
                    y += 1
                    if x < gl.dimension and y < gl.dimension:
                        if gl.field[x - 1][y] != ' ' and gl.field[x][y - 1] != ' ':
                            break
                        if x + 1 < gl.dimension:
                            if gl.field[x + 1][y] != ' ':
                                break
                        if y + 1 < gl.dimension:
                            if gl.field[x][y + 1] != ' ':
                                break   # Не проходит рядом с другими точками
                        if gl.field[x][y] == ' ':
                            gl.influence[x][y][3] += increment
                        else:
                            break
                    else:
                        break


def validation(x, y):  # Первоначальная валидация (перед постановкой камня)

    ally_dame = 0  # Количество лишних дыханий(свыше 1-го) у соседних с ходом союзных групп

    if y != 0:  # Сверху не стенка
        if gl.field[x][y-1] == ' ':
            return True  # Можно ходить, если у хода есть хотя бы одно дыхание
        elif gl.enemy_index[x][y-1] != []:
            if len(gl.enemy_index[x][y-1][1]) == 1:
                return True # Можно ходить если у противника одно дыхание
        elif gl.ally_index[x][y-1] != []:
            ally_dame += len(gl.ally_index[x][y-1][1])-1  # Учитываем количество лишних дыханий союзной группы

    if y != gl.dimension-1: # Снизу не стенка
        if gl.field[x][y+1] == ' ':
            return True  # Можно ходить, если у хода есть хотя бы одно дыхание
        elif gl.enemy_index[x][y+1] != []:
            if len(gl.enemy_index[x][y+1][1]) == 1:
                return True # Можно ходить если у противника одно дыхание
        elif gl.ally_index[x][y+1] != []:
            ally_dame += len(gl.ally_index[x][y+1][1])-1 # Учитываем количество лишних дыханий союзной группы

    if x != 0: # Справа не стенка
        if gl.field[x-1][y] == ' ':
            return True # Можно ходить, если у хода есть хотя бы одно дыхание
        elif gl.enemy_index[x-1][y] != []:
            if len(gl.enemy_index[x-1][y][1])==1: # IndexError FIXED
                return True # Можно ходить если у противника одно дыхание
        elif gl.ally_index[x-1][y] != []:
            ally_dame += len(gl.ally_index[x-1][y][1])-1 # Учитываем количество лишних дыханий союзной группы

    if x != gl.dimension-1: # Слева не стенка
        if gl.field[x+1][y] == ' ':
            return True # Можно ходить, если у хода есть хотя бы одно дыхание
        elif gl.enemy_index[x+1][y] != []:
            if len(gl.enemy_index[x+1][y][1])==1:
                return True # Можно ходить если у противника одно дыхание
        elif gl.ally_index[x+1][y] != []:
            ally_dame += len(gl.ally_index[x+1][y][1])-1 # Учитываем количество лишних дыханий союзной группы

    if ally_dame == 0:
        return False # Нет дыханий у хода и у всех союзных групп по одному дыханию
    else:
        return True

