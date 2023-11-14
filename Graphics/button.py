import pygame

class Button:
    def __init__(self, screen, rect, text, text_color, font):
        self.screen = screen
        self.rect = rect
        self.text = text
        self.text_color = text_color
        self.font = font
        self.btn_image = pygame.image.load("Resources/btn_image.png")
        self.btn_image = pygame.transform.scale(self.btn_image, (180, 60))
        self.hover_image = self.create_hover_image(self.btn_image)

    def create_hover_image(self, image):
        hover_image = image.copy()
        hover_image.fill((255,255,255,190), None, pygame.BLEND_RGBA_MULT)
        return hover_image
    
    def check_hover(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
    
    def draw(self):
        text_alpha = 255
        mouse_pos = pygame.mouse.get_pos()
        if self.check_hover(mouse_pos):
            img = self.hover_image
            text_alpha = 190
        else:
            img = self.btn_image

        image_rect = img.get_rect()
        image_rect.center = self.rect.center
        self.screen.blit(img, image_rect)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_surface.set_alpha(text_alpha)
        text_rect = text_surface.get_rect()
        text_rect.center = self.rect.center
        self.screen.blit(text_surface, text_rect)