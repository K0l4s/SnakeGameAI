import pygame
import random
class Food:
    def __init__(self, width, height, snake):
        self.width = width
        self.height = height
        self.snake = snake
        self.spawn_food()
        
    def spawn_food(self):
        while True:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if (x, y) not in self.snake.body:
                self.food = (x, y)
                break