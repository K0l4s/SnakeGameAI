import pygame 
class Snake:
    def __init__(self, x, y):
        self.body = [(x, y)]
        self.direction = (1, 0)

    def change_direction(self, new_direction):
        if self.direction[0] + new_direction[0] != 0 or self.direction[1] + new_direction[1] != 0:
            self.direction = new_direction

    def move(self):
        head = self.body[-1]
        # print(head)
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        self.body.append(new_head)
        return new_head

    def collides_with_wall(self, width, height):
        head = self.body[-1]
        x, y = head[0], head[1]
        return x < 0 or x >= width or y < 0 or y >= height

    def collides_with_self(self):
        head = self.body[-1]
        return head in self.body[:-1]
    