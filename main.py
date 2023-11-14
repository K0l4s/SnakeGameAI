import pygame
from pygame.math import Vector2
from Game.snake import Snake
from Game.gameLogic import GameLogic
from Graphics.background import Background
from Graphics.button import Button
import Game.colors as color
from Game.ranks import ranks
import Game.config as cf
import random
pygame.init()

WIDTH, HEIGHT = 1400, 800
SCREEN_WIDTH, SCREEN_HEIGHT = 700, 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

pygame.display.set_caption("Snake Game")
# window = pygame.display.set_mode((WIDTH, HEIGHT))
# screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
window = cf.window
screen = cf.screen
btn_screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
snake = Snake(GRID_WIDTH // 2, GRID_HEIGHT // 2)
game_logic = GameLogic(snake, GRID_WIDTH, GRID_HEIGHT)
food = game_logic.food
clock = pygame.time.Clock()
background = Background(WIDTH, HEIGHT)


score = 0

font = pygame.font.Font(pygame.font.get_default_font(), 40)

#button solve
btn_solve_rect = pygame.Rect(SCREEN_WIDTH + 150, 150, 180, 50)
btn_solve = Button(window, btn_solve_rect, "Solve", color.WHITE, color.RED, font)

#button start
btn_start_rect = pygame.Rect(SCREEN_WIDTH //2 + 150, SCREEN_HEIGHT //2 , 180, 50)
btn_start = Button(window, btn_start_rect, "Start", color.WHITE, color.GREEN, font)

btn_setting_rect = pygame.Rect(SCREEN_WIDTH //2 + 150, SCREEN_HEIGHT //2 + 70 , 180, 50)
btn_setting = Button(window, btn_setting_rect, "Setting", color.WHITE, color.GREEN, font)
#button quit
btn_quit_rect = pygame.Rect(SCREEN_WIDTH //2 + 150, SCREEN_HEIGHT //2+ 140 , 180, 50)
btn_quit = Button(window, btn_quit_rect, "Quit", color.WHITE, color.RED, font)

#button exit
btn_exit_rect = pygame.Rect(SCREEN_WIDTH + 150, 250, 180, 50)
btn_exit = Button(window, btn_exit_rect, "Exit", color.WHITE, color.RED, font)

def display_message(message, color, screen, screen_size):
    popup_font = pygame.font.Font(None, 48)
    popup_text = popup_font.render(message, True, color)
    popup_rect = popup_text.get_rect(center=(screen_size[0] // 2, screen_size[1] // 2))
    screen.blit(popup_text, popup_rect)

def main():
    playing = False
    start = False
    is_over = False
    using_algorithm = False
    while True:
        background.draw_menu(window)
        image = pygame.image.load("Resources/background_note.png")
        image = pygame.transform.scale(image, (40, 40))
        # Vẽ background
        for x in range(0, 1280, image.get_width()):
            for y in range(0, 1280, image.get_height()):
                screen.blit(image, (x, y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if btn_start_rect.collidepoint(event.pos) and not playing:
                        playing = True
                        start = True
                        game_logic.snake.set_moving(True)
                        game_logic.restart_game()
                    # elif btn_setting.colilidepoint(event.pos) and not playing:
                    #     print("SETTING")
                    elif btn_exit_rect.collidepoint(event.pos):
                        playing = False
                        start = False
                        using_algorithm = False
                    elif btn_quit_rect.collidepoint(event.pos) and not playing:
                        pygame.quit()
                        return 

            if playing:
                if event.type == pygame.KEYDOWN:
                    game_logic.snake.set_moving(True)
                    if event.key == pygame.K_SPACE:
                        if game_logic.game_over():
                            is_over = False
                            game_logic.restart_game()
                    elif not game_logic.game_over() and not using_algorithm:
                        if event.key == pygame.K_UP:
                            snake.change_direction((0, -1))
                        elif event.key == pygame.K_DOWN:
                            snake.change_direction((0, 1))
                        elif event.key == pygame.K_LEFT:
                            snake.change_direction((-1, 0))
                        elif event.key == pygame.K_RIGHT:
                            snake.change_direction((1, 0))
                        game_logic.snake.set_moving(True)
                if not game_logic.game_over():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            if btn_solve_rect.collidepoint(event.pos):
                                using_algorithm = True
        if start:
            background.draw(window)
            btn_solve.draw()
            btn_exit.draw()            
        else:
            btn_start.draw()
            btn_setting.draw()
            btn_quit.draw()

        if playing and not using_algorithm:
            game_logic.update()
        if playing:
            # Vẽ con rắn
            snake.draw_snake(screen)

            # # Vẽ khung viền ngoài
            pygame.draw.rect(screen, color.WHITE, (0, 0, SCREEN_WIDTH + 1, SCREEN_HEIGHT + 1), 3)

            # Vẽ food
            screen.blit(game_logic.food.image, (food.food[0] * GRID_SIZE, food.food[1] * GRID_SIZE))
            # screen.blit(game_logic.food.image, game_logic.food.food_rect)

            # score
            score = game_logic.get_score()

            # score hiển thị màn hình
            display_message(f"Score: {score}",color.RED,window, (SCREEN_WIDTH + 1400, 150))

            if game_logic.game_over():
                if not is_over:
                    rank = ranks(score)
                    rank.high_score(score)
                    is_over = True
                screen.fill(color.BLACK)
                display_message(f"Game Over - Press SPACE to restart \n Your scores: {score}", 
                                color.RED, screen, (SCREEN_WIDTH, SCREEN_HEIGHT))

            window.blit(screen, (0, 0))
        
        if using_algorithm:
            clock.tick(50)
        else:
            clock.tick(15)
        if using_algorithm:
            game_logic.visualize_bfs(screen, window)
            game_logic.move_along_path()
        pygame.display.update()
if __name__ == "__main__":
    main()
