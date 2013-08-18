#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame


class BallSprite(pygame.sprite.Sprite):

    image_origin = pygame.image.load('ball.png')

    def __init__(self, position=(0,0), size=(25,25)):
        pygame.sprite.Sprite.__init__(self)
        self.image_origin = self.image_origin.convert_alpha()
        self.image_origin = pygame.transform.scale(self.image_origin, size)
        self.image = self.image_origin
        self.size = size
        self.rect = self.image.get_rect()
        self.position = position

    def resize(self, size):
        if self.size != size:
            self.size = size
            self.image_origin = pygame.transform.scale(self.image_origin, size)
            self.image = self.image_origin
            self.rect = self.image.get_rect()

    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.image_origin, angle)
        self.rect = self.image.get_rect()

    def set_pos(self, position):
        self.position = position

    def update(self):
        self.rect.center = self.position
