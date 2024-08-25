import pygame


class Bird:
    GRAVITY = 0.125
    RADIUS = 20
    JUMP_VELOCITY = -5
  
    def __init__(self, window, x, y):
        self.window = window
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.dy = 0
        self.image = pygame.image.load("flappy\\bird.png")
        self.image = pygame.transform.scale(self.image, (self.RADIUS * 3, self.RADIUS * 2))
        self.game_over = False
        self.score = 0
    
    def draw(self):
        rotated_image = pygame.transform.rotate(self.image, -7.5*self.dy + 22.5)
        new_rect = rotated_image.get_rect(center = (self.x, self.y))
        pygame.Surface.blit(self.window, rotated_image, new_rect)

        # pygame.draw.circle(self.window, (255,255,255), (self.x, self.y), self.RADIUS)
    
    def move(self): 
        self.dy += self.GRAVITY
        if self.y + self.dy > self.window.get_height():
            self.dy = 0
        else:    
            self.y += self.dy
    
    def jump(self):
        self.dy = self.JUMP_VELOCITY
    
    def reset(self):
        self.y = self.original_y
        self.dy = 0