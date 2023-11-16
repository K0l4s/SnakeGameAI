import pygame 
class Snake:
    def __init__(self, x, y):
        self.body = [(x, y), (x-1, y)]
        self.direction = (-1, 0)
        self.is_moving = False
        self.tail_up = pygame.image.load('Resources/skin/ekans_skin/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Resources/skin/ekans_skin/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Resources/skin/ekans_skin/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Resources/skin/ekans_skin/tail_left.png').convert_alpha()

        self.head_up = pygame.image.load('Resources/skin/ekans_skin/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Resources/skin/ekans_skin/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Resources/skin/ekans_skin/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Resources/skin/ekans_skin/head_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Resources/skin/ekans_skin/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Resources/skin/ekans_skin/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Resources/skin/ekans_skin/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Resources/skin/ekans_skin/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Resources/skin/ekans_skin/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Resources/skin/ekans_skin/body_bl.png').convert_alpha()

        self.crunch_sound = pygame.mixer.Sound('Resources/Sound/crunch.wav')
        
        self.head_up = pygame.transform.scale(self.head_up, (20, 20))
        self.head_down = pygame.transform.scale(self.head_down, (20, 20))
        self.head_right = pygame.transform.scale(self.head_right, (20, 20))
        self.head_left = pygame.transform.scale(self.head_left, (20, 20))

        self.tail_up = pygame.transform.scale(self.tail_up, (20, 20))
        self.tail_down = pygame.transform.scale(self.tail_down, (20, 20))
        self.tail_right = pygame.transform.scale(self.tail_right, (20, 20))
        self.tail_left = pygame.transform.scale(self.tail_left, (20, 20))

        self.body_vertical = pygame.transform.scale(self.body_vertical, (20, 20))
        self.body_horizontal = pygame.transform.scale(self.body_horizontal, (20, 20))

        self.body_tr = pygame.transform.scale(self.body_tr, (20, 20))
        self.body_tl = pygame.transform.scale(self.body_tl, (20, 20))
        self.body_br = pygame.transform.scale(self.body_br, (20, 20))
        self.body_bl = pygame.transform.scale(self.body_bl, (20, 20))

    def change_direction(self, new_direction):
        if isinstance(new_direction, tuple) and len(new_direction) == 2:
            if self.direction[0] + new_direction[0] != 0 or self.direction[1] + new_direction[1] != 0:
                self.direction = new_direction
                self.is_moving = False
            
    def move(self):
        head = self.body[-1]
        # print(head)
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        self.body.append(new_head)
        return new_head

    def collides_with_wall(self, width, height):
        head = self.body[-1]
        x, y = head[0], head[1]
        return x < 0 or x >= width or y < 0 or y >= height

    def collides_with_self(self):
        head = self.body[-1]
        return head in self.body[:-1]

    def draw_snake(self, screen):
        for index, segment in enumerate(self.body):
            x, y = segment
            rect = pygame.Rect(x * 20, y * 20, 20, 20)

            if index == 0:
                self.update_tail_graphics()
                screen.blit(self.tail, rect)                
            elif index == len(self.body) - 1:
                self.update_head_graphics()
                screen.blit(self.head, rect)
            else:
                previous_block = (self.body[index + 1][0] -x, self.body[index + 1][1] - y)
                next_block = (self.body[index - 1][0] -x, self.body[index - 1][1] - y)

                if previous_block[0] == next_block[0]:
                    screen.blit(self.body_vertical, rect)
                elif previous_block[1] == next_block[1]:
                    screen.blit(self.body_horizontal, rect)
                else:
                    if previous_block[0] == -1 and next_block[1] == -1 or previous_block[1] == -1 and next_block[0] == -1:
                        screen.blit(self.body_tl,rect)
                    elif previous_block[0] == -1 and next_block[1] == 1 or previous_block[1] == 1 and next_block[0] == -1:
                        screen.blit(self.body_bl,rect)
                    elif previous_block[0] == 1 and next_block[1] == -1 or previous_block[1] == -1 and next_block[0] == 1:
                        screen.blit(self.body_tr,rect)
                    elif previous_block[0] == 1 and next_block[1] == 1 or previous_block[1] == 1 and next_block[0] == 1:
                        screen.blit(self.body_br,rect)
                    
    def update_head_graphics(self):
        head_relation = (self.body[-2][0] - self.body[-1][0], self.body[-2][1] - self.body[-1][1])
        if head_relation == (1, 0):
            self.head = self.head_left
        elif head_relation == (-1, 0):
            self.head = self.head_right
        elif head_relation == (0, 1):
            self.head = self.head_up
        elif head_relation == (0, -1):
            self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = (self.body[1][0] - self.body[0][0], self.body[1][1] - self.body[0][1])
        if tail_relation == (1, 0):
            self.tail = self.tail_left
        elif tail_relation == (-1, 0):
            self.tail = self.tail_right
        elif tail_relation == (0, 1):
            self.tail = self.tail_up
        elif tail_relation == (0, -1):
            self.tail = self.tail_down

    def play_crunch_sound(self):
        self.crunch_sound.play()
        self.crunch_sound.set_volume(0.3)
        
    def set_moving(self, flag):
        self.is_moving = flag