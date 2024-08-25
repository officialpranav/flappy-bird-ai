import pygame
import random

class Pipe:
    GAP = 160
    WIDTH = 80
    PIPE_GAP_RANGE = 300
    DX = -3
    
    def __init__(self, window, x):
        self.window = window
        self.passed = False
        self.x = self.original_x = x
        self.y = random.randint(window.get_height() // 2 - self.PIPE_GAP_RANGE // 2, window.get_height() // 2 + self.PIPE_GAP_RANGE // 2)
        self.bottom_pipe_rect = pygame.Rect(self.x, self.y + self.GAP // 2, self.WIDTH, window.get_height())
        self.top_pipe_rect = pygame.Rect(self.x, 0, self.WIDTH, self.y - self.GAP // 2)
        self.top_pipe_img = pygame.image.load("flappy\\pipe.png")
        self.bottom_pipe_img = pygame.transform.rotate(self.top_pipe_img, 180)
        
    def draw(self):

        self.window.blit(self.bottom_pipe_img, (self.x, self.y + self.GAP // 2))
        self.window.blit(self.top_pipe_img, (self.x, -750 + self.y - self.GAP // 2))
        self.update_pipe_rects()
        
        # pygame.draw.rect(self.window, (0, 255, 0), self.bottom_pipe_rect)
        # pygame.draw.rect(self.window, (0, 255, 0), self.top_pipe_rect)
    
    def update_pipe_rects(self):
        self.bottom_pipe_rect = pygame.Rect(self.x, self.y + self.GAP // 2, self.WIDTH, self.window.get_height())
        self.top_pipe_rect = pygame.Rect(self.x, 0, self.WIDTH, self.y - self.GAP // 2)
    
    def change_y(self):
        self.y = random.randint(self.window.get_height() // 2 - self.PIPE_GAP_RANGE // 2, self.window.get_height() // 2 + self.PIPE_GAP_RANGE // 2)
        self.update_pipe_rects()

    def move(self):
        self.x += self.DX
        self.update_pipe_rects()
        
    def reset(self):
        self.passed = False
        self.change_y()
        self.x = self.window.get_width() + self.GAP // 2
        self.update_pipe_rects()