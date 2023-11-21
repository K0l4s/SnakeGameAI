import random
import pygame
from Game.food import Food
from Game.obstacle import Obstacle
import Game.colors as color
import Game.config as cf
clock = pygame.time.Clock()
from queue import PriorityQueue
from Graphics.background import Background
bg = Background(cf.WIDTH, cf.HEIGHT)
import heapq
from random import randrange
from collections import deque

class GameLogic:
    def __init__(self, snake, width, height):
        self.snake = snake
        self.width = width
        self.height = height
        self.food = Food(width, height, snake)
        self.obstacles = [Obstacle(5, 5), Obstacle(10, 10), Obstacle(22, 22), Obstacle(14, 14), Obstacle(3,3)]
        self.game_over_flag = False
        self.score = 0
        self.path = []
        self.path_to_draw = []
        self.is_on_music = True
        self.is_paused = False
        self.visited_nodes = []
        self.current_path = []
    def toggle_pause(self):
        self.is_paused = not self.is_paused
        
    def update(self):
        if not self.snake.is_moving or self.is_paused:
            return
        head = self.snake.move()

        if head == self.food.food:
            self.food.is_eaten = True
            if self.is_on_music:
                self.snake.play_crunch_sound()
            self.food.spawn_food(self.obstacles)
            self.score +=1
            # print(self.score)
        else:
            self.snake.body.pop(0)
        
        if self.snake.collides_with_wall(self.width, self.height) \
            or self.snake.collides_with_self() \
            or self.snake.collides_with_obstacles(self.obstacles):
            self.game_over_flag = True

    def get_score(self):
        return self.score
            
    def game_over(self):
        return self.game_over_flag
    
    def draw_obstacles(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)
            
    def restart_game(self):
        self.snake.__init__(self.width // 2, self.height // 2)
        self.food.spawn_food(self.obstacles)
        self.game_over_flag = False
        self.score = 0
        self.path = []

    def bfs(self, start, target, screen, window):
        visited = set()
        queue = [(start, [])]
        while queue:
            current, path = queue.pop(0)
            if current:
                self.visited_nodes.append(current)
            if current == target:
                self.current_path = path if path else []
                return path

            if target == self.snake.body[0]:
                    for neighbor in self.get_valid_neighbors_new(current):
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append((neighbor, path + [neighbor]))
            else:
                for neighbor in self.get_valid_neighbors(current):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append((neighbor, path + [neighbor]))
        
        return None
    
    def ucs(self, start, target, screen, window):
        visited = set()
        queue = PriorityQueue()
        queue.put((0, start, []))
        
        while not queue.empty():
            cost, current, path = queue.get()
            
            if current:
                self.visited_nodes.append(current)

            if current == target:
                self.current_path = path if path else []
                return path

            if current not in visited:
                visited.add(current)
                if target == self.snake.body[0]:
                    for neighbor in self.get_valid_neighbors_new(current):
                        new_cost = cost + 1
                        queue.put((new_cost, neighbor, path + [neighbor]))
                else:
                    for neighbor in self.get_valid_neighbors(current):
                        new_cost = cost + 1
                        queue.put((new_cost, neighbor, path + [neighbor]))
        return None
    
    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def calculate_cost(self, current, neighbor):
        return 1
    
    def a_star(self, start, target, screen, window):
        visited = set()
        queue = [(0, start, [])]
        
        while queue:
            cost, current, path = heapq.heappop(queue)
            
            if current:
                self.visited_nodes.append(current)

            if current == target:
                self.current_path = path if path else []
                return path

            if current not in visited:
                visited.add(current)
                if target == self.snake.body[0]:
                    for neighbor in self.get_valid_neighbors_new(current):
                        new_cost = cost + self.calculate_cost(current, neighbor)
                        priority = new_cost + self.heuristic(neighbor, target)
                        heapq.heappush(queue, (priority, neighbor, path + [neighbor]))
                else:
                    for neighbor in self.get_valid_neighbors(current):
                        new_cost = cost + self.calculate_cost(current, neighbor)
                        priority = new_cost + self.heuristic(neighbor, target)
                        heapq.heappush(queue, (priority, neighbor, path + [neighbor]))


        return None
    
    def greedy(self, start, target, screen, window):
        visited = set()
        queue = PriorityQueue()
        queue.put((self.heuristic(start, target), start, []))

        while not queue.empty():
            _, current, path = queue.get()

            if current:
                self.visited_nodes.append(current)

            if current == target:
                self.current_path = path if path else []
                return path

            if current not in visited:
                visited.add(current)
                if target == self.snake.body[0]:
                    for neighbor in self.get_valid_neighbors_new(current):
                        new_cost = self.calculate_cost(current, neighbor)
                        queue.put((self.heuristic(neighbor, target), neighbor, path + [neighbor]))
                else:
                    for neighbor in self.get_valid_neighbors(current):
                        new_cost = self.calculate_cost(current, neighbor)
                        queue.put((self.heuristic(neighbor, target), neighbor, path + [neighbor]))

        return None
    def get_valid_neighbors(self, position):
        x, y = position
        valid_neighbors = []

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_x, new_y = x + dx, y + dy
            if (0 <= new_x < self.width) and (0 <= new_y < self.height) \
                and (new_x, new_y) not in self.snake.body \
                and (new_x, new_y) not in [(obstacle.x, obstacle.y) for obstacle in self.obstacles]:
                valid_neighbors.append((new_x, new_y))

        return valid_neighbors
    
    def get_valid_neighbors_new(self, position):
        x, y = position
        valid_neighbors = []

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_x, new_y = x + dx, y + dy
            if (0 <= new_x < self.width) and (0 <= new_y < self.height) \
                and (new_x, new_y) not in self.snake.body[1:-1] \
                and (new_x, new_y) not in [(obstacle.x, obstacle.y) for obstacle in self.obstacles]:
                valid_neighbors.append((new_x, new_y))

        return valid_neighbors

    def simulate_ucs(self, screen, window):
        if not self.game_over():
            start = self.snake.body[-1]
            target = self.food.food
            path = self.ucs(start, target, screen, window)
            if path:
                print("default path")
                self.path = [(path[0][0] - start[0], path[0][1] - start[1])]
                self.path.extend((path[i][0] - path[i-1][0], path[i][1] - path[i-1][1]) for i in range(1, len(path)))
            else:
                tail = self.snake.body[0]

                path = self.ucs(start, tail, screen, window)
                if path:
                    print("following tail")
                    self.path = [(path[0][0] - start[0], path[0][1] - start[1])]
                    self.path.extend((path[i][0] - path[i-1][0], path[i][1] - path[i-1][1]) for i in range(1, len(path)))         
                else:
                        choose_longest_path = self.choose_longest_path(start)
                        if choose_longest_path:
                            print("choose_longest_path")
                            self.path = [choose_longest_path]  
                        else:
                                print("follow default head")
                                head_direction = (self.snake.body[-1][0] - self.snake.body[-2][0], self.snake.body[-1][1] - self.snake.body[-2][1])
                                self.path = [head_direction]
    
    def simulate_astar(self, screen, window):
        if not self.game_over():
            start = self.snake.body[-1]
            target = self.food.food
            path = self.a_star(start, target, screen, window)
            
            if path:
                print("default path")
                self.path = [(path[0][0] - start[0], path[0][1] - start[1])]
                self.path.extend((path[i][0] - path[i-1][0], path[i][1] - path[i-1][1]) for i in range(1, len(path)))
            else:
                tail = self.snake.body[0]

                path = self.ucs(start, tail, screen, window)
                if path:
                    print("following tail")
                    self.path = [(path[0][0] - start[0], path[0][1] - start[1])]
                    self.path.extend((path[i][0] - path[i-1][0], path[i][1] - path[i-1][1]) for i in range(1, len(path)))         
                else:
                        choose_longest_path = self.choose_longest_path(start)
                        if choose_longest_path:
                            print("choose_longest_path")
                            self.path = [choose_longest_path]  
                        else:
                                print("follow default head")
                                head_direction = (self.snake.body[-1][0] - self.snake.body[-2][0], self.snake.body[-1][1] - self.snake.body[-2][1])
                                self.path = [head_direction]
    def simulate_greedy(self, screen, window):
        if not self.game_over():
            start = self.snake.body[-1]
            target = self.food.food
            path = self.greedy(start, target, screen, window)
            if path:
                self.is_finding = True
                print("default path")
                self.path = [(path[0][0] - start[0], path[0][1] - start[1])]
                self.path.extend((path[i][0] - path[i-1][0], path[i][1] - path[i-1][1]) for i in range(1, len(path)))
            else:   
                tail = self.snake.body[0]
                path = self.greedy(start, tail, screen, window)
                if path:
                    print("following tail")
                    self.path = [(path[0][0] - start[0], path[0][1] - start[1])]
                    self.path.extend((path[i][0] - path[i-1][0], path[i][1] - path[i-1][1]) for i in range(1, len(path)))   
                          
                else:
                        choose_longest_path = self.choose_longest_path(start)
                        if choose_longest_path:
                            print("choose_longest_path")
                            self.path = [choose_longest_path]  
                        else:
                                print("follow default head")
                                head_direction = (self.snake.body[-1][0] - self.snake.body[-2][0], self.snake.body[-1][1] - self.snake.body[-2][1])
                                self.path = [head_direction]
    

    def simulate_bfs(self, screen, window):
        if not self.game_over():
            start = self.snake.body[-1]
            target = self.food.food
            path = self.bfs(start, target, screen, window)
            if path:
                self.is_finding = True
                print("default path")
                self.path = [(path[0][0] - start[0], path[0][1] - start[1])]
                self.path.extend((path[i][0] - path[i-1][0], path[i][1] - path[i-1][1]) for i in range(1, len(path)))
            else:   
                tail = self.snake.body[0]
                path = self.bfs(start, tail, screen, window)
                if path:
                    print("following tail")
                    self.path = [(path[0][0] - start[0], path[0][1] - start[1])]
                    self.path.extend((path[i][0] - path[i-1][0], path[i][1] - path[i-1][1]) for i in range(1, len(path)))   
                          
                else:
                        choose_longest_path = self.choose_longest_path(start)
                        if choose_longest_path:
                            print("choose_longest_path")
                            self.path = [choose_longest_path]  
                        else:
                                print("follow default head")
                                head_direction = (self.snake.body[-1][0] - self.snake.body[-2][0], self.snake.body[-1][1] - self.snake.body[-2][1])
                                self.path = [head_direction]
            
    
    def choose_longest_path(self, start):
        def count_available_space(x, y, dx, dy):
            count = 0
            while (0 <= x < self.width) and (0 <= y < self.height) and (x, y) not in self.snake.body:
                count += 1
                x += dx
                y += dy
            return count

        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        best_direction = None
        max_available_space = 0

        for dx, dy in directions:
            new_x, new_y = start[0] + dx, start[1] + dy
            space = count_available_space(new_x, new_y, dx, dy)

            opposite_space = count_available_space(start[0] - dx, start[1] - dy, -dx, -dy)
            total_space = space + opposite_space - 1  # Subtract 1 to avoid double counting start cell

            if total_space > max_available_space:
                max_available_space = total_space
                best_direction = (dx, dy)

            elif total_space == max_available_space and space > max_available_space // 2:
                # If equal available space, prioritize the direction that has more space in its direct line
                max_available_space = total_space
                best_direction = (dx, dy)

        # Di chuyển tiết kiệm không gian
        if best_direction:
            new_x, new_y = start[0] + best_direction[0], start[1] + best_direction[1]
            space_ahead = count_available_space(new_x, new_y, best_direction[0], best_direction[1])
            space_behind = count_available_space(start[0] - best_direction[0], start[1] - best_direction[1], -best_direction[0], -best_direction[1])

            if space_ahead > space_behind:
                return best_direction
            else:
                return (-best_direction[0], -best_direction[1])

        return best_direction

    def move_along_path(self):
        if self.path:
            direction = self.path.pop(0)
            self.snake.change_direction(direction)
            self.snake.set_moving(True)
            self.update()
    
    #draw nodes when simulating
    def draw_nodes(self, screen):
        for node in self.visited_nodes:
            pygame.draw.rect(screen, color.GREEN, (7 + node[0] * 20, 7 + node[1] * 20, 5, 5), 5)

        for step in self.current_path:
            x, y = step
            pygame.draw.rect(screen, color.WHITE, (7 + x * 20, 7 + y * 20, 6, 6))

    #delete nodes for the next simulation
    def reset_nodes(self):
        self.visited_nodes = []
        
