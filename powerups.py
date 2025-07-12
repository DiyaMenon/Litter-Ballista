import pygame
import random
import math

class PowerUp:
    def __init__(self, x, y, power_type):
        self.x = x
        self.y = y
        self.power_type = power_type
        self.width = 40
        self.height = 40
        self.collected = False
        self.float_offset = 0
        self.float_speed = 0.1
        
        # Power-up colors and symbols
        self.colors = {
            'rapid_fire': (255, 100, 100),
            'multi_shot': (100, 255, 100),
            'time_freeze': (100, 100, 255),
            'score_multiplier': (255, 255, 100)
        }
        
        self.symbols = {
            'rapid_fire': 'RF',
            'multi_shot': 'MS',
            'time_freeze': 'TF',
            'score_multiplier': 'x2'
        }
    
    def update(self):
        # Floating animation
        self.float_offset += self.float_speed
        self.y += math.sin(self.float_offset) * 0.5
        
        # Move left with the level
        self.x -= 2
        
        # Remove if off screen
        if self.x < -50:
            self.collected = True
    
    def draw(self, screen, font):
        if not self.collected:
            # Draw glowing effect
            pygame.draw.circle(screen, self.colors[self.power_type], 
                             (int(self.x + self.width//2), int(self.y + self.height//2)), 
                             self.width//2 + 5)
            pygame.draw.circle(screen, (255, 255, 255), 
                             (int(self.x + self.width//2), int(self.y + self.height//2)), 
                             self.width//2)
            
            # Draw symbol
            text = font.render(self.symbols[self.power_type], True, (0, 0, 0))
            text_rect = text.get_rect(center=(self.x + self.width//2, self.y + self.height//2))
            screen.blit(text, text_rect)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class PowerUpManager:
    def __init__(self):
        self.power_ups = []
        self.active_effects = {}
        self.spawn_timer = 0
        self.spawn_delay = 600  # frames between spawns
        
    def update(self):
        # Update existing power-ups
        for power_up in self.power_ups[:]:
            power_up.update()
            if power_up.collected:
                self.power_ups.remove(power_up)
        
        # Spawn new power-ups
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_delay:
            self.spawn_power_up()
            self.spawn_timer = 0
        
        # Update active effects timers
        for effect in list(self.active_effects.keys()):
            self.active_effects[effect] -= 1
            if self.active_effects[effect] <= 0:
                del self.active_effects[effect]
    
    def spawn_power_up(self):
        if len(self.power_ups) < 2:  # Limit active power-ups
            power_types = ['rapid_fire', 'multi_shot', 'time_freeze', 'score_multiplier']
            power_type = random.choice(power_types)
            x = 900  # Start from right edge
            y = random.randint(50, 400)
            self.power_ups.append(PowerUp(x, y, power_type))
    
    def check_collection(self, mouse_pos, clicked):
        for power_up in self.power_ups[:]:
            if power_up.get_rect().collidepoint(mouse_pos) and clicked:
                self.activate_power_up(power_up.power_type)
                power_up.collected = True
                return True
        return False
    
    def activate_power_up(self, power_type):
        duration = 300  # 5 seconds at 60 FPS
        if power_type == 'time_freeze':
            duration = 180  # 3 seconds for time freeze
        
        self.active_effects[power_type] = duration
    
    def draw(self, screen, font):
        for power_up in self.power_ups:
            power_up.draw(screen, font)
    
    def draw_active_effects(self, screen, font):
        y_offset = 10
        for effect, time_left in self.active_effects.items():
            seconds_left = time_left // 60 + 1
            text = font.render(f"{effect.replace('_', ' ').title()}: {seconds_left}s", True, (255, 255, 255))
            screen.blit(text, (10, y_offset))
            y_offset += 25
    
    def is_active(self, effect_type):
        return effect_type in self.active_effects
    
    def get_score_multiplier(self):
        return 2 if self.is_active('score_multiplier') else 1