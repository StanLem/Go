import pygame as pg
from pygame import gfxdraw
import globals as gl
import func as fn
import random as rnd


def ai_move(max_ten):
    radius = int(gl.net_wide*0.2)
    pg.draw.circle(surface=gl.screen, color=gl.GREEN, radius=radius,
                   center=(gl.border + max_ten[0][0][0] * gl.net_wide, gl.border + max_ten[0][0][1] * gl.net_wide))
    for dot in max_ten[0][1:]:
        pg.draw.circle(surface=gl.screen, color=gl.BLUE, radius=radius,
                       center=(gl.border + dot[0] * gl.net_wide, gl.border + dot[1] * gl.net_wide))

def ai_best_ten(score_move):
    for elem in score_move:
        score = gl.dame_font.render(str(elem[0]), True, gl.GREEN)
        dot = elem[1]
        if elem[0] < 10:
            gl.screen.blit(score, (gl.border - int(gl.net_wide / 8) + dot[0] * gl.net_wide,
                                    gl.border - int(3 * gl.net_wide / 8) + dot[1] * gl.net_wide))
        else:
            gl.screen.blit(score, (gl.border - int(gl.net_wide/4) + dot[0] * gl.net_wide,
                                            gl.border - int(3*gl.net_wide/8) + dot[1] * gl.net_wide))


def all():
    gl.screen.blit(gl.background, (0, 0))
    field()
    info()
    positions()
    dame(gl.black_groups)
    dame(gl.white_groups)
    eyes()
    influence()
    current_move()
    pg.image.save(gl.screen, 'temp.jpeg')
    gl.temp_background = pg.image.load('temp.jpeg') # Чтобы курсор отображался
    pg.display.update()
    win_prediction()


def current_move():
    radius = int(gl.net_wide*0.48)
    if gl.move_list != [] and gl.move_list[gl.move_count-1] != 'pass': # list index out of range
        line = gl.move_list[gl.move_count-1][0] # Подсвечиваем шаг сделанный на ходу под номером move_count
        column = gl.move_list[gl.move_count-1][1]
        gfxdraw.aacircle(gl.screen, gl.border + line * gl.net_wide, gl.border + column * gl.net_wide,
                         radius, (250, 250, 250))
        gfxdraw.aacircle(gl.screen, gl.border + line * gl.net_wide, gl.border + column * gl.net_wide,
                         radius+1, (250, 250, 250))
        gfxdraw.aacircle(gl.screen, gl.border + line * gl.net_wide, gl.border + column * gl.net_wide,
                         radius+2, (250, 250, 250))
        gfxdraw.aacircle(gl.screen, gl.border + line * gl.net_wide, gl.border + column * gl.net_wide,
                         radius+3, (250, 250, 250))
        gfxdraw.aacircle(gl.screen, gl.border + line * gl.net_wide, gl.border + column * gl.net_wide,
                         radius-1, (250, 250, 250))
        gfxdraw.aacircle(gl.screen, gl.border + line * gl.net_wide, gl.border + column * gl.net_wide,
                         radius-2, (250, 250, 250))


def cursor():
    radius = int(gl.net_wide*0.47)
    if gl.turn_colour == 'B':
        #pg.draw.circle(surface=gl.screen, color=gl.BLACK, radius=radius, center=(gl.x, gl.y))
        gfxdraw.filled_circle(gl.screen, gl.x, gl.y, radius, gl.BLACK)
    else:
        #pg.draw.circle(surface=gl.screen, color=gl.WHITE, radius=radius, center=(gl.x, gl.y))
        gfxdraw.filled_circle(gl.screen, gl.x, gl.y, radius, gl.WHITE)


