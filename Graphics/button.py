import pygame

class Button:
    def __init__(self, screen, rect, text, text_color, background_color, font):
        self.screen = screen
        self.rect = rect
        self.text = text
        self.text_color = text_color
        self.background_color = background_color
        self.font = font

    def draw(self):
        pygame.draw.rect(self.screen, self.background_color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect()
        text_rect.center = self.rect.center
        self.screen.blit(text_surface, text_rect)