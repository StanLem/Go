import tkinter as tk
import tkinter.filedialog as fd


def save_chineese(filename):
    if filename != '':
        print('Open party', filename)
        file = open(filename, 'r', encoding='UTF-8')
        save_file = open('save_ch.txt', 'a', encoding='UTF-8')
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

        try:
            win_c = file[1].split('RE[')[1]
            win_c = win_c.split(']')[0]
            if 'B' not in win_c and 'W' not in win_c:
                save_file.write(filename + win_c + '\n')
        except IndexError:
            return False
        except ValueError:
            return False


def save_rules(file, game_):
    if file != '':
        print('Open party', file)
        file = open(file, 'r', encoding='UTF-8')
        save_file = open('save_rule_other.txt', 'a', encoding='UTF-8')
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
        file = file.split(';')

        try:
            rule = file[1].split('RU[')[1]
            rule = rule.split(']')[0]
            if 'apanese' in rule:
                rule = 'Japanese'
            elif 'hinese' in rule:
                rule = 'Chinese'
            elif 'orea' in rule:
                rule = 'Korean'
            else:
                save_file.write(game_ + '/' + rule + '\n')
        except IndexError:
            return False
        except ValueError:
            return False


def save_size(file, game_):
    if file != '':
        print('Open party', file)
        file = open(file, 'r', encoding='UTF-8')
        save_file = open('save_size.txt', 'a', encoding='UTF-8')
        try:
            file = file.read()
        except UnicodeDecodeError:
            print('UnicodeDecodeError')
            return False
        file = file.replace('\n', '')
        file = file.split(';')

        try:
            if '[t' in file or 't]' in file:
                size = 20
            else:
                size = file[1].split('SZ[')[1]
                size = size.split(']')[0]
            save_file.write(game_ + '/' + size + '\n')
        except IndexError:
            return False
        except ValueError:
            return False


def save_level(file, game_):
    if file != '':
        print('Open party', file)
        file = open(file, 'r', encoding='UTF-8')
        save_file = open('save_level.txt', 'a', encoding='UTF-8')
        try:
            file = file.read()
        except UnicodeDecodeError:
            print('UnicodeDecodeError')
            return False
        file = file.replace('\n', '')
        file = file.split(';')

        try:
            l1 = file[1].split('BR[')[1]
            l1 = l1.split(']')[0]
            l2 = file[1].split('WR[')[1]
            l2 = l2.split(']')[0]
            save_file.write(game_ + '/' + l1 + ' '+ l2+ '\n')
        except IndexError:
            return False
        except ValueError:
            return False


def save_move_count(file, game_):
    if file != '':
        print('Open party', file)
        file = open(file, 'r', encoding='UTF-8')
        save_file = open('save_move_count.txt', 'a', encoding='UTF-8')
        try:
            file = file.read()
        except UnicodeDecodeError:
            print('UnicodeDecodeError')
            return False
        file = file.replace('\n', '')
        file = file.split(';')

        try:
            l = len(file) - 1
            save_file.write(game_ + '/' + str(l) + '\n')
        except IndexError:
            return False
        except ValueError:
            return False


def save_strange_format(file, game_):
    if file != '':
        print('Open party', file)
        file = open(file, 'r', encoding='UTF-8')
        save_file = open('save_strange_format.txt', 'a', encoding='UTF-8')
        try:
            file = file.read()
        except UnicodeDecodeError:
            print('UnicodeDecodeError')
            return False

        file = file.split('))')

        if len(file) > 1:
            save_file.write(game_ + '/N )) = ' + str(len(file)) + '\n')
            return True
        else:
            return False


def save_all(filename):
    if filename != '':
        print('Open party', filename)
        game = filename.split('/')[-1]
        file = open(filename, 'r', encoding='UTF-8')
        save_file = open('save_all.txt', 'a', encoding='UTF-8')
        dimension = 19
        black_level = 0
        white_level = 0
        komi = 0
        wins = 0
        color = ''
        try:
            file = file.read()
        except UnicodeDecodeError:
            print('UnicodeDecodeError')
            return False
        if len(file) == 0:
            print('file is empty')
            return False
        # Размер поля 19
        if '[t' in file:
            print('>19 field')
            return False
        if 't]' in file:
            print('>19 field')
            return False
        title = file.split(';')[1]
        file = file.replace('(;'+title+';', '')  # Убираем заголовок
        file = file.split(')')  # Отделяем основную партию от ответвлений
        file = file[0].split(';')  # Разделение на ходы
        number_of_moves = len(file)

        try:
            wins = title.split('RE[')[1]
            wins = wins.split(']')[0]
            color = wins.split('+')[0]
            wins = int(wins.split('+')[1])
            if wins == 0:
                return False
        except IndexError:
            print('WIN is empty')
            return False
        except ValueError:
            print('WIN is invalid')
            return False

        try:
            size = title.split('SZ[')[1]
            size = size.split(']')[0]
            size = int(size)
            if size != dimension:
                if dimension != 20:  # Размер изменён на 20 при наличии строки t
                    dimension = size
        except IndexError:
            print('SZ is empty')

        try:
            black_level = title.split('BR[')[1]
            black_level = int(black_level.split(']')[0].replace('p','').replace('*',''))
            white_level = title.split('WR[')[1]
            white_level = int(white_level.split(']')[0].replace('p','').replace('*',''))
        except IndexError:
            print('LVL is empty')
        except ValueError:
            print('LVL is incorrect')

        try:
            komi = title.split('KM[')[1]
            komi = komi.split(']')[0]
            komi = float(komi)  # Если не указано коми, устанавливаем значение по умолчанию
        except IndexError:
            print('komi default')
            return False
        except ValueError:
            print('komi default')
            return False
        white_score = komi

        if dimension == 19\
            and komi != 0 \
            and wins != 0 \
            and number_of_moves > 200:
            '''and black_level > 3\
            and white_level > 3\''''
            save_file.write('moves=' + str(number_of_moves) + ' B=' + str(black_level) + ' W='
                            + str(white_level) + ' wins=' + color + ' points=' + str(wins) + ' komi='
                            + str(komi) + ' ' + game + '\n')


def chose_dir():
    root = tk.Tk()
    folder = fd.askdirectory(title="Выбрать папку",
                             initialdir="C:/Users/Станислав/PycharmProjects/Fractal/My_Projects/Go")
    root.destroy()
    return folder


mypath = chose_dir()

if mypath:
    from os import listdir
    from os.path import isfile, join

    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    # enable = True
    for game in onlyfiles:  # text
        save_all(mypath + '/' + game)
    print('data mined')
else:
    print('data mine canceled')



