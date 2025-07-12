import pygame
import random
import time

class ScoreMultiplierPowerUp:
    def __init__(self, screen_width, screen_height):
        self.image = pygame.transform.scale(
            pygame.image.load('assets/powerups/score_multiplier.png'), (50, 50)
        )
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x = random.randint(50, screen_width - 100)
        self.y = random.randint(100, screen_height - 300)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        
        # Movement velocity
        self.vx = random.choice([-2, 2])  # move left or right
        self.vy = random.choice([-1, 1])  # move up or down
        
        self.active = False
        self.start_time = 0
        self.duration = 10  # seconds
        self.visible = False
        self.spawn_timer = 0

    def spawn(self):
        self.x = random.randint(50, self.screen_width - 100)
        self.y = random.randint(100, self.screen_height - 300)
        self.rect.topleft = (self.x, self.y)
        self.vx = random.choice([-2, 2])
        self.vy = random.choice([-1, 1])
        self.visible = True

    def draw(self, screen):
        if self.visible and not self.active:
            screen.blit(self.image, self.rect)

    def check_collision(self, mouse_pos):
        if self.visible and self.rect.collidepoint(mouse_pos):
            self.activate()

    def activate(self):
        self.active = True
        self.start_time = time.time()
        self.visible = False

    def update(self):
        # Handle active state duration
        if self.active and time.time() - self.start_time > self.duration:
            self.active = False

        # Move the star if it's visible and not active
        if self.visible and not self.active:
            self.x += self.vx
            self.y += self.vy

            # Bounce off walls
            if self.x <= 0 or self.x + 50 >= self.screen_width:
                self.vx *= -1
            if self.y <= 0 or self.y + 50 >= self.screen_height - 200:  # avoid bottom banner
                self.vy *= -1

            # Update rect position
            self.rect.topleft = (self.x, self.y)
