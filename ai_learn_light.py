import copy
import os
import time
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
# from tensorflow.keras.datasets import mnist         # библиотека базы выборок Mnist
from tensorflow import keras
from tensorflow.keras.layers import Concatenate, Dense, Flatten, Dropout, Conv2D, MaxPooling2D

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))


# tf.debugging.set_log_device_placement(True)
def train_best_move():
    with open('go_data.txt', 'r') as f:
        f = f.readlines()
        print('file reading completed')
        # print(f)
        n_test = round(len(f)/10)
        i = 0
        for line in f:
            line = line.split(';') # line[0] = field, line[1] = move
            field = line[0]
            move = line[1].replace('\n', '').split(',')
            if i < n_test:
                x_test.append([])
                for raw in range(0, 19):
                    x_test[i].append([])
                    for col in range(0, 19):
                        if field[raw*19 + col] == '0':
                            x_test[i][raw].append([1, 0, 0])
                        elif field[raw*19 + col] == '1':
                            x_test[i][raw].append([0, 1, 0])
                        else: # 2
                            x_test[i][raw].append([0, 0, 1])
                move_ = int(move[0])*19 + int(move[1])
                y_test.append([])
                for num in range(0, 361):
                    if num == move_:
                        y_test[i].append(1)
                    else:
                        y_test[i].append(0)
            else:
                x_train.append([])
                for raw in range(0, 19):
                    x_train[i-n_test].append([])
                    for col in range(0, 19):
                        if field[raw * 19 + col] == '0':
                            x_train[i-n_test][raw].append([1, 0, 0])
                        elif field[raw * 19 + col] == '1':
                            x_train[i-n_test][raw].append([0, 1, 0])
                        else:  # 2
                            x_train[i-n_test][raw].append([0, 0, 1])
                y_train.append([])
                for num in range(0, 361):
                    if num == move_:
                        y_train[i-n_test].append(1)
                    else:
                        y_train[i-n_test].append(0)
            i += 1
    return (x_train, y_train), (x_test, y_test)


def train_win(data):
    x_train = []
    y_train = []
    x_test = []
    y_test = []
    print('Train from', data)
    with open(data, 'r') as f:
        f = f.readlines()
        # print(f)
        n_test = round(len(f)/5) # Доля для тестовой выборки
        i = 0
        for line in f:
            line = line.split(';') # line[0] = field, line[1] = move
            field = line[0]
            black_turn = float(line[1][0])
            white_turn = float(line[1][1])
            black_score = float(line[2])/50
            white_score = float(line[3])/50
            score = float(line[4])/50
            black_win = float(line[5][0])
            white_win = float(line[5][1])
            if i < n_test:
                x_test.append([])
                fill_x_win(x_test[i], field, black_turn, white_turn, black_score, white_score)

                y_test.append([score, black_win, white_win])
                #y_test.append([black_win, white_win])
            else:
                x_train.append([])
                fill_x_win(x_train[i-n_test], field, black_turn, white_turn, black_score, white_score)

                y_train.append([score, black_win, white_win])
                #y_train.append([black_win, white_win])
            i += 1
    return (x_train, y_train), (x_test, y_test)


def fill_x_win(x, field, black_turn, white_turn, black_score, white_score):
    for num in range(0, 361):
            if field[num] == '0':
                x.append(0.)
            elif field[num] == '1':
                x.append(0.5)
            else:  # 2
                x.append(1.)
    x.append(black_turn)
    x.append(white_turn)
    x.append(black_score)
    x.append(white_score)


# Build model
'''layer_field = keras.Sequential([
    Dense(361, activation='relu', input_shape=(19, 19, 3)),
    Flatten()
])
layer_score = keras.Sequential([
    Dense(2, activation='relu', input_shape=(2,)),
    Flatten()
])
layer_input = Concatenate([layer_field, layer_score])'''

model = keras.Sequential([
    #Conv2D(6, (3, 3), padding='same', activation='relu', input_shape=(363,)),
    #Flatten(),
    Dense(2, activation='softmax', input_shape=(365,)),
    Dense(3, activation='softmax'),
    # MaxPooling2D((2, 2), strides=2),
    # Flatten(),
])
best_model_name = 'AI/AI_WIN-2-3-b1-e6_p50_'
parts = 50

(x_train, y_train), (x_test, y_test) = train_win('DATA/go_wins_chi.txt')

black_wins = 0
white_wins = 0
for line in y_train:
    if line[1] == 1.0:
        black_wins += 1
    else:
        white_wins += 1
print('black:', black_wins)
print('white:', white_wins)


x_test2 = x_test[int(len(x_test)/2):]
y_test2 = y_test[int(len(y_test)/2):]
x_test = x_test[:int(len(x_test)/5)]
y_test = y_test[:int(len(y_test)/5)]

print(model.summary())      # вывод структуры НС в консоль
model.compile(optimizer='adam',
             loss='categorical_crossentropy',
             metrics=['accuracy'])
print('model compiled', time.ctime())


# tf.function(jit_compile=True)

# model = keras.models.load_model('AI/AI_WIN_TURN_part_5')

print('start training', time.ctime())
best_accuracy = 0
# best_model = copy.deepcopy(model)
best_model = keras.models.clone_model(model)
best_model.build((None, 365)) # input layer
best_model.compile(optimizer='rmsprop', loss='categorical_crossentropy')
best_model.set_weights(model.get_weights())
best_model_name_post = ''

for part in range(0, parts-1):
    print('part', part)
    x_size = int(len(x_train) / parts)
    x_train_cur = x_train[part * x_size:(part + 1) * x_size]
    y_size = int(len(y_train) / parts)
    y_train_cur = y_train[part * y_size:(part + 1) * y_size]

    # his = model.fit(x_train_cur, y_train_cur, batch_size=1, epochs=6, validation_data=(x_test, y_test))
    his = model.fit(x_train_cur, y_train_cur, batch_size=1, epochs=6)

    eva = model.evaluate(x_test, y_test)

    # model.evaluate(x_train_cur, y_train_cur)

    if eva[1] > best_accuracy:
        best_accuracy = eva[1]
        best_model = keras.models.clone_model(model)
        best_model.build((None, 365)) # input layer
        best_model.compile(optimizer='rmsprop', loss='categorical_crossentropy')
        best_model.set_weights(model.get_weights())
        best_model_name_post = str(part) + '_a' + str(int(best_accuracy*100))

    # model.evaluate(x_train[parts-1:parts], y_train[parts-1:parts]) # accuracy: 1.0000

best_model.save(best_model_name + best_model_name_post)

print('Обучение завершено', time.ctime(), 'Лучшая точность', best_accuracy)