def dame(color_group):
    for group in color_group:  # Отображение групп и дыханий
        if group not in gl.alive_groups:
            if color_group == gl.black_groups:
                color = (rnd.randint(140, 220), rnd.randint(140, 220), rnd.randint(140, 220))
            else:
                color = (rnd.randint(0, 135), rnd.randint(0, 135), rnd.randint(0, 135))
            for dot in group[0]:
                n = len(group[1])
                if n == 1:
                    # gfxdraw.aacircle(surface, x, y, radius, color)
                    gfxdraw.aacircle(gl.screen, gl.border + dot[0] * gl.net_wide, gl.border + dot[1] * gl.net_wide,
                                     int(gl.net_wide*0.3), gl.RED)
                    gfxdraw.aacircle(gl.screen, gl.border + dot[0] * gl.net_wide, gl.border + dot[1] * gl.net_wide,
                                     int(gl.net_wide*0.3)+1, gl.RED)
                    gfxdraw.aacircle(gl.screen, gl.border + dot[0] * gl.net_wide, gl.border + dot[1] * gl.net_wide,
                                     int(gl.net_wide*0.3)+2, gl.RED)
                    #pg.draw.circle(surface=gl.screen, color=gl.RED, radius=int(gl.net_wide*0.3), width=2,
                                   #center=(gl.border + dot[0] * gl.net_wide, gl.border + dot[1] * gl.net_wide))
                gfxdraw.aacircle(gl.screen, gl.border + dot[0] * gl.net_wide, gl.border + dot[1] * gl.net_wide,
                                 int(gl.net_wide*0.47), color)
                gfxdraw.aacircle(gl.screen, gl.border + dot[0] * gl.net_wide, gl.border + dot[1] * gl.net_wide,
                                 int(gl.net_wide*0.47)+1, color)
                gfxdraw.aacircle(gl.screen, gl.border + dot[0] * gl.net_wide, gl.border + dot[1] * gl.net_wide,
                                 int(gl.net_wide*0.47)+2, color)
                gfxdraw.aacircle(gl.screen, gl.border + dot[0] * gl.net_wide, gl.border + dot[1] * gl.net_wide,
                                 int(gl.net_wide*0.47), color)
                gfxdraw.aacircle(gl.screen, gl.border + dot[0] * gl.net_wide, gl.border + dot[1] * gl.net_wide,
                                 int(gl.net_wide*0.47)-1, color)
                #pg.draw.circle(surface=gl.screen, color=color, radius=int(gl.net_wide*0.47), width=3,
                               #center=(gl.border + dot[0] * gl.net_wide, gl.border + dot[1] * gl.net_wide))
                dame_n = gl.dame_font.render(str(n), True, color)
                if n < 10:
                    gl.screen.blit(dame_n, (gl.border - int(gl.net_wide/8) + dot[0] * gl.net_wide,
                                            gl.border - int(3*gl.net_wide/8) + dot[1] * gl.net_wide))
                else:
                    gl.screen.blit(dame_n, (gl.border - int(gl.net_wide/4) + dot[0] * gl.net_wide,
                                            gl.border - int(3*gl.net_wide/8) + dot[1] * gl.net_wide))


def eyes():  # Рисуем глаза
    for group in (gl.black_group_eyes + gl.white_group_eyes):
        for eye in group[2]:
            # aaellipse(surface, x, y, rx, ry, color)
            gfxdraw.aaellipse(gl.screen, gl.border + eye[0] * gl.net_wide, gl.border + eye[1] * gl.net_wide,
                              int(gl.net_wide*0.3), int(gl.net_wide*0.1), gl.LIGHT)
            gfxdraw.aaellipse(gl.screen, gl.border + eye[0] * gl.net_wide, gl.border + eye[1] * gl.net_wide,
                              int(gl.net_wide*0.3)-1, int(gl.net_wide*0.1)-1, gl.LIGHT)
            gfxdraw.aaellipse(gl.screen, gl.border + eye[0] * gl.net_wide, gl.border + eye[1] * gl.net_wide,
                              int(gl.net_wide*0.3)-2, int(gl.net_wide*0.1)-2, gl.LIGHT)

            gfxdraw.aacircle(gl.screen, gl.border + eye[0] * gl.net_wide, gl.border + eye[1] * gl.net_wide,
                             int(gl.net_wide * 0.1)-1, gl.LIGHT)
            gfxdraw.aacircle(gl.screen, gl.border + eye[0] * gl.net_wide, gl.border + eye[1] * gl.net_wide,
                             int(gl.net_wide * 0.1)-2, gl.LIGHT)
            gfxdraw.aacircle(gl.screen, gl.border + eye[0] * gl.net_wide, gl.border + eye[1] * gl.net_wide,
                             int(gl.net_wide * 0.1)-3, gl.LIGHT)

            gfxdraw.filled_circle(gl.screen, gl.border + eye[0] * gl.net_wide, gl.border + eye[1] * gl.net_wide,
                                  int(gl.net_wide * 0.1)-5, gl.BLACK)


def field():
    vert = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
    hor = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
           'U', 'V', 'W', 'X', 'Y', 'Z', 'I']
    for raw in range(gl.dimension):
        pg.draw.line(gl.screen, gl.BLACK, [gl.border + raw * gl.net_wide, gl.border], # Вертикальные линии
                     [gl.border + raw * gl.net_wide, gl.border + (gl.dimension-1) * gl.net_wide], 2)
        pg.draw.line(gl.screen, gl.BLACK, [gl.border, gl.border + raw * gl.net_wide], # Горизонтальные линии
                     [gl.border + (gl.dimension-1) * gl.net_wide, gl.border + raw * gl.net_wide], 2)

        v = gl.text_font.render(str(vert[raw]), True, gl.BLACK) # Буквы
        gl.screen.blit(v, (int(gl.net_wide/2), gl.border - int(gl.net_wide/4) + raw * gl.net_wide)) if raw < 9 \
            else gl.screen.blit(v, (int(gl.net_wide/3), gl.border - int(gl.net_wide/4) + raw * gl.net_wide))

        h = gl.text_font.render(hor[raw], True, gl.BLACK) # Цифры
        gl.screen.blit(h, (gl.border - int(gl.net_wide/4) + raw * gl.net_wide, int(gl.border/2) - int(gl.net_wide/4)))


