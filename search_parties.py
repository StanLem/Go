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


def chose_dir():
    root = tk.Tk()
    folder = fd.askdirectory(title="?????????????? ??????????",
                             initialdir="C:/Users/??????????????????/PycharmProjects/Fractal/My_Projects/Go")
    root.destroy()
    return folder


mypath = chose_dir()

if mypath:
    from os import listdir
    from os.path import isfile, join

    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    # enable = True
    for game in onlyfiles:  # text
        save_size(mypath + '/' + game, game)
    print('data mined')
else:
    print('data mine canceled')



