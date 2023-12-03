import pygame
WIDTH, HEIGHT = 1100, 720
SCREEN_WIDTH, SCREEN_HEIGHT = 700, 600
screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
window = pygame.display.set_mode((WIDTH, HEIGHT))
GRID_SIZE = 20
current_skin_index = 0
start_time, end_time, execution_time = 0, 0, 0

total_visited = 0
time_exec = 0