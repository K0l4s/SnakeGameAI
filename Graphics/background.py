import pygame

class Background:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.background_image = pygame.image.load("Resources/menu.jpg")
        self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))

        self.background_menu = pygame.image.load("Resources/menu_game.jpg")
        self.background_menu = pygame.transform.scale(self.background_menu, (self.width, self.height))

        #Set icon
        icon = pygame.Surface((200,156))
        icon_image = pygame.image.load("Resources/snake_icon.ico")
        icon.blit(icon_image, (0,0))
        pygame.display.set_icon(icon)

    def draw(self, window):
        window.blit(self.background_image, (0,0))
    def draw_menu(self,window):
        window.blit(self.background_menu, (0,0))