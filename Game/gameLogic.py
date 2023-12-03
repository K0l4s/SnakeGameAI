import pygame
from Game.food import Food
import Game.colors as color
import Game.config as cf
clock = pygame.time.Clock()
from queue import PriorityQueue
from Graphics.background import Background
bg = Background(cf.WIDTH, cf.HEIGHT)
from Game.obstacle import Obstacle

class GameLogic:
    def __init__(self, snake, width, height):
        self.snake = snake
        self.width = width
        self.height = height
        self.food = Food(width, height, snake)
        self.obstacles = []
        self.game_over_flag = False
        self.score = 0
        self.path = []
        self.path_to_draw = []
        self.is_on_music = True
        self.is_paused = False
        self.visited_nodes = []
        self.current_path = []
        self.font = pygame.font.Font("Resources/fonts/Coconut Cookies.ttf", 40)

        # self.obstacles = [Obstacle(8,27),Obstacle(7,27),Obstacle(6,27), Obstacle(11, 22),Obstacle(11, 19),Obstacle(11, 21), Obstacle(3, 27), Obstacle(4, 27), Obstacle(5,27), Obstacle(11,20),
        #                   Obstacle(11,23), Obstacle(11,24), Obstacle(11,25), Obstacle(11,26), Obstacle(11,27), Obstacle(11,28), Obstacle(11,29),
        #                   Obstacle(11,18),Obstacle(11,17),Obstacle(11,16),Obstacle(11,15),Obstacle(10,15),Obstacle(9,15),Obstacle(6,15),Obstacle(5,15),Obstacle(4,15),Obstacle(3,15),Obstacle(7,15),Obstacle(8,15)]
    def toggle_pause(self):
        self.is_paused = not self.is_paused
        
    def update(self):
        self.is_finding = True
        if not self.snake.is_moving or self.is_paused:
            return
        head = self.snake.move()

        if head == self.food.food:
            
            self.food.is_eaten = True
            if self.is_on_music:
                self.snake.play_crunch_sound()
            self.food.spawn_food(self.obstacles)
            self.score +=1
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

    def get_obstacle(self, x, y):
        for obstacle in self.obstacles:
            if obstacle.x == x and obstacle.y == y:
                return obstacle
        return None
    def remove_obstacles(self, obstacle):
        self.obstacles.remove(obstacle)
        obstacle_rect = pygame.Rect(30 + obstacle.x * cf.GRID_SIZE, 30 + obstacle.y * cf.GRID_SIZE, cf.GRID_SIZE, cf.GRID_SIZE)
        if (obstacle.x + obstacle.y) % 2 == 0:
            background_rect_image = pygame.image.load("Resources/background_rect_caro_1.png")
            background_rect_image = pygame.transform.scale(background_rect_image, (cf.GRID_SIZE, cf.GRID_SIZE))
        else:
            background_rect_image = pygame.image.load("Resources/background_rect_caro_2.png")
            background_rect_image = pygame.transform.scale(background_rect_image, (cf.GRID_SIZE, cf.GRID_SIZE))
        cf.window.blit(background_rect_image, obstacle_rect)

        pygame.display.update(obstacle_rect)

    def restart_game(self):
        self.snake.__init__(self.width // 2, self.height // 2)
        self.food.spawn_food(self.obstacles)
        self.game_over_flag = False
        self.score = 0
        self.path = []

    def bfs(self, start, target):
        visited = set()
        queue = [(start, [])]
        while queue:
            current, path = queue.pop(0)
            if current:
                self.visited_nodes.append(current)
            if current == target:
                self.current_path = path if path else []
                cf.total_visited = len(visited)
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
    def dfs(self, start, target, max_depth):
        cf.start_time = pygame.time.get_ticks()

        visited = set()
        stack = [(start,[],0)]
        
        while stack:
            current, path, depth = stack.pop()
            
            if depth > max_depth:
                continue 
            
            if current:
                self.visited_nodes.append(current)
                
            if current == target:
                self.current_path = path if path else []
                cf.total_visited = len(visited)
                return path
            
            visited.add(current)
            
            if target == self.snake.body[0]:
                for neighbor in self.get_valid_neighbors_new(current):
                    if neighbor not in visited:
                        stack.append(( neighbor, path + [neighbor], depth + 1))
            else:
                for neighbor in self.get_valid_neighbors(current):
                    if neighbor not in visited:
                        stack.append(( neighbor, path + [neighbor], depth + 1))
                    
        return None
    def ids(self, start, target):
        max_depth = 5
        solution = None
        
        while solution is None and max_depth <= 1050:
            solution = self.dfs(start, target, max_depth)
            max_depth += 1
        # print(max_depth)
        return solution
    
    def ucs(self, start, target):
        visited = set()
        queue = PriorityQueue()
        queue.put((0, start, []))
        
        while not queue.empty():
            cost, current, path = queue.get()
            
            if current:
                self.visited_nodes.append(current)

            if current == target:
                self.current_path = path if path else []
                cf.total_visited = len(visited)
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
    
    def reconstruct_path(self,came_from, current_state):
        path = []
        while current_state is not None:
            state, move, _ = came_from.get(current_state, (None, None, None))
            if move is not None:
                path.insert(0, (state, move, None))
            current_state = state
        return path
    
    def a_star(self, start, target):
        open_set = PriorityQueue()
        open_set.put((0, start))  
        came_from = {}
        g_score = {start: 0}  
        while not open_set.empty():
            _, current = open_set.get()
            
            if current:
                self.visited_nodes.append(current)

            if current == target:
                path = self.reconstruct_path(came_from, current)
                self.current_path = [move for (_, move, _) in path]
                cf.total_visited = len(self.visited_nodes)
                return [move for (_, move, _) in path]

           
            if target == self.snake.body[0]:
                for neighbor in self.get_valid_neighbors_new(current):
                    tentative_g_score = g_score[current] + 1 
                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = (current, neighbor, None)
                        g_score[neighbor] = tentative_g_score
                        f_score = tentative_g_score + self.heuristic(neighbor, target)
                        open_set.put((f_score, neighbor))
            else:
                for neighbor in self.get_valid_neighbors(current):
                    tentative_g_score = g_score[current] + 1 
                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = (current, neighbor, None)
                        g_score[neighbor] = tentative_g_score
                        f_score = tentative_g_score + self.heuristic(neighbor, target)
                        open_set.put((f_score, neighbor))
        return None
    
    def greedy(self, start, target):
        visited = set()
        queue = PriorityQueue()
        queue.put((self.heuristic(start, target), start, []))

        while not queue.empty():
            _, current, path = queue.get()

            if current:
                self.visited_nodes.append(current)

            if current == target:
                self.current_path = path if path else []
                cf.total_visited = len(visited)
                return path

            if current not in visited:
                visited.add(current)
                if target == self.snake.body[0]:
                    for neighbor in self.get_valid_neighbors_new(current):
                        queue.put((self.heuristic(neighbor, target), neighbor, path + [neighbor]))
                else:
                    for neighbor in self.get_valid_neighbors(current):
                        queue.put((self.heuristic(neighbor, target), neighbor, path + [neighbor]))

        return None
    def beam_search(self, start, target, beam_width):
        visited = set()
        queue = PriorityQueue()
        queue.put((self.heuristic(start, target), start, []))

        while not queue.empty():
            candidates = []
            for _ in range(queue.qsize()):
                _, current, path = queue.get()
                
                if current:
                    self.visited_nodes.append(current)
                
                if current == target:
                    self.current_path = path if path else []
                    cf.total_visited = len(visited)
                    return path

                if current not in visited:
                    visited.add(current)
                    if target == self.snake.body[0]:
                        neighbors = self.get_valid_neighbors_new(current)
                    else:
                        neighbors = self.get_valid_neighbors(current)

                    for neighbor in neighbors:
                        candidates.append((self.heuristic(neighbor, target), neighbor, path + [neighbor]))

            candidates = sorted(candidates, key=lambda x: x[0])[:beam_width]
            for candidate in candidates:
                queue.put(candidate)

        return None


    def get_valid_neighbors(self, position):
        x, y = position
        valid_neighbors = []

        for dx, dy in [(1, 0), (-1, 0), (0, -1), (0, 1)]:
            new_x, new_y = x + dx, y + dy
            if (0 <= new_x < self.width) and (0 <= new_y < self.height) \
                and (new_x, new_y) not in self.snake.body \
                and (new_x, new_y) not in [(obstacle.x, obstacle.y) for obstacle in self.obstacles]:
                valid_neighbors.append((new_x, new_y))

        return valid_neighbors
    
    def get_valid_neighbors_new(self, position):
        x, y = position
        valid_neighbors = []

        for dx, dy in [(1, 0), (-1, 0), (0, -1), (0, 1)]:
            new_x, new_y = x + dx, y + dy
            if (0 <= new_x < self.width) and (0 <= new_y < self.height) \
                and (new_x, new_y) not in self.snake.body[1:-1] \
                and (new_x, new_y) not in [(obstacle.x, obstacle.y) for obstacle in self.obstacles]:
                valid_neighbors.append((new_x, new_y))

        return valid_neighbors

    def find_by_algorithm(self, start, target, algorithm):
        if algorithm == "BFS":
            return self.bfs(start, target)
        elif algorithm == "UCS":
            return self.ucs(start, target)
        elif algorithm == "GREEDY":
            return self.greedy(start, target)
        elif algorithm == "ASTAR":
            return self.a_star(start, target)
        elif algorithm == "DFS":
            return self.dfs(start, target, 1050)
        elif algorithm == "IDS":
            return self.ids(start, target)
        elif algorithm == "BEAM":
            return self.beam_search(start, target, 10)
        
    def simulate_algorithm(self, algorithm):
        if not self.game_over():
            start = self.snake.body[-1]
            target = self.food.food
            
            path = self.find_by_algorithm(start, target, algorithm)
            if path:
                self.path = [(path[0][0] - start[0], path[0][1] - start[1])]
                self.path.extend((path[i][0] - path[i-1][0], path[i][1] - path[i-1][1]) for i in range(1, len(path)))
            else:
                tail = self.snake.body[0]
                path = self.find_by_algorithm(start, tail, algorithm)
                if path:
                    self.path = [(path[0][0] - start[0], path[0][1] - start[1])]
                    self.path.extend((path[i][0] - path[i-1][0], path[i][1] - path[i-1][1]) for i in range(1, len(path)))         
                else:
                        choose_longest_path = self.choose_longest_path(start)
                        if choose_longest_path:
                            self.path = [choose_longest_path]  
                        else:
                            head_direction = (self.snake.body[-1][0] - self.snake.body[-2][0], self.snake.body[-1][1] - self.snake.body[-2][1])
                            self.path = [head_direction]

    def choose_longest_path(self, start):
        directions = [(1, 0), (-1, 0)]
        best_direction = None
        
        for dx, dy in directions:
            new_x, new_y = start[0] + dx, start[1] + dy
            space_count = 0
            if (0 <= new_x < self.width) and (0 <= new_y < self.height) \
                    and (new_x, new_y) not in self.snake.body \
                    and (new_x, new_y) not in [(obstacle.x, obstacle.y) for obstacle in self.obstacles]:
            
                best_direction = (dx, dy)
        if best_direction:
            return best_direction
        else:
            directions = [(0, -1), (0, 1)]
            max_space = 0
            best_direction = None
            
            for dx, dy in directions:
                new_x, new_y = start[0] + dx, start[1] + dy
                space_count = 0
                while (0 <= new_x < self.width) and (0 <= new_y < self.height) \
                        and (new_x, new_y) not in self.snake.body \
                        and (new_x, new_y) not in [(obstacle.x, obstacle.y) for obstacle in self.obstacles]:
                    space_count += 1
                    new_x += dx
                    new_y += dy

                if space_count > max_space:
                    max_space = space_count
                    best_direction = (dx, dy)

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
        