def help():

    gl.screen.fill(gl.WHITE)
    font = gl.text_font
    text = ['A - Подсказка от компьютера ai_move',
            'E - Авто доигрывание',
            'H - Вызов страницы подсказки',
            'L - Загрузка партии',
            'M - Собрать данные для обучения из папки',
            'N - Новая игра',
            'R - Повернуть поле по часовой стрелке',
            'T - Отзеркалить поле по вертикали',
            'LEFT - Отменить ход, перейти на ход назад',
            'RIGHT - Перейти на ход вперёд в партии',
            'UP - Перейти к началу партии',
            'DOWN - Перейти в конец партии',
            'SPACE - Пропуск хода, пас']

    for n in range(0, len(text)):
        line = font.render(text[n], True, gl.BLACK)
        gl.screen.blit(line, (gl.border, gl.border + n * gl.net_wide))


def influence():

    font = gl.influence_font
    for x in range(0, gl.dimension):
        for y in range(0, gl.dimension):
            vector = gl.influence[x][y] #(⬋, ⬉, ⬈, ⬊)
            if vector[0] != 0:
                if vector[0] > 0:
                    color = gl.BLACK
                else:
                    color = gl.WHITE
                influence_vector = font.render('⬋', True, color)
                gl.screen.blit(influence_vector, (gl.border - int(5*gl.net_wide/16) + x * gl.net_wide,
                                                  gl.border - int(gl.net_wide/4) + y * gl.net_wide))
            if vector[1] != 0:
                if vector[1] > 0:
                    color = gl.BLACK
                else:
                    color = gl.WHITE
                influence_vector = font.render("⬉", True, color)
                gl.screen.blit(influence_vector, (gl.border - int(5*gl.net_wide/16) + x * gl.net_wide,
                                                  gl.border - int(gl.net_wide/2) + y * gl.net_wide))
            if vector[2] != 0:
                if vector[2] > 0:
                    color = gl.BLACK
                else:
                    color = gl.WHITE
                influence_vector = font.render("⬈", True, color)
                gl.screen.blit(influence_vector, (gl.border - int(gl.net_wide/16) + x * gl.net_wide,
                                                  gl.border - int(gl.net_wide/2) + y * gl.net_wide))
            if vector[3] != 0:
                if vector[3] > 0:
                    color = gl.BLACK
                else:
                    color = gl.WHITE
                influence_vector = font.render('⬊', True, color)
                gl.screen.blit(influence_vector, (gl.border - int(gl.net_wide/16) + x * gl.net_wide,
                                                  gl.border - int(gl.net_wide/4) + y * gl.net_wide))


def info():
    info = str(gl.move_count)
    x = gl.border
    y = gl.border + gl.net_wide*(gl.dimension-1) + gl.net_wide/2

    if gl.end_game:
        if gl.total_score > 0:
            info += ' Чёрные выиграли со счётом: ' + str(gl.total_score)
        else:
            info += ' Белые выиграли со счётом: ' + str(abs(gl.total_score))
    else:
        if gl.move_list != [] and gl.move_list[gl.move_count-1] == 'pass': # list index out of range
            if gl.turn_colour == 'B':
                info += ' Белые Пасуют'
            else:
                info += ' Чёрные Пасуют'
        info += ' Ч:' + str(gl.black_score) + '+' + str(gl.black_territory)
        info += '   Б:' + str(gl.white_score) + '+' + str(gl.white_territory)

    info = gl.text_font.render(info, True, gl.BLACK)
    gl.screen.blit(info, (x, y))


def massage(massage):
    warning = gl.text_font.render(massage, True, gl.RED)
    gl.screen.blit(warning, (0, 0))


def positions():
    radius = int(gl.net_wide*0.47)
    for line in range(len(gl.field)):  # Отрисовка позиций
        for column in range(len(gl.field[line])):
            if gl.field[line][column] == 'B':
                #pg.draw.circle(surface=gl.screen, color=gl.BLACK, radius=radius,
                               #center=(gl.border + line * gl.net_wide, gl.border + column * gl.net_wide))
                #pg.gfxdraw.aacircle(surface=gl.screen, color=gl.BLACK, radius=radius,
                               #center=(gl.border + line * gl.net_wide, gl.border + column * gl.net_wide))
                gfxdraw.filled_circle(gl.screen, gl.border + line * gl.net_wide, gl.border + column * gl.net_wide,
                                      radius, gl.BLACK)
            elif gl.field[line][column] == 'W':
                #pg.draw.circle(surface=gl.screen, color=gl.WHITE, radius=radius,
                               #center=(gl.border + line * gl.net_wide, gl.border + column * gl.net_wide))
                gfxdraw.filled_circle(gl.screen, gl.border + line * gl.net_wide, gl.border + column * gl.net_wide,
                                      radius, gl.WHITE)


def win_prediction():
    1 == 1
    '''if gl.dimension == 19:
        x = fn.save_inputs_for_win_ai(gl.field)
        y = gl.win_model.predict(x)
        print(y)
        win = y[0]
        if win[0] > win[1]:
            print('Чёрные ведут на', round(win[2]*50), 'очков')
        else:
            print('Белые ведут на', round(win[2]*50), 'очков')'''
