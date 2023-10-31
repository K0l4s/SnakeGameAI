import pygame
from Game.snake import Snake
from Game.gameLogic import GameLogic
from Graphics.background import Background

WIDTH, HEIGHT = 1400, 900
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 800
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY  = (96, 100, 107)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

def main():
    pygame.init()
    pygame.display.set_caption("Snake Game")
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    snake = Snake(GRID_WIDTH // 2, GRID_HEIGHT // 2)
    game_logic = GameLogic(snake, GRID_WIDTH, GRID_HEIGHT)
    clock = pygame.time.Clock()
    background = Background(WIDTH, HEIGHT)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    snake.change_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    snake.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction((1, 0))

        background.draw(window)
        game_logic.update()
        # Vẽ screen
        screen.fill(BLACK)
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                pygame.draw.rect(screen, GRAY, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

        pygame.draw.rect(screen, RED, (game_logic.food[0] * GRID_SIZE, game_logic.food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        # Vẽ rắn
        for segment in snake.body:
            pygame.draw.rect(screen, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        window.blit(screen, (50, 50))
        pygame.display.update()
        clock.tick(10)

    pygame.quit()

if __name__ == "__main__":
    main()
