import pygame
import Game.config as cf
class Background:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.background_image = pygame.image.load("Resources/background.jpg")
        self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))

        self.background_menu = pygame.image.load("Resources/menu_game.jpg")
        self.background_menu = pygame.transform.scale(self.background_menu, (self.width, self.height))

        #Set icon
        icon = pygame.Surface((200,156))
        icon_image = pygame.image.load("Resources/snake_icon.ico")
        icon.blit(icon_image, (0,0))
        pygame.display.set_icon(icon)

        #
        self.block_image = pygame.image.load("Resources/block.jpg")
        self.block_image = pygame.transform.scale(self.block_image, (20, 20))

    def draw(self, window):
        window.blit(self.background_image, (0,0))
    def draw_menu(self,window):
        window.blit(self.background_menu, (0,0))
    def draw_border(self, window):
        for x in range(0, cf.SCREEN_WIDTH + 40, cf.GRID_SIZE):
            window.blit(self.block_image, (x + 10, 10))
            window.blit(self.block_image, (x + 10, cf.SCREEN_HEIGHT + 30))
        for y in range(0, cf.SCREEN_HEIGHT, cf.GRID_SIZE):
            window.blit(self.block_image, (0 + 10, y + 30))
            window.blit(self.block_image, (cf.SCREEN_WIDTH + 30, y + 30))