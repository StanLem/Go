import pygame as pg
import draw
import globals as gl
import func
import ctypes


ctypes.windll.user32.SetProcessDPIAware()  # Для отмены эффекта масштабирования окна


if __name__ == '__main__':
    # Запуск движка
    pg.init()
    pg.font.init()
    gl.dame_font = pg.font.SysFont('Comic Sans MS', int(gl.net_wide/2))
    gl.text_font = pg.font.SysFont('Cascadia Code', int(gl.screen_scale/20))
    gl.influence_font = pg.font.Font("c:/windows/fonts/seguisym.ttf", int(gl.net_wide/2))
    gl.background = pg.image.load('wood.jpg')
    gl.screen = pg.display.set_mode((gl.screen_scale, gl.screen_scale))
    gl.temp_background = gl.background

    func.reset_globals()
    gl.screen.blit(gl.background, (0, 0))
    pg.display.update()
    pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
    pg.mouse.set_visible(False)

    running = True

    draw.field()
    pg.image.save(gl.screen, 'temp.jpeg')
    gl.temp_background = pg.image.load('temp.jpeg') # Чтобы курсор отображался

    func.load_party(gl.save_file)
    draw.all()

    pg.display.update()



    while running:
        for event in pg.event.get():

            if event.type == pg.QUIT:
                running = False

            elif event.type == pg.MOUSEBUTTONDOWN:
                gl.x = event.pos[0]
                gl.y = event.pos[1]
                line = (gl.x - gl.border) / gl.net_wide
                column = (gl.y - gl.border) / gl.net_wide
                if event.button == 1 and not gl.end_game:
                    if abs(line - round(line)) < 0.3:  # Разброс при постановке камня
                        if abs(column - round(column)) < 0.3:  # Разброс при постановке камня
                            if gl.x > gl.border - gl.net_wide/3: # Пределы поля
                                if gl.x < gl.net_wide * (gl.dimension - 0.7) + gl.border:  # Пределы поля
                                    if gl.y > gl.border - gl.net_wide/3:  # Пределы поля
                                        if gl.y < gl.net_wide * (gl.dimension - 0.7) + gl.border:  # Пределы поля
                                            line = round(line)
                                            column = round(column)
                                            if not func.move(line, column):
                                                draw.massage(' Недопустимый ход!')
                                            else:
                                                draw.all()
                                                draw.cursor()  # Переместить в draw_all
                                                pg.display.update()
                elif event.button == 3:
                    if line < gl.dimension and column < gl.dimension:
                        print(gl.influence[round(line)][round(column)])
                    else:
                        print(gl.x, gl.y)

            elif event.type == pg.MOUSEMOTION:
                gl.x = event.pos[0]
                gl.y = event.pos[1]

                gl.screen.blit(gl.temp_background, (0, 0))

                draw.cursor()
                pg.display.update()

            elif event.type == pg.KEYDOWN:

                if event.key == pg.K_a:
                    func.ai_move()

                if event.key == pg.K_e:
                    func.end_game()
                    draw.all()

                if event.key == pg.K_h:
                    draw.help()

                elif event.key == pg.K_l:
                    func.load_party(func.choose_file())
                    draw.all()

                elif event.key == pg.K_m:
                    func.mine_data(func.chose_dir())

                elif event.key == pg.K_n:
                    func.new_game()
                    draw.all()

                elif event.key == pg.K_r:
                    func.rotate()
                    draw.all()

                elif event.key == pg.K_s:
                    #save_moves()
                    print('data saved')

                elif event.key == pg.K_t:
                    func.mirror()
                    draw.all()


                elif event.key == pg.K_LEFT:
                    func.backward()
                    draw.all()

                elif event.key == pg.K_RIGHT:
                    func.forward()
                    draw.all()

                elif event.key == pg.K_UP:
                    func.to_start()
                    draw.all()

                elif event.key == pg.K_DOWN:
                    func.to_end()
                    draw.all()

                elif event.key == pg.K_SPACE:
                    func.pass_move()  # Пас - смена очереди хода
                    draw.all()
                    draw.cursor()

                pg.display.update()  # Убрать после переноски draw_cursor в draw_all
    pg.quit()




