import pygame
import Game.colors as color
class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 20
        self.image = pygame.image.load("Resources/block.jpg")
        self.image = pygame.transform.scale(self.image, (self.size, self.size))

    def draw(self, screen):
        screen.blit(self.image, (self.x * 20, self.y * 20))