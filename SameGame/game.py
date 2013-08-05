#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import deque
import random
import sys
from pprint import pprint
import time

import pygame
from pygame.locals import *


pygame.init()


BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
SILVER = (170, 170, 170)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
COLORS = (BLACK, BLUE, GREEN, RED, WHITE, YELLOW)

SQUARE_HEIGHT = 30
SQUARE_MARGIN = 2
SQUARE_WIDTH = 30

class SquareModel:

    def __init__(self, row, col, num_colors=5):
        self.num_colors = num_colors
        self.col = col
        self.row = row
        self._data = [[0 for j in range(col)] for i in range(row)]
        self.num_squares = 0

    def _rearrange(self):
        for j in range(self.col):
            I = [i for i in range(self.row)
                 if self._data[i][j]]
            p = self.row
            for i in reversed(I):
                p -= 1
                self._data[p][j] = self._data[i][j]
            while p:
                p -= 1
                self._data[p][j] = 0

    def adjacent_same_sqaures(self, row, col):
        return [(i,j) for i,j in self.adjacent_squares(row, col)
                if self._data[i][j] == self._data[row][col]]

    def adjacent_squares(self, row, col):
        L = [(row-1,col), (row, col-1), (row+1, col), (row, col+1)]
        return [(i,j) for i,j in L
                if 0 <= i < self.row
                if 0 <= j < self.col]

    def square_color(self, row, col):
        return self._data[row][col]

    def height(self):
        return self.row

    def populate(self):
        for i in range(self.row):
            for j in range(self.col):
                self._data[i][j] = random.randint(1, self.num_colors)
        self.num_squares = self.row * self.col

    def remove_same_sqaures(self, row, col):
        if not self._data[row][col]:
            return 0
        elif not len(self.adjacent_same_sqaures(row, col)):
            return 0
        D = deque([(row,col)])
        counter = 0
        while len(D):
            i,j = D.pop()
            counter += 1
            for x in self.adjacent_same_sqaures(i,j):
                if x not in D:
                    D.append(x)
            self._data[i][j] = 0
        self._rearrange()
        self.num_squares -= counter
        return counter

    def width(self):
        return self.col


def main():
    m = SquareModel(12, 8)
    m.populate()
    scores = 0
    game_rect = pygame.Rect(0, 0, m.width() * (SQUARE_WIDTH+SQUARE_MARGIN),
                            m.height() * (SQUARE_HEIGHT+SQUARE_MARGIN))
    btn_new_rect = pygame.Rect(game_rect.right+20, game_rect.bottom-40, 100, 30)
    screen = pygame.display.set_mode((game_rect.width+150, game_rect.height))
    pygame.display.set_caption('Same Squares')
    clock = pygame.time.Clock()
    font1 = pygame.font.Font(None, 32)
    font2 = pygame.font.Font(None, 24)

    while True:
        clock.tick(20)
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                if game_rect.collidepoint(x, y):
                    row = y / (SQUARE_WIDTH+SQUARE_MARGIN)
                    col = x / (SQUARE_HEIGHT+SQUARE_MARGIN)
                    scores += m.remove_same_sqaures(row, col)
                elif btn_new_rect.collidepoint(x, y):
                    m.populate()
                    scores = 0
        screen.fill(BLACK)
        for i in range(m.height()):
            for j in range(m.width()):
                c = COLORS[m.square_color(i,j)]
                pygame.draw.rect(
                                 screen, c,
                                 (j * (SQUARE_WIDTH+SQUARE_MARGIN),
                                  i * (SQUARE_HEIGHT+SQUARE_MARGIN),
                                  SQUARE_WIDTH+SQUARE_MARGIN,
                                  SQUARE_HEIGHT+SQUARE_MARGIN),
                                 0
                                )
        pygame.draw.line(screen, SILVER, (game_rect.right+2,0), (game_rect.right+2,game_rect.bottom), 3)
        text = 'scores: {}'.format(scores)
        font_surface = font1.render(text, True, WHITE)
        screen.blit(font_surface, (game_rect.right + 8, 0))
        text = 'squares: {}'.format(m.num_squares)
        font_surface = font1.render(text, True, WHITE)
        screen.blit(font_surface, (game_rect.right + 8, 30))
        pygame.draw.rect(screen, SILVER, btn_new_rect, 5)
        text = 'New Game'
        font_surface = font2.render(text, True, GREEN)
        screen.blit(font_surface, (btn_new_rect.left + 10, btn_new_rect.top + 6))
        pygame.display.update()


if __name__ == '__main__':
    main()
