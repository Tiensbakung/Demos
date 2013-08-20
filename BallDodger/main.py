#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import random

import pygame
from pygame.locals import *
import Box2D as b2

from sprite import BallSprite

pygame.init()

screen_size = (400, 400)
ballsprite_size = (20, 20)
ballbody_radius = 0.5
origin = (0, 0)
ratio = 20


def b2g(pos):
    return b2g_x(pos[0]), b2g_y(pos[1])

def b2g_x(x):
    return x * ratio

def b2g_y(y):
    return -y * ratio

def g2b(pos):
    return g2b_x(pos[0]), g2b_y(pos[1])

def g2b_x(x):
    return x / ratio

def g2b_y(y):
    return -y / ratio


def create_ball(w, pos, radius, density):
    ball = w.CreateDynamicBody(position=pos)
    ball.CreateCircleFixture(radius=radius, density=density, restitution=1.0)
    return ball

def create_wall(w, pos, size):
    wall = w.CreateStaticBody(position=pos)
    wall.CreatePolygonFixture(box=(size[0]/2,size[1]/2), density=0, restitution=0.9)
    return wall


def main():
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('Ball Dodger')
    clock = pygame.time.Clock()

    w = b2.b2World()
    floor = create_wall(w, g2b((screen_size[0]/2, screen_size[1])),
                        (screen_size[0]/ratio, 0.2))
    lwall = create_wall(w, g2b((0, screen_size[1]/2)),
                        (0.2, screen_size[1]/ratio))
    rwall = create_wall(w, g2b((screen_size[0], screen_size[1]/2)),
                        (0.2, screen_size[1]/ratio))

    robots = []
    for i in range(8):
        pos = (ballsprite_size[0], random.uniform(0, screen_size[0]/3))
        body = create_ball(w, g2b(pos), ballbody_radius, 1.0)
        body.ApplyLinearImpulse((random.uniform(3,15), random.uniform(0,3)),
                                body.worldCenter, True)
        sprite = BallSprite(pos, ballsprite_size)
        robots.append((body, sprite))
    allsprites = pygame.sprite.RenderPlain([x[1] for x in robots])

    running = True
    fps = 60
    dt = 1.0 / fps
    vel_iters = 10
    pos_iters = 10
    while running:
        for e in pygame.event.get():
            if e.type == QUIT:
                running = False
            elif e.type == KEYDOWN and e.key == K_ESCAPE:
                running = False

        w.Step(dt, vel_iters, pos_iters)
        for body, sprite in robots:
            pos = b2g(body.position)
            angle = math.degrees(body.angle) % 360
            sprite.set_pos(pos)
            sprite.rotate(angle)
        screen.fill(0x0)
        allsprites.update()
        allsprites.draw(screen)
        pygame.display.flip()
        clock.tick(fps)


if __name__ == '__main__':
    main()
