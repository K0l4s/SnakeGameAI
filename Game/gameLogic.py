import random
import pygame
from Game.food import Food
import Game.colors as color
import Game.config as cf
clock = pygame.time.Clock()
class GameLogic:
    def __init__(self, snake, width, height):
        self.snake = snake
        self.width = width
        self.height = height
        self.food = Food(width, height, snake)
        self.game_over_flag = False
        self.score = 0
        self.path = []
        self.using_algorithm = False
    def update(self):
        if not self.snake.is_moving:
            return
        head = self.snake.move()

        # self.visualize_bfs(cf.screen, cf.window)
        if head == self.food.food:
            self.snake.play_crunch_sound()
            self.food.spawn_food()
            self.score +=1
            print(self.score)
        else:
            self.snake.body.pop(0)

        if self.snake.collides_with_wall(self.width, self.height) or self.snake.collides_with_self():
            self.game_over_flag = True

    def get_score(self):
        return self.score
            
    def game_over(self):
        return self.game_over_flag
    
    def restart_game(self):
        self.snake.__init__(self.width // 2, self.height // 2)
        self.food.spawn_food()
        self.game_over_flag = False
        self.score = 0

    def bfs(self, start, target, screen, window):
        visited = set()
        queue = [(start, [])]
        
        while queue:
            current, path = queue.pop(0)
            if current:
                node_rect = pygame.Rect( 7 + current[0] * 20, 7 + current[1] * 20, 5, 5)
                pygame.draw.rect(screen, color.GREEN , node_rect)
        
            if current == target:
                window.blit(screen, (0,0))  
                pygame.display.update(node_rect)
                return path

            for neighbor in self.get_valid_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return None
    def get_valid_neighbors(self, position):
        x, y = position
        valid_neighbors = []

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_x, new_y = x + dx, y + dy
            if (0 <= new_x < self.width) and (0 <= new_y < self.height) and (new_x, new_y) not in self.snake.body:
                valid_neighbors.append((new_x, new_y))

        return valid_neighbors
    
    def visualize_bfs(self, screen, window):
        if not self.game_over():
            start = self.snake.body[-1]
            target = self.food.food
            path = self.bfs(start, target, screen, window)
            if path:
                self.path = [(path[0][0] - start[0], path[0][1] - start[1])]
                self.path.extend((path[i][0] - path[i-1][0], path[i][1] - path[i-1][1]) for i in range(1, len(path)))
                
    
    def is_direction_safe(self, direction):
        head = self.snake.body[-1]
        new_head = (head[0] + direction[0], head[1] + direction[1])
        return (
            0 <= new_head[0] < self.width and 0 <= new_head[1] < self.height and new_head not in self.snake.body[:-1]
        )

    def change_direction_safely(self):
        possible_directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        safe_directions = [direction for direction in possible_directions if self.is_direction_safe(direction)]
        print(f"safe: {safe_directions}")
        if safe_directions:
            new_direction = random.choice(safe_directions)
            print(f"choose: {new_direction}")
            self.snake.change_direction(new_direction)
            self.snake.set_moving(True)
            self.update()
        else:
            pass

    def open_path(self):
        for _ in range(50):
            self.change_direction_safely()
            self.snake.set_moving(True)
            self.visualize_bfs(cf.screen, cf.window)
            self.update()
            if self.path:
                self.using_algorithm = True
                self.move_along_path()
                self.update()
                break
    
    def move_along_path(self):
        if self.path:
            direction = self.path.pop(0)
            # print(direction)
            self.snake.change_direction(direction)
            self.snake.set_moving(True)
            self.update()
        else:
            print("No path")
            self.using_algorithm = False
            self.open_path()
        

        
        