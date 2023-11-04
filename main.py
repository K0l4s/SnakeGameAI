import pygame
from Game.snake import Snake
from Game.gameLogic import GameLogic
from Graphics.background import Background
from Game.food import Food
import Game.colors as color

WIDTH, HEIGHT = 1400, 900
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 800
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE


def display_message(message, screen, screen_size):
    popup_font = pygame.font.Font(None, 48)
    popup_text = popup_font.render(message, True, color.RED)
    popup_rect = popup_text.get_rect(center=(screen_size[0] // 2, screen_size[1] // 2))
    screen.blit(popup_text, popup_rect)
    
def main():
    pygame.init()
    pygame.display.set_caption("Snake Game")
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    snake = Snake(GRID_WIDTH // 2, GRID_HEIGHT // 2)
    game_logic = GameLogic(snake, GRID_WIDTH, GRID_HEIGHT)
    food = game_logic.food
    clock = pygame.time.Clock()
    background = Background(WIDTH, HEIGHT)
    playing = True

    score = 0
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_logic.game_over():
                        game_logic.restart_game()

                elif not game_logic.game_over():
                    if event.key == pygame.K_UP:
                        snake.change_direction((0, -1))
                    elif event.key == pygame.K_DOWN:
                        snake.change_direction((0, 1))
                    elif event.key == pygame.K_LEFT:
                        snake.change_direction((-1, 0))
                    elif event.key == pygame.K_RIGHT:
                        snake.change_direction((1, 0))

        background.draw(window)
        
        if not game_logic.game_over():
            game_logic.update()
            
        # Vẽ screen
        screen.fill(color.BLACK)
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                pygame.draw.rect(screen, color.GRAY, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)
                
        # Vẽ khung viền ngoài
        pygame.draw.rect(screen, color.WHITE, (0, 0, SCREEN_WIDTH + 1, SCREEN_HEIGHT + 1 ), 3 )
        
        # food
        pygame.draw.rect(screen, color.RED, (food.food[0] * GRID_SIZE, food.food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        
        # Vẽ rắn
        for segment in snake.body:
            pygame.draw.rect(screen, color.GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        window.blit(screen, (50, 50))
        
        # score
        score = game_logic.get_score()
        
        if game_logic.game_over():
            screen.fill(color.BLACK)
            
            display_message(f"Game Over - Press SPACE to restart\nYour scores: {score}", screen, (SCREEN_WIDTH, SCREEN_HEIGHT))
            window.blit(screen, (50, 50))

        pygame.display.update()
        clock.tick(10)

    pygame.quit()
if __name__ == "__main__":
    main()
