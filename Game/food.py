import pygame
import random
class Food:
    def __init__(self, width, height, snake):
        self.width = width
        self.height = height
        self.snake = snake
        self.image = pygame.image.load("Resources/skin/apple.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.is_eaten = False
    def spawn_food(self, obstacles):
        self.is_eaten = False
        while True:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if (x, y) not in self.snake.body and (x, y) not in [(obstacle.x, obstacle.y) for obstacle in obstacles]:
                self.food = (x, y)
                break