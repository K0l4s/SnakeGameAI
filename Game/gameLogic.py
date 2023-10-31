import random

class GameLogic:
    def __init__(self, snake, width, height):
        self.snake = snake
        self.width = width
        self.height = height
        self.spawn_food()

    def spawn_food(self):
        while True:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if (x, y) not in self.snake.body:
                self.food = (x, y)
                break

    def update(self):
        head = self.snake.move()

        if head == self.food:
            self.spawn_food()
        else:
            self.snake.body.pop(0)

        if self.snake.collides_with_wall(self.width, self.height) or self.snake.collides_with_self():
            print("Game over!")
            self.snake.__init__(self.width // 2, self.height // 2)
