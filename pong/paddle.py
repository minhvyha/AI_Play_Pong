import pygame


class Paddle:
    VEL = 4
    WIDTH = 20
    HEIGHT = 100

    def __init__(self, x, y, color):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.color = color

    def draw(self, win):
        pygame.draw.rect(
            win, self.color, (self.x, self.y, self.WIDTH, self.HEIGHT))
        pygame.draw.rect(win, (255,255,255), (self.x, self.y, self.WIDTH, 2.5))
        pygame.draw.rect(win, (255,255,255), (self.x, self.y, 2.5, self.HEIGHT))
        pygame.draw.rect(win, (255,255,255), (self.x, self.y + self.HEIGHT, self.WIDTH, 2.5))
        pygame.draw.rect(win, (255,255,255), (self.x + self.WIDTH, self.y, 2.5, self.HEIGHT + 2.5))

    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
