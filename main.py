import pygame
from pygame.math import Vector2
from Game.snake import Snake
from Game.gameLogic import GameLogic
from Graphics.background import Background
from Graphics.button import Button, RoundButton, ArrowButton
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

#init object
pygame.display.set_caption("Snake Game")
window = cf.window
screen = cf.screen
simulation_screen = pygame.Surface.copy(screen)
btn_screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
snake = Snake(GRID_WIDTH // 2, GRID_HEIGHT // 2)
game_logic = GameLogic(snake, GRID_WIDTH, GRID_HEIGHT)
food = game_logic.food
clock = pygame.time.Clock()
background = Background(WIDTH, HEIGHT)

score = 0

# Fonts
default_font = pygame.font.Font(None, 35)
font = pygame.font.Font("Resources/fonts/Coconut Cookies.ttf", 40)
setting_font = pygame.font.Font("Resources/fonts/Coconut Cookies.ttf", 35)

btn_bfs_rect = pygame.Rect(SCREEN_WIDTH + 120, 100, 180, 60)
btn_bfs = Button(window, btn_bfs_rect, "BFS", color.WHITE, font)

btn_ucs_rect = pygame.Rect(SCREEN_WIDTH + 120, 180, 180, 60)
btn_ucs = Button(window, btn_ucs_rect, "UCS", color.WHITE, font)

btn_a_star_rect = pygame.Rect(SCREEN_WIDTH + 120, 260, 180, 60)
btn_a_star = Button(window, btn_a_star_rect, "A star", color.WHITE, font)

btn_start_rect = pygame.Rect(WIDTH //2 - 100, HEIGHT //2 - 50 , 180, 60)
btn_start = Button(window, btn_start_rect, "START", color.WHITE, font)

btn_greedy_rect = pygame.Rect(SCREEN_WIDTH + 120, 340, 180, 60)
btn_greedy = Button(window, btn_greedy_rect, "Greedy", color.WHITE, font)

btn_setting_rect = pygame.Rect(WIDTH //2 - 100, HEIGHT //2 - 50 + 70 , 180, 60)
btn_setting = Button(window, btn_setting_rect, "SETTING", color.WHITE, font)

btn_quit_rect = pygame.Rect(WIDTH //2 - 100, HEIGHT //2 - 50+ 140 , 180, 60)
btn_quit = Button(window, btn_quit_rect, "QUIT", color.WHITE, font)

btn_exit_rect = pygame.Rect(SCREEN_WIDTH + 120, 420, 180, 60)
btn_exit = Button(window, btn_exit_rect, "Exit", color.WHITE, font)

btn_music_toggle = RoundButton(window, (40, 685), 30, "Resources/btn_music.png")

btn_music_mute = RoundButton(window, (40, 685), 30, "Resources/btn_music_mute.png")
btn_music = RoundButton(window, (40, 685), 30, "Resources/btn_music.png")

btn_pause_toggle = RoundButton(window, (120, 685), 30, "Resources/btn_pause.png")
btn_pause = RoundButton(window, (120, 685), 30, "Resources/btn_pause.png")
btn_unpause = RoundButton(window, (120, 685), 30, "Resources/btn_unpause.png")

btn_close = RoundButton(window, (WIDTH // 2 + 150, 600), 30, "Resources/btn_close.png")

btn_dec_player_speed = RoundButton(window, (WIDTH // 2 + 100, 270), 15,"Resources/btn_back.png")
btn_inc_player_speed = RoundButton(window, (WIDTH // 2 + 170, 270), 15,"Resources/btn_next.png")

btn_dec_AI_speed = RoundButton(window, (WIDTH // 2 + 100, 310), 15,"Resources/btn_back.png")
btn_inc_AI_speed = RoundButton(window, (WIDTH // 2 + 170, 310), 15,"Resources/btn_next.png")

player_speed = 15
AI_speed = 30
player_speed_text = setting_font.render("PLAYER SPEED", True, color.WHITE)
AI_speed_text = setting_font.render("AI SPEED", True, color.WHITE)

def display_message(message, color, screen, screen_size):
    popup_text = font.render(message, True, color)
    popup_rect = popup_text.get_rect(center=(screen_size[0], screen_size[1]))
    screen.blit(popup_text, popup_rect)

def main():
    global player_speed, AI_speed
    playing = False
    start = False
    is_over = False
    using_algorithm = False
    selected_algorithm = ""
    setting_clicked = False
    background.start_background_music()
    while True:
        background.draw_menu(window)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if btn_start_rect.collidepoint(event.pos) and not playing and not setting_clicked: 
                        playing = True
                        start = True
                        game_logic.is_paused = False
                        btn_pause_toggle.image = btn_pause.image
                        game_logic.snake.set_moving(True)
                        game_logic.restart_game()
                        background.reset_frame(screen)
                        game_logic.reset_nodes()
                        print(snake.direction)
                    elif btn_setting_rect.collidepoint(event.pos) and not playing and not setting_clicked:
                        setting_clicked = True
                        print("SETTING")
                    elif btn_exit_rect.collidepoint(event.pos) and not setting_clicked:
                        playing = False
                        start = False
                        using_algorithm = False
                    elif btn_close.collidepoint(event.pos):
                        setting_clicked = False
                    elif btn_dec_player_speed.collidepoint(event.pos):
                        if player_speed > 10:
                            player_speed -= 5
                    elif btn_inc_player_speed.collidepoint(event.pos):
                        if player_speed < 20:
                            player_speed += 5
                    elif btn_dec_AI_speed.collidepoint(event.pos):
                        if AI_speed > 30:
                            AI_speed -= 30
                    elif btn_inc_AI_speed.collidepoint(event.pos):
                        if AI_speed < 90:
                            AI_speed += 30
                    elif btn_quit_rect.collidepoint(event.pos) and not playing and not setting_clicked:
                        pygame.quit()
                        return 
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

                
            if playing:
                if event.type == pygame.KEYDOWN and not game_logic.is_paused:
                    game_logic.snake.set_moving(True)
                    if event.key == pygame.K_SPACE:
                        if game_logic.game_over():
                            if game_logic.is_paused:
                                btn_music_toggle.image = btn_music.image
                                background.unpause_background_music()
                            is_over = False
                            using_algorithm = False
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
                            if not using_algorithm:
                                if btn_bfs_rect.collidepoint(event.pos):
                                    using_algorithm = True
                                    selected_algorithm = "BFS"
                                    print(f"Algorithm: {selected_algorithm}")
                                elif btn_ucs_rect.collidepoint(event.pos):
                                    using_algorithm = True
                                    selected_algorithm = "UCS"
                                    print(f"Algorithm: {selected_algorithm}")
                                elif btn_a_star_rect.collidepoint(event.pos):
                                    using_algorithm = True
                                    selected_algorithm = "A star"
                                    print(f"Algorithm: {selected_algorithm}")
                                elif btn_greedy_rect.collidepoint(event.pos):
                                    using_algorithm = True
                                    selected_algorithm = "Greedy"
                                    print(f"Algorithm: {selected_algorithm}")
                            # elif btn_music_toggle.collidepoint(event.pos):
                            #     print("Music changed")
                            #     if game_logic.is_on_music:
                            #         btn_music_toggle.image = btn_music_mute.image
                            #         background.pause_background_music()
                            #         game_logic.is_on_music = False
                            #     else:
                            #         btn_music_toggle.image = btn_music.image
                            #         background.unpause_background_music()
                            #         game_logic.is_on_music = True
                            elif btn_pause_toggle.collidepoint(event.pos):
                                game_logic.toggle_pause()
                                if game_logic.is_paused:
                                    btn_pause_toggle.image = btn_unpause.image
                                    print("Paused")
                                else: 
                                    btn_pause_toggle.image = btn_pause.image
                                    print("unpaused")
        #draw button in game
        if start:
            background.draw(window)
            btn_bfs.draw()
            btn_ucs.draw()
            btn_a_star.draw()
            btn_greedy.draw()
            btn_exit.draw()            

        if not start:
            btn_start.draw()
            btn_setting.draw()
            btn_quit.draw()

        if using_algorithm: 
            if not game_logic.is_paused:
                if selected_algorithm == "BFS":
                    if not game_logic.path:
                        game_logic.reset_nodes()
                        game_logic.simulate_bfs(screen, window)
                    else:
                        game_logic.move_along_path()
        
                elif selected_algorithm == "UCS":
                    if not game_logic.path:
                        game_logic.reset_nodes()
                        game_logic.simulate_ucs(screen, window)
                    else:
                        game_logic.move_along_path()
                elif selected_algorithm == "A star":
                    if not game_logic.path:
                        game_logic.reset_nodes()
                        game_logic.simulate_astar(screen, window)
                    else:
                        game_logic.move_along_path()
                elif selected_algorithm == "Greedy":
                    if not game_logic.path:
                        game_logic.reset_nodes()
                        game_logic.simulate_greedy(screen, window)
                    else:
                        game_logic.move_along_path()

        if setting_clicked:
            setting_rect = pygame.Surface((SCREEN_WIDTH // 2 + 50, SCREEN_HEIGHT // 2 + 100), pygame.SRCALPHA)
            setting_rect.fill(color.DARK_GREEN)
            window.blit(setting_rect, (WIDTH // 3 - 20, HEIGHT // 3))
            window.blit(player_speed_text, (WIDTH // 3, HEIGHT // 3 + 10))
            window.blit(AI_speed_text, (WIDTH // 3, HEIGHT // 3 + 50))
            window.blit(default_font.render(str(player_speed), True, color.WHITE), (WIDTH // 3 + 305, HEIGHT // 3 + 20))
            window.blit(default_font.render(str(AI_speed), True, color.WHITE), (WIDTH // 3 + 305, HEIGHT // 3 + 60))
            btn_close.draw()
            btn_dec_player_speed.draw()
            btn_inc_player_speed.draw()
            btn_dec_AI_speed.draw()
            btn_inc_AI_speed.draw()
        if playing and not using_algorithm:
            game_logic.update()
        if playing:
            background.reset_frame(screen)

            if game_logic.visited_nodes:
                game_logic.draw_nodes(screen)

            # Draw snake
            snake.draw_snake(screen)

            # Draw border
            background.draw_border(window)

            # Draw food
            screen.blit(game_logic.food.image, (food.food[0] * GRID_SIZE, food.food[1] * GRID_SIZE))
            # screen.blit(game_logic.food.image, game_logic.food.food_rect)

            # Display score screen
            score = game_logic.get_score()
            display_message(f"Score: {score}",color.WHITE,window, (SCREEN_WIDTH + 200, 50))

            if game_logic.game_over():
                if not is_over:
                    background.pause_background_music()
                    rank = ranks(score)
                    rank.high_score(score)
                    is_over = True
                #screen.fill(color.BLACK)
                display_message(f"Game Over - Press SPACE to restart! \n Your scores: {score}", 
                                color.RED, screen, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

            window.blit(screen, (30, 30))
        
        #draw button (only on menu game)
        if start:
            btn_music_toggle.draw()
            btn_pause_toggle.draw()

        pygame.display.update()
        
        #FPS
        if using_algorithm:
            clock.tick(1000)
        else:
            clock.tick(player_speed)

if __name__ == "__main__":
    main()
