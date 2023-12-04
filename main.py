import pygame
from Game.snake import Snake
from Game.obstacle import Obstacle
from Game.gameLogic import GameLogic
from Graphics.background import Background
from Graphics.button import Button, RoundButton
import Game.colors as color
from Game.ranks import ranks
import Game.config as cf
import time as time
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
nums_font = pygame.font.Font("Resources/fonts/October Night.ttf", 30)

btn_bfs_rect = pygame.Rect(SCREEN_WIDTH + 60, 70, 160, 60)
btn_bfs = Button(window, btn_bfs_rect, "BFS", color.WHITE, font)

btn_ucs_rect = pygame.Rect(SCREEN_WIDTH + 60, 140, 160, 60)
btn_ucs = Button(window, btn_ucs_rect, "UCS", color.WHITE, font)

btn_a_star_rect = pygame.Rect(SCREEN_WIDTH + 60, 210, 160, 60)
btn_a_star = Button(window, btn_a_star_rect, "ASTAR", color.WHITE, font)

btn_greedy_rect = pygame.Rect(SCREEN_WIDTH + 60, 280, 160, 60)
btn_greedy = Button(window, btn_greedy_rect, "GREEDY", color.WHITE, font)

btn_dfs_rect = pygame.Rect(SCREEN_WIDTH + 230, 70, 160, 60)
btn_dfs = Button(window, btn_dfs_rect, "DFS", color.WHITE, font)

btn_ids_rect = pygame.Rect(SCREEN_WIDTH + 230, 140, 160, 60)
btn_ids = Button(window, btn_ids_rect, "IDS", color.WHITE, font)

btn_beam_rect = pygame.Rect(SCREEN_WIDTH + 230, 210, 160, 60)
btn_beam = Button(window, btn_beam_rect, "BEAM", color.WHITE, font)

btn_reset_rect = pygame.Rect(SCREEN_WIDTH + 230, 280, 160, 60)
btn_reset = Button(window, btn_reset_rect, "RESET", color.DARK_RED, font)

