import random
import pygame
from Game.food import Food
import Game.colors as color
import Game.config as cf
clock = pygame.time.Clock()
from queue import PriorityQueue
import math
class GameLogic:
    def __init__(self, snake, width, height):
        self.snake = snake
        self.width = width
        self.height = height
        self.food = Food(width, height, snake)
        self.game_over_flag = False
        self.score = 0
        self.path = []
        self.is_finding = False
        self.is_on_music = True
    def update(self):
        if not self.snake.is_moving:
            return
        head = self.snake.move()

        # self.visualize_bfs(cf.screen, cf.window)
        if head == self.food.food:
            if self.is_on_music:
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
        self.is_finding = False
        while queue:
            self.is_finding = False
            current, path = queue.pop(0)

            if current:
                node_rect = pygame.Rect( 7 + current[0] * 20, 7 + current[1] * 20, 5, 5)
                pygame.draw.rect(screen, color.GREEN , node_rect)

            if current == target:
                window.blit(screen, (30,30))  
                pygame.display.update(node_rect)
                self.is_finding = True
                return path

            for neighbor in self.get_valid_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return None
    
    def ucs(self, start, target, screen, window):
        visited = set()
        queue = PriorityQueue()
        queue.put((0, start, []))  # (cost, current, path)
        
        while not queue.empty():
            self.is_finding = False
            cost, current, path = queue.get()
            
            if current:
                node_rect = pygame.Rect(7 + current[0] * 20, 7 + current[1] * 20, 5, 5)
                pygame.draw.rect(screen, color.GREEN, node_rect)

            if current == target:
                window.blit(screen, (30, 30))
                pygame.display.update(node_rect)
                self.is_finding = True
                return path

            if current not in visited:
                visited.add(current)
                for neighbor in self.get_valid_neighbors(current):
                    new_cost = cost + 1  # Assuming all steps have equal cost
                    queue.put((new_cost, neighbor, path + [neighbor]))

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
                print("path: 1")
                self.path = [(path[0][0] - start[0], path[0][1] - start[1])]
                self.path.extend((path[i][0] - path[i-1][0], path[i][1] - path[i-1][1]) for i in range(1, len(path)))
            elif not self.is_finding:
                print("path: 22")
                alternative_direction = self.get_alternative_direction(start)
                
                path = self.bfs(start, target, screen, window)
            
                if path:
                    print("change path: 2")
                    self.path = [(path[0][0] - start[0], path[0][1] - start[1])]
                    self.path.extend((path[i][0] - path[i-1][0], path[i][1] - path[i-1][1]) for i in range(1, len(path)))
                elif alternative_direction:
                    print("change path: 2222222222222")
                    self.path = [alternative_direction]    
                    path = self.bfs(start, target, screen, window)
                    
                    if path:
                        self.path = [(path[0][0] - start[0], path[0][1] - start[1])]
                        self.path.extend((path[i][0] - path[i-1][0], path[i][1] - path[i-1][1]) for i in range(1, len(path)))
                    
                elif not path:
                    print("path: 333")
                    path = self.bfs(start, target, screen, window)
                    if not path:
                        path = self.bfs(start, self.food.food, screen, window)
                        print("change")
                    if path:
                        self.path = [(self.path[0][0] - start[0], self.path[0][1] - start[1])]
                        self.path.extend((self.path[i][0] - self.path[i-1][0], self.path[i][1] - self.path[i-1][1]) for i in range(1, len(self.path)))
                else:
                # Thay vì kết thúc trò chơi, hãy di chuyển theo đầu rắn
                    head_direction = (self.snake.body[-1][0] - self.snake.body[-2][0], self.snake.body[-1][1] - self.snake.body[-2][1])
                    self.path = [head_direction]      

    def visualize_ucs(self, screen, window):
        if not self.game_over():
            start = self.snake.body[-1]
            target = self.food.food
            path = self.ucs(start, target, screen, window)
            if path:
                print("path: 1")
                self.path = [(path[0][0] - start[0], path[0][1] - start[1])]
                self.path.extend((path[i][0] - path[i-1][0], path[i][1] - path[i-1][1]) for i in range(1, len(path)))
            elif not self.is_finding:
                print("path: 22")
                alternative_direction = self.get_alternative_direction(start)
                
                path = self.ucs(start, target, screen, window)
            
                if path:
                    print("change path: 2")
                    self.path = [(path[0][0] - start[0], path[0][1] - start[1])]
                    self.path.extend((path[i][0] - path[i-1][0], path[i][1] - path[i-1][1]) for i in range(1, len(path)))
                elif alternative_direction:
                    print("change path: 2222222222222")
                    self.path = [alternative_direction]    
                    path = self.ucs(start, target, screen, window)
                    
                    if path:
                        self.path = [(path[0][0] - start[0], path[0][1] - start[1])]
                        self.path.extend((path[i][0] - path[i-1][0], path[i][1] - path[i-1][1]) for i in range(1, len(path)))
                
                    elif not path:
                        print("path: 333")
                        path = self.ucs(start, target, screen, window)
                        if not path:
                            path = self.ucs(start, self.food.food, screen, window)
                            print("change")
                        if path:
                            self.path = [(self.path[0][0] - start[0], self.path[0][1] - start[1])]
                            self.path.extend((self.path[i][0] - self.path[i-1][0], self.path[i][1] - self.path[i-1][1]) for i in range(1, len(self.path)))
                else:
                    # Thay vì kết thúc trò chơi, hãy di chuyển theo đầu rắn
                        head_direction = (self.snake.body[-1][0] - self.snake.body[-2][0], self.snake.body[-1][1] - self.snake.body[-2][1])
                        self.path = [head_direction]        

    def get_alternative_direction(self, start):
        max_space = 0
        best_direction = None

        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            new_x, new_y = start[0] + dx, start[1] + dy

            if (0 < new_x < self.width-1) and (0 < new_y < self.height-1) and (new_x, new_y) not in self.snake.body:
                space_count = 0
                for ddx, ddy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                    nx, ny = new_x + ddx, new_y + ddy
                    if (0 <= nx < self.width) and (0 <= ny < self.height) and (nx, ny) not in self.snake.body:
                        space_count += 1

                # Update if the current direction provides more space
                if space_count > max_space:
                    max_space = space_count
                    best_direction = (dx, dy)
        print(max_space)
        return best_direction
    
        # for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        #     new_x, new_y = start[0] + dx, start[1] + dy
        #     if (0 < new_x < self.width) and (0 < new_y < self.height) and (new_x, new_y) not in self.snake.body:
        #         return (dx, dy)
        # return None

    def move_along_path(self):
        if self.path:
            direction = self.path.pop(0)
            # print(direction)
            self.snake.change_direction(direction)
            self.snake.set_moving(True)
            self.update()