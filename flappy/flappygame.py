import pygame
from .bird import Bird
from .pipe import Pipe
pygame.init()

class FlappyGame:
    SCORE_FONT = pygame.font.SysFont("yeet", 50)
    
    def __init__(self, window, window_height, window_width, birds):
        print(window_height, window_width)
        self.window_width = window_width
        self.window_height = window_height
        self.birds = birds
        self.pipe1 = Pipe(window, 600)
        self.pipe2 = Pipe(window, 975)
        self.bg = pygame.transform.scale(pygame.image.load("flappy\\flappyBG.png"), (600, 760))
        self.window = window
        self.score = 0
        self.game_over = False
    
    def intersects(self, rect, r, center):
        circle_distance_x = abs(center[0]-rect.centerx)
        circle_distance_y = abs(center[1]-rect.centery)
        if circle_distance_x > rect.w/2.0+r or circle_distance_y > rect.h/2.0+r:
            return False
        if circle_distance_x <= rect.w/2.0 or circle_distance_y <= rect.h/2.0:
            return True
        corner_x = circle_distance_x-rect.w/2.0
        corner_y = circle_distance_y-rect.h/2.0
        corner_distance_sq = corner_x**2.0 +corner_y**2.0
        return corner_distance_sq <= r**2.0

    def collide(self, bird):
        colliding_with_pipe = (self.intersects(self.pipe1.top_pipe_rect, bird.RADIUS, [bird.x, bird.y]) 
                                + self.intersects(self.pipe1.bottom_pipe_rect, bird.RADIUS, [bird.x, bird.y])
                                + self.intersects(self.pipe2.top_pipe_rect, bird.RADIUS, [bird.x, bird.y]) 
                                + self.intersects(self.pipe2.bottom_pipe_rect, bird.RADIUS, [bird.x, bird.y]))
        if colliding_with_pipe or bird.y < 0 or bird.y >= (self.window_height - bird.RADIUS*2):
            return True
        return False
    
    def draw(self):
        #set background
        self.window.blit(self.bg, (0,0))
        score_text = self.SCORE_FONT.render(f"{self.score}", 1, (0,0,0))
        self.window.blit(score_text, (300 - score_text.get_width()//2, 20))
        self.pipe1.draw()
        self.pipe2.draw()
        for i, bird in enumerate(self.birds):
            bird.draw()

    def loop(self):
        birds_alive = False     
        for i, bird in enumerate(self.birds):
            if bird.game_over:
                bird.move()
            elif self.collide(bird):
                bird.game_over = True
                bird.score = self.score
            else: 
                birds_alive = True
                bird.move()

        if not birds_alive:
            self.game_over = True
            return
        
        if self.pipe1.x + self.pipe1.WIDTH < self.birds[0].x and not self.pipe1.passed:
            self.score += 1
            self.pipe1.passed = True
        if self.pipe2.x + self.pipe2.WIDTH < self.birds[0].x and not self.pipe2.passed:
            self.score += 1
            self.pipe2.passed = True
        if self.pipe1.x < 0 - self.pipe1.GAP // 2:
            self.pipe1.reset()
        if self.pipe2.x < 0 - self.pipe2.GAP // 2:
            self.pipe2.reset()
        self.pipe1.move()
        self.pipe2.move()