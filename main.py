import pygame
from pygame.math import Vector2
from Game.snake import Snake
from Game.gameLogic import GameLogic
from Graphics.background import Background
from Graphics.button import Button, RoundButton
import Game.colors as color
from Game.ranks import ranks
import Game.config as cf
import random
pygame.init()

WIDTH, HEIGHT = cf.WIDTH, cf.HEIGHT
SCREEN_WIDTH, SCREEN_HEIGHT = cf.SCREEN_WIDTH, cf.SCREEN_HEIGHT
GRID_SIZE = cf.GRID_SIZE
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

pygame.display.set_caption("Snake Game")
window = cf.window
screen = cf.screen
btn_screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
snake = Snake(GRID_WIDTH // 2, GRID_HEIGHT // 2)
game_logic = GameLogic(snake, GRID_WIDTH, GRID_HEIGHT)
food = game_logic.food
clock = pygame.time.Clock()
background = Background(WIDTH, HEIGHT)


score = 0

# font = pygame.font.Font(pygame.font.get_default_font(), 40)
font = pygame.font.Font("Resources/fonts/Coconut Cookies.ttf", 40)

#button solve
btn_bfs_rect = pygame.Rect(SCREEN_WIDTH + 120, 100, 180, 60)
btn_bfs = Button(window, btn_bfs_rect, "BFS", color.WHITE, font)

btn_ucs_rect = pygame.Rect(SCREEN_WIDTH + 120, 180, 180, 60)
btn_ucs = Button(window, btn_ucs_rect, "UCS", color.WHITE, font)

#button start
btn_start_rect = pygame.Rect(WIDTH //2 - 100, HEIGHT //2 - 50 , 180, 60)
btn_start = Button(window, btn_start_rect, "Start", color.WHITE, font)

btn_setting_rect = pygame.Rect(WIDTH //2 - 100, HEIGHT //2 - 50 + 70 , 180, 60)
btn_setting = Button(window, btn_setting_rect, "Setting", color.WHITE, font)
#button quit
btn_quit_rect = pygame.Rect(WIDTH //2 - 100, HEIGHT //2 - 50+ 140 , 180, 60)
btn_quit = Button(window, btn_quit_rect, "Quit", color.WHITE, font)

#button exit
btn_exit_rect = pygame.Rect(SCREEN_WIDTH + 120, 260, 180, 60)
btn_exit = Button(window, btn_exit_rect, "Exit", color.WHITE, font)

btn_music_toggle = RoundButton(window, (40, 685), 30, "Resources/btn_music.png")

btn_music_mute = RoundButton(window, (40, 685), 30, "Resources/btn_music_mute.png")
btn_music = RoundButton(window, (40, 685), 30, "Resources/btn_music.png")

btn_pause_toggle = RoundButton(window, (120, 685), 30, "Resources/btn_pause.png")
btn_pause = RoundButton(window, (120, 685), 30, "Resources/btn_pause.png")
btn_unpause = RoundButton(window, (120, 685), 30, "Resources/btn_unpause.png")

pause = False

def display_message(message, color, screen, screen_size):
    popup_font = pygame.font.Font(None, 48)
    popup_text = popup_font.render(message, True, color)
    popup_rect = popup_text.get_rect(center=(screen_size[0], screen_size[1]))
    screen.blit(popup_text, popup_rect)

def main():
    playing = False
    start = False
    is_over = False
    using_algorithm = False
    selected_alogrithm = ""
    setting_clicked = False
    background.start_background_music()
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
                        game_logic.is_paused = False
                        game_logic.snake.set_moving(True)
                        game_logic.restart_game()
                    elif btn_setting_rect.collidepoint(event.pos) and not playing:
                        setting_clicked = True
                        print("SETTING")
                    elif btn_exit_rect.collidepoint(event.pos):
                        playing = False
                        start = False
                        using_algorithm = False
                    elif btn_quit_rect.collidepoint(event.pos) and not playing:
                        pygame.quit()
                        return 
                
            if playing:
                if event.type == pygame.KEYDOWN and not game_logic.is_paused:
                    game_logic.snake.set_moving(True)
                    if event.key == pygame.K_SPACE:
                        if game_logic.game_over():
                            background.unpause_background_music()
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
                            if btn_bfs_rect.collidepoint(event.pos):
                                using_algorithm = True
                                selected_alogrithm = "BFS"
                            elif btn_ucs_rect.collidepoint(event.pos):
                                using_algorithm = True
                                selected_alogrithm = "UCS"
                            elif btn_music_toggle.collidepoint(event.pos):
                                print("Music changed")
                                if game_logic.is_on_music:
                                    btn_music_toggle.image = btn_music_mute.image
                                    background.pause_background_music()
                                    game_logic.is_on_music = False
                                else:
                                    btn_music_toggle.image = btn_music.image
                                    background.unpause_background_music()
                                    game_logic.is_on_music = True
                            elif btn_pause_toggle.collidepoint(event.pos):
                                print("Paused")
                                game_logic.toggle_pause()
                                if game_logic.is_paused:
                                    if(game_logic.is_on_music):
                                        btn_music_toggle.image = btn_music_mute.image
                                        game_logic.is_on_music = False
                                    
                                    btn_pause_toggle.image = btn_unpause.image
                                else: 
                                    if(not game_logic.is_on_music):
                                        btn_music_toggle.image = btn_music.image
                                        game_logic.is_on_music = True
                                    btn_pause_toggle.image = btn_pause.image
        if start:
            background.draw(window)
            btn_bfs.draw()
            btn_ucs.draw()
            btn_exit.draw()            
        if not start:
            btn_start.draw()
            btn_setting.draw()
            btn_quit.draw()
        
        if setting_clicked:
            blur_rect = pygame.Surface((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), pygame.SRCALPHA)
            blur_rect.fill((0,0,0,128))
            window.blit(blur_rect, (200,200))
        if playing and not using_algorithm:
            game_logic.update()
        if playing:
            # Vẽ con rắn
            snake.draw_snake(screen)

            # Vẽ border
            background.draw_border(window)

            # Vẽ food
            screen.blit(game_logic.food.image, (food.food[0] * GRID_SIZE, food.food[1] * GRID_SIZE))
            # screen.blit(game_logic.food.image, game_logic.food.food_rect)

            # score
            score = game_logic.get_score()

            # score hiển thị màn hình
            display_message(f"Score: {score}",color.WHITE,window, (SCREEN_WIDTH + 200, 50))

            if game_logic.game_over():
                if not is_over:
                    background.pause_background_music()
                    rank = ranks(score)
                    rank.high_score(score)
                    is_over = True
                screen.fill(color.BLACK)
                display_message(f"Game Over - Press SPACE to restart! \n Your scores: {score}", 
                                color.RED, screen, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

            window.blit(screen, (30, 30))
        
        if using_algorithm:
            clock.tick(50)
        else:
            clock.tick(15)
        if using_algorithm and selected_alogrithm == "BFS":
            game_logic.visualize_bfs(screen, window)
            game_logic.move_along_path()

        if using_algorithm and selected_alogrithm == "UCS":
            game_logic.visualize_ucs(screen, window)
            game_logic.move_along_path()

        if start:
            btn_music_toggle.draw()
            btn_pause_toggle.draw()
        pygame.display.update()
if __name__ == "__main__":
    main()
