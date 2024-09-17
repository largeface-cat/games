import pygame as pg
import time
import os
import numpy as np
import matplotlib.pyplot as plt
import threading


Lock = threading.Lock()  # 在threading模块中获得锁类
direction = 'r'
num_foods = 50
last_direction = direction
alive = True
score = 0
pg.init()
pg.display.set_caption('title')
screen = pg.display.set_mode((1920, 1080))

class Snake:
    def __init__(self, screen, x=0, y=0, width=20, height=20, color=(0, 0, 0)):
        self.screen = screen
        self.width = width
        self.height = height
        self.color = color
        self.body = [(x, y)]
        self.last_place = (x, y)

    def draw(self):
        for i in range(len(self.body)):
            x, y = self.body[i]
            pg.draw.rect(self.screen, self.color, (x, y, self.width, self.height))
            pg.draw.rect(self.screen, (255, 255, 255), (x + 4, y + 4, self.width - 8, self.height - 8))
            # if i == 0:
            pg.draw.rect(self.screen, (np.random.randint(0,255), np.random.randint(0,255), np.random.randint(0,255)), (x + 5, y + 5, self.width - 10, self.height - 10))

    def move(self, direction: str):
        x, y = self.body[0]
        if direction == 'l':
            x -= self.width
        elif direction == 'r':
            x += self.width
        elif direction == 'u':
            y -= self.height
        elif direction == 'd':
            y += self.height
        self.body.insert(0, (x, y))
        self.last_place = self.body.pop()

    def eat(self):
        self.body.append(self.last_place)

    def check_collision(self):
        x, y = self.body[0]
        if x < 0 or x >= self.screen.get_width() or y < 0 or y >= self.screen.get_height():
            return True
        if self.body[0] in self.body[1:]:
            return True
        return False


class Food:
    def __init__(self, screen, snake, x=0, y=0, width=20, height=20, color=(255, 0, 0)):
        self.screen = screen
        self.width = width
        self.height = height
        self.color = color
        self.x = x
        self.y = y
        self.reset(snake)

    def draw(self):
        self.color = (np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255))
        pg.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height))

    def reset(self, snake):
        self.x, self.y = None, None
        while (self.x, self.y) in snake.body or (self.x, self.y) == snake.last_place or self.x is None:
            self.x = np.random.randint(0, self.screen.get_width() // self.width) * self.width
            self.y = np.random.randint(0, self.screen.get_height() // self.height) * self.height


class DrawThread(threading.Thread):
    def __init__(self, screen):
        super(DrawThread, self).__init__()
        self.screen = screen

    def run(self):
        global direction, alive, score, last_direction, num_foods
        snake = Snake(self.screen)
        foods = []
        for i in range(num_foods):
            foods.append(Food(self.screen, snake))
        while True:
            Lock.acquire()
            if direction:
                snake.move(direction)
                last_direction = direction
            # if snake.body[0] == (food.x, food.y):
            #     score += 1
            #     snake.eat()
            #     food.reset(snake)
            for food in foods:
                if snake.body[0] == (food.x, food.y):
                    score += 1
                    snake.eat()
                    food.reset(snake)
            if snake.check_collision() or not alive:
                alive = False
                Lock.release()
                return -1
            self.screen.fill((255, 255, 255))
            snake.draw()
            # food.draw()
            for food in foods:
                food.draw()
            pg.display.flip()
            Lock.release()
            time.sleep(0.1)


def end(alive_threads: [threading.Thread]): # type: ignore
    if Lock.locked():
        Lock.release()
    global alive, score
    Lock.acquire()
    alive = False
    Lock.release()
    for thread in alive_threads:
        thread.join()
    print('Your score is:', score)
    pg.quit()
    exit()


draw_thread = DrawThread(screen)
draw_thread.start()
while True:
    Lock.acquire()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            end([draw_thread])
            break
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                end([draw_thread])
                break
            if event.key == pg.K_LEFT and last_direction != 'r':
                direction = 'l'
            if event.key == pg.K_RIGHT and last_direction != 'l':
                direction = 'r'
            if event.key == pg.K_UP and last_direction != 'd':
                direction = 'u'
            if event.key == pg.K_DOWN and last_direction != 'u':
                direction = 'd'
    if Lock.locked():
        Lock.release()
    if not alive:
        end([draw_thread])
        break
exit()
