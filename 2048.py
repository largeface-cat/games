import random
state = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
flag = True
while flag:
    empty = []
    for i in range(4):
        for j in range(4):
            if state[i][j] == 0:
                print('□', end=' ')
                empty.append((i, j))
            else:
                print(state[i][j], end=' ')
        print()
    if not empty:
        flag = False
        break
    x, y = random.choice(empty)
    state[x][y] = random.choice([2, 4])
    direction = input()
    if direction == 'w':
        for j in range(4):
            temp = []
            for i in range(4):
                if state[i][j] != 0:
                    temp.append(state[i][j])
            for i in range(len(temp)):
                if i + 1 < len(temp) and temp[i] == temp[i + 1]:
                    temp[i] *= 2
                    temp.pop(i + 1)
            for i in range(4):
                if i < len(temp):
                    state[i][j] = temp[i]
                else:
                    state[i][j] = 0
    elif direction == 's':
        for j in range(4):
            temp = []
            for i in range(3, -1, -1):
                if state[i][j] != 0:
                    temp.append(state[i][j])
            for i in range(len(temp)):
                if i + 1 < len(temp) and temp[i] == temp[i + 1]:
                    temp[i] *= 2
                    temp.pop(i + 1)
            for i in range(3, -1, -1):
                if 3 - i < len(temp):
                    state[i][j] = temp[3 - i]
                else:
                    state[i][j] = 0
    elif direction == 'a':
        for i in range(4):
            temp = []
            for j in range(4):
                if state[i][j] != 0:
                    temp.append(state[i][j])
            for j in range(len(temp)):
                if j + 1 < len(temp) and temp[j] == temp[j + 1]:
                    temp[j] *= 2
                    temp.pop(j + 1)
            for j in range(4):
                if j < len(temp):
                    state[i][j] = temp[j]
                else:
                    state[i][j] = 0
    elif direction == 'd':
        for i in range(4):
            temp = []
            for j in range(3, -1, -1):
                if state[i][j] != 0:
                    temp.append(state[i][j])
            for j in range(len(temp)):
                if j + 1 < len(temp) and temp[j] == temp[j + 1]:
                    temp[j] *= 2
                    temp.pop(j + 1)
            for j in range(3, -1, -1):
                if 3 - j < len(temp):
                    state[i][j] = temp[3 - j]
                else:
                    state[i][j] = 0
    else:
        print('Invalid input!')
        