btn_start_rect = pygame.Rect(WIDTH //2 - 100, HEIGHT //2 - 50 , 200, 70)
btn_start = Button(window, btn_start_rect, "START", color.WHITE, font)

btn_setting_rect = pygame.Rect(WIDTH //2 - 100, HEIGHT //2 - 50 + 70 , 200, 70)
btn_setting = Button(window, btn_setting_rect, "SETTING", color.WHITE, font)

btn_quit_rect = pygame.Rect(WIDTH //2 - 100, HEIGHT //2 - 50+ 140 , 200, 70)
btn_quit = Button(window, btn_quit_rect, "QUIT", color.WHITE, font)

btn_edit_obstacles_rect = pygame.Rect(SCREEN_WIDTH // 3 + 20,  655, 160, 60)
btn_edit = Button(window, btn_edit_obstacles_rect, "Edit", color.GREEN, font)

btn_clear_obstacles_rect = pygame.Rect(SCREEN_WIDTH // 3 + 190, 655, 160, 60)
btn_clear = Button(window, btn_clear_obstacles_rect, "Clear", color.GREEN, font)

btn_save_obstacles_rect = pygame.Rect(SCREEN_WIDTH // 3 + 360, 655, 160, 60)
btn_save = Button(window, btn_save_obstacles_rect, "Save", color.GREEN, font)

btn_music_toggle = RoundButton(window, (40, 685), 30, "Resources/btn_music.png")

btn_music_mute = RoundButton(window, (40, 685), 30, "Resources/btn_music_mute.png")
btn_music = RoundButton(window, (40, 685), 30, "Resources/btn_music.png")

btn_pause_toggle = RoundButton(window, (110, 685), 30, "Resources/btn_pause.png")
btn_pause = RoundButton(window, (110, 685), 30, "Resources/btn_pause.png")
btn_unpause = RoundButton(window, (110, 685), 30, "Resources/btn_unpause.png")

btn_exit = RoundButton(window, (180, 685), 30, "Resources/btn_home.png")

btn_close = RoundButton(window, (WIDTH // 2 + 150, 600), 30, "Resources/btn_close.png")

btn_dec_player_speed = RoundButton(window, (WIDTH // 2 + 100, 270), 15,"Resources/btn_minus.png")
btn_inc_player_speed = RoundButton(window, (WIDTH // 2 + 170, 270), 15,"Resources/btn_plus.png")

btn_dec_AI_speed = RoundButton(window, (WIDTH // 2 + 100, 310), 15,"Resources/btn_minus.png")
btn_inc_AI_speed = RoundButton(window, (WIDTH // 2 + 170, 310), 15,"Resources/btn_plus.png")

btn_dec_AI_speed_ingame = RoundButton(window, (WIDTH // 2 + 310, HEIGHT // 2 + 330), 15,"Resources/btn_minus.png")
btn_inc_AI_speed_ingame = RoundButton(window, (WIDTH // 2 + 380,  HEIGHT // 2 + 330), 15,"Resources/btn_plus.png")

player_speed = 15
AI_speed = 30
player_speed_text = setting_font.render("PLAYER SPEED", True, color.WHITE)
AI_speed_text = setting_font.render("AI SPEED", True, color.WHITE)

volume_text = setting_font.render("MUSIC", True, color.WHITE)
current_volume = background.background_music_volume
volume_slider = pygame.Rect(WIDTH // 3 + 200, 340, 165, 20) 

skin_text = setting_font.render("CHANGE SKIN", True, color.WHITE)
current_skin_index = cf.current_skin_index
btn_back_skin = RoundButton(window, (WIDTH // 2 + 110, 390), 15,"Resources/btn_back.png")
btn_next_skin = RoundButton(window, (WIDTH // 2 + 170, 390), 15,"Resources/btn_next.png")

def display_message(message, color, screen, position, highboard=None):
    popup_font = pygame.font.Font("Resources/fonts/October Night.ttf", 40)
    lines = message.split('\n')
    line_height = (popup_font.get_linesize() - 17)

    for i, line in enumerate(lines):
        popup_text = popup_font.render(line, True, color)
        popup_rect = popup_text.get_rect(center=(position[0], position[1] + i * line_height))
        screen.blit(popup_text, popup_rect)

    if highboard is not None:
        high_scores_font = pygame.font.Font("Resources/fonts/October Night.ttf", 35)
        highboard_lines = highboard.split('\n')
        for j, highboard_line in enumerate(highboard_lines):
            high_scores_text = high_scores_font.render(highboard_line, True, color)
            high_scores_rect = high_scores_text.get_rect(center=(position[0], position[1] + (j - 10) * line_height))
            screen.blit(high_scores_text, high_scores_rect)
        display_message("--------------------------------", color, screen, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 160), highboard=None) 

def main():
    global player_speed, AI_speed
    playing = False
    start = False
    is_over = False
    using_algorithm = False
    selected_algorithm = ""
    setting_clicked = False
    is_creating = False
    mouse_dragging = False
    last_obstacle_x, last_obstacle_y = None, None
    background.start_background_music()
    global current_skin_index
    while True:
        background.draw_menu(window)
        background.draw_logo(window)
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
                    elif btn_setting_rect.collidepoint(event.pos) and not playing and not setting_clicked:
                        setting_clicked = True
                    elif btn_exit.collidepoint(event.pos) and not setting_clicked:
                        playing = False
                        start = False
                        using_algorithm = False
                    elif btn_reset_rect.collidepoint(event.pos):
                        game_logic.restart_game()
                        game_logic.reset_nodes()
                        using_algorithm = False
                    elif btn_edit_obstacles_rect.collidepoint(event.pos) and not setting_clicked and not is_over:
                        is_creating = True
                        mouse_dragging= True
                        new_obstacle = None
                        while is_creating:
                            for sub_event in pygame.event.get():
                                if sub_event.type == pygame.QUIT:
                                    pygame.quit()
                                    return
                                elif sub_event.type == pygame.MOUSEBUTTONDOWN and sub_event.button == 1:
                                    obstacle_x = (sub_event.pos[0] - 30) // GRID_SIZE
                                    obstacle_y = (sub_event.pos[1] - 30) // GRID_SIZE
                                    if (0 <= obstacle_x < SCREEN_WIDTH // GRID_SIZE) and (0 <= obstacle_y < SCREEN_HEIGHT // GRID_SIZE):
                                        obstacle_at_pos = game_logic.get_obstacle(obstacle_x,obstacle_y)
                                        if obstacle_at_pos:
                                            game_logic.remove_obstacles(obstacle_at_pos)
                                        elif (obstacle_x,obstacle_y) not in game_logic.obstacles \
                                            and (obstacle_x,obstacle_y) not in snake.body and (obstacle_x,obstacle_y) != food.food:
                                            new_obstacle = Obstacle(obstacle_x, obstacle_y)
                                            game_logic.obstacles.append(new_obstacle)
                                            
                                            obstacle_rect = new_obstacle.image.get_rect(topleft=(30 + new_obstacle.x * GRID_SIZE, 
                                                                                                    30 + new_obstacle.y * GRID_SIZE))
                                            window.blit(new_obstacle.image, obstacle_rect)
                                            pygame.display.update(obstacle_rect)
                                    if btn_save_obstacles_rect.collidepoint(sub_event.pos):
                                        is_creating = False
                                elif sub_event.type == pygame.MOUSEMOTION and sub_event.buttons[0] == 1 and mouse_dragging:
                                    obstacle_x = (sub_event.pos[0] - 30) // GRID_SIZE
                                    obstacle_y = (sub_event.pos[1] - 30) // GRID_SIZE
                                    if (obstacle_x, obstacle_y) != (last_obstacle_x, last_obstacle_y):
                                        if (0 <= obstacle_x < SCREEN_WIDTH // GRID_SIZE) and (0 <= obstacle_y < SCREEN_HEIGHT // GRID_SIZE):
                                            obstacle_at_pos = game_logic.get_obstacle(obstacle_x,obstacle_y)
                                            if obstacle_at_pos:
                                                game_logic.remove_obstacles(obstacle_at_pos)
                                            elif (obstacle_x,obstacle_y) not in game_logic.obstacles \
                                                and (obstacle_x,obstacle_y) not in snake.body and (obstacle_x,obstacle_y) != food.food:
                                                new_obstacle = Obstacle(obstacle_x, obstacle_y)
                                                game_logic.obstacles.append(new_obstacle)
                                                
                                                obstacle_rect = new_obstacle.image.get_rect(topleft=(30 + new_obstacle.x * GRID_SIZE, 
                                                                                                        30 + new_obstacle.y * GRID_SIZE))
                                                window.blit(new_obstacle.image, obstacle_rect)
                                                pygame.display.update(obstacle_rect)
                                            elif sub_event.type == pygame.MOUSEBUTTONUP and sub_event.button == 1:
                                                mouse_dragging = False
                                        last_obstacle_x, last_obstacle_y = obstacle_x, obstacle_y
                                    if btn_save_obstacles_rect.collidepoint(sub_event.pos):
                                        is_creating = False
                    elif btn_clear_obstacles_rect.collidepoint(event.pos) and not setting_clicked:
                        game_logic.obstacles = []
                    elif btn_close.collidepoint(event.pos) and setting_clicked:
                        setting_clicked = False
                    elif btn_dec_player_speed.collidepoint(event.pos) and setting_clicked:
                        if player_speed > 10:
                            player_speed -= 5
                    elif btn_inc_player_speed.collidepoint(event.pos) and setting_clicked:
                        if player_speed < 20:
                            player_speed += 5
                    elif btn_dec_AI_speed.collidepoint(event.pos) and setting_clicked:
                        if AI_speed > 15:
                            AI_speed -= 10
                    elif btn_inc_AI_speed.collidepoint(event.pos) and setting_clicked:
                        if AI_speed < 90:
                            AI_speed += 10
                    elif btn_dec_AI_speed_ingame.collidepoint(event.pos) and start:
                        if AI_speed > 15:
                            AI_speed -= 10
                    elif btn_inc_AI_speed_ingame.collidepoint(event.pos) and start:
                        if AI_speed < 90:
                            AI_speed += 10
                    elif volume_slider.collidepoint(event.pos) and setting_clicked:
                            global current_volume
                            current_volume = (event.pos[0] - volume_slider.x) / volume_slider.width
                            current_volume = max(0, min(1, current_volume))
                            background.set_volume_background_music(current_volume)
                    elif btn_back_skin.collidepoint(event.pos) and setting_clicked:
                        if current_skin_index > 0:
                            current_skin_index -= 1
                        snake.change_skin(current_skin_index)
                    elif btn_next_skin.collidepoint(event.pos) and setting_clicked:
                        if current_skin_index < 3:
                            current_skin_index += 1
                        snake.change_skin(current_skin_index)
                    elif btn_quit_rect.collidepoint(event.pos) and not playing and not setting_clicked:
                        pygame.quit()
                        return 
                    elif btn_music_toggle.collidepoint(event.pos) and not is_over:
                            if game_logic.is_on_music:
                                btn_music_toggle.image = btn_music_mute.image
                                background.pause_background_music()
                                game_logic.is_on_music = False
                            else:
                                btn_music_toggle.image = btn_music.image
                                background.unpause_background_music()
                                game_logic.is_on_music = True
                
                    elif btn_pause_toggle.collidepoint(event.pos) and not is_over:
                        game_logic.toggle_pause()
                        if game_logic.is_paused:
                            btn_pause_toggle.image = btn_unpause.image
                        else: 
                            btn_pause_toggle.image = btn_pause.image
            
            if playing:
                if event.type == pygame.KEYDOWN and not game_logic.is_paused:
                    game_logic.snake.set_moving(True)
                    if event.key == pygame.K_SPACE:
                        if game_logic.game_over():
                            # if game_logic.is_paused:
                            btn_music_toggle.image = btn_music.image
                            background.unpause_background_music()
                            game_logic.is_on_music = True
                            is_over = False
                            using_algorithm = False
                            game_logic.reset_nodes()
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
                                elif btn_ucs_rect.collidepoint(event.pos):
                                    using_algorithm = True
                                    selected_algorithm = "UCS"
                                elif btn_a_star_rect.collidepoint(event.pos):
                                    using_algorithm = True
                                    selected_algorithm = "ASTAR"
                                elif btn_greedy_rect.collidepoint(event.pos):
                                    using_algorithm = True
                                    selected_algorithm = "GREEDY"
                                elif btn_dfs_rect.collidepoint(event.pos):
                                    using_algorithm = True
                                    selected_algorithm = "DFS"
                                elif btn_ids_rect.collidepoint(event.pos):
                                    using_algorithm = True
                                    selected_algorithm = "IDS"
                                elif btn_beam_rect.collidepoint(event.pos):
                                    using_algorithm = True
                                    selected_algorithm = "BEAM"
        #draw button in game
        if start:
            background.draw(window)
            btn_bfs.draw()
            btn_ucs.draw()
            btn_a_star.draw()
            btn_greedy.draw()
            btn_dfs.draw()
            btn_ids.draw()
            btn_beam.draw()
            btn_reset.draw()
            window.blit(AI_speed_text, (WIDTH // 2 + 290, HEIGHT // 2 + 270))
            window.blit(default_font.render(str(AI_speed), True, color.WHITE), (WIDTH // 2 + 330, HEIGHT // 2 + 320))
            btn_dec_AI_speed_ingame.draw()
            btn_inc_AI_speed_ingame.draw()
            btn_exit.draw()            
            btn_edit.draw()
            btn_clear.draw()
            btn_save.draw()
            background.draw_logo(window)
            
        if not start:
            btn_start.draw()
            btn_setting.draw()
            btn_quit.draw()
        if using_algorithm:
            if not game_logic.game_over():
                window.blit(nums_font.render(f"SIMULATING: {selected_algorithm}", True, color.LIGHT_BLUE), (SCREEN_WIDTH + 70, 350))
                
                if not game_logic.is_paused:
                    if selected_algorithm == "BFS":
                        if not game_logic.path:
                            game_logic.reset_nodes()
                            start = time.time()
                            game_logic.simulate_algorithm(selected_algorithm)
                            end = time.time()
                            cf.time_exec = end - start
                        else:
                            game_logic.move_along_path()
                    elif selected_algorithm == "UCS":
                        if not game_logic.path:
                            game_logic.reset_nodes()
                            start = time.time()
                            game_logic.simulate_algorithm(selected_algorithm)
                            end = time.time()
                            cf.time_exec = end - start
                        else:
                            game_logic.move_along_path()
                    elif selected_algorithm == "ASTAR":
                        if not game_logic.path:
                            game_logic.reset_nodes()
                            start = time.time()
                            game_logic.simulate_algorithm(selected_algorithm)
                            end = time.time()
                            cf.time_exec = end - start
                        else:
                            game_logic.move_along_path()
                    elif selected_algorithm == "GREEDY":
                        if not game_logic.path:
                            game_logic.reset_nodes()
                            start = time.time()
                            game_logic.simulate_algorithm(selected_algorithm)
                            end = time.time()
                            cf.time_exec = end - start
                        else:
                            game_logic.move_along_path()
                    elif selected_algorithm == "DFS":
                        if not game_logic.path:
                            game_logic.reset_nodes()
                            start = time.time()
                            game_logic.simulate_algorithm(selected_algorithm)
                            end = time.time()
                            cf.time_exec = end - start
                        else:
                            game_logic.move_along_path()
                    elif selected_algorithm == "IDS":
                        if not game_logic.path:
                            game_logic.reset_nodes()
                            start = time.time()
                            game_logic.simulate_algorithm(selected_algorithm)
                            end = time.time()
                            cf.time_exec = end - start
                        else:
                            game_logic.move_along_path()
                    elif selected_algorithm == "BEAM":
                        if not game_logic.path:
                            game_logic.reset_nodes()
                            start = time.time()
                            game_logic.simulate_algorithm(selected_algorithm)
                            end = time.time()
                            cf.time_exec = end - start
                        else:
                            game_logic.move_along_path()
                window.blit(nums_font.render(f"VISITED: {cf.total_visited}", True, color.LIGHT_BLUE), (SCREEN_WIDTH + 70, 390))
                window.blit(nums_font.render(f"TIME: {cf.time_exec}", True, color.LIGHT_BLUE), (SCREEN_WIDTH + 70, 430))
                    

        if setting_clicked:
            setting_rect = pygame.Surface((SCREEN_WIDTH // 2 + 50, SCREEN_HEIGHT // 2 + 100), pygame.SRCALPHA)
            setting_rect.fill(color.DARK_GREEN)
            window.blit(setting_rect, (WIDTH // 3 - 20, HEIGHT // 3))
            window.blit(player_speed_text, (WIDTH // 3, HEIGHT // 3 + 10))
            window.blit(AI_speed_text, (WIDTH // 3, HEIGHT // 3 + 50))
            window.blit(default_font.render(str(player_speed), True, color.WHITE), (WIDTH // 3 + 305, HEIGHT // 3 + 20))
            window.blit(default_font.render(str(AI_speed), True, color.WHITE), (WIDTH // 3 + 305, HEIGHT // 3 + 60))
            btn_dec_player_speed.draw()
            btn_inc_player_speed.draw()
            btn_dec_AI_speed.draw()
            btn_inc_AI_speed.draw()
            btn_next_skin.draw()
            btn_back_skin.draw()
            window.blit(volume_text, (WIDTH // 3, HEIGHT // 3 + 90))
            pygame.draw.rect(window, color.WHITE, volume_slider)
            pygame.draw.rect(window, color.GREEN, (volume_slider.x, volume_slider.y, current_volume * volume_slider.width, volume_slider.height))
            window.blit(skin_text, (WIDTH // 3, HEIGHT // 3 + 130))
            window.blit(default_font.render(str(current_skin_index), True, color.WHITE), (WIDTH // 3 + 315, HEIGHT // 3 + 140))
            current_skin_preview = pygame.image.load(f'Resources/skin/skin_{current_skin_index}/full.png').convert_alpha()
            current_skin_preview = pygame.transform.scale(current_skin_preview, (300, 180))
            window.blit(current_skin_preview, (WIDTH // 3 + 25, HEIGHT // 3 + 190))
            btn_close.draw()


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

            # Draw obstacles
            game_logic.draw_obstacles(screen)

            # Display score screen
            score = game_logic.get_score()
            display_message(f" SCORE: {score}", color.LIGHT_RED,window, (SCREEN_WIDTH + 215, 40))
            if game_logic.game_over():
                if not is_over:
                    background.pause_background_music()
                    rank = ranks(score)
                    high_scores = rank.high_score(score)
                    highboard = '\n'.join(high_scores['High score'].astype(str))
                    is_over = True
                screen.fill(color.BLACK)
                display_message("HIGH SCORES", color.RED, screen, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 250), highboard=None) 
                display_message("--------------------------------", color.RED, screen, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 205), highboard=None) 
                display_message(f"\nGAME OVER - Press SPACE to restart! \n Your scores: {score}",
                                    color.RED, screen, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 170),
                                    highboard=highboard)    

            # window.blit(font.render(f"VISITED: {cf.visited}", True, color.LIGHT_BLUE), (SCREEN_WIDTH + 70, 380))

            window.blit(screen, (30, 30))
        
        #draw button (only on menu game)
        if start:
            btn_music_toggle.draw()
            btn_pause_toggle.draw()
        pygame.display.update()
        
        #FPS
        if using_algorithm:
            clock.tick(AI_speed)
        else:
            clock.tick(player_speed)

if __name__ == "__main__":
    main()
