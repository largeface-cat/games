import pygame as pg
import time
import threading
import os
import numpy as np
import matplotlib.pyplot as plt

pg.init()  # 初始化
pg.display.set_caption('title')
screen = pg.display.set_mode((800, 800), pg.RESIZABLE)  # 建立一个400x400的窗口
rect = pg.Rect(0, 0, 800, 100)
rect.center = (0, 0)

def parse_event(event):
    if event.type == pg.QUIT:
        pg.quit()
        exit()
    if event.type == pg.KEYDOWN:
        if event.key == pg.K_ESCAPE:
            pg.quit()
            exit()
        if event.key in range(pg.K_0, pg.K_9):
            print(event.key - pg.K_0)

while True:
    screen.fill((255, 255, 255))  # 填充白色
    # rand_array = np.random.rand(1000)
    # plt.hist(rand_array, bins=100)
    # plt.savefig('hist.png')
    # plt.close()
    # hist = pg.image.load('hist.png')
    # os.remove('hist.png')
    # screen.blit(hist, rect)
    # rect = rect.move(0, 1)

    for event in pg.event.get():  # 获取用户事件
        parse_event(event)
    pg.display.flip()  # 更新窗口
