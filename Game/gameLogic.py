import random
from Game.food import Food
from Game.bfs import bfs
class GameLogic:
    def __init__(self, snake, width, height):
        self.snake = snake
        self.width = width
        self.height = height
        self.food = Food(width, height, snake)

    def update(self):
        head = self.snake.move()

        if head == self.food.food:
            self.food.spawn_food()
        else:
            self.snake.body.pop(0)

        if self.snake.collides_with_wall(self.width, self.height) or self.snake.collides_with_self():
            print("Game over!")
            self.snake.__init__(self.width // 2, self.height // 2)
