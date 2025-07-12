import pygame
import random
import math

class WeatherEffect:
    def __init__(self):
        self.current_weather = 'clear'
        self.weather_timer = 0
        self.weather_duration = 900  # 15 seconds
        self.particles = []
        self.fog_alpha = 0
        self.wind_offset = 0
        
        self.weather_types = ['clear', 'rain', 'fog', 'wind']
        
    def update(self):
        self.weather_timer += 1
        
        # Change weather periodically
        if self.weather_timer >= self.weather_duration:
            self.change_weather()
            self.weather_timer = 0
        
        # Update weather effects
        if self.current_weather == 'rain':
            self.update_rain()
        elif self.current_weather == 'fog':
            self.update_fog()
        elif self.current_weather == 'wind':
            self.update_wind()
    
    def change_weather(self):
        # 40% chance to stay clear, 60% chance for weather
        if random.random() < 0.4:
            self.current_weather = 'clear'
        else:
            self.current_weather = random.choice(['rain', 'fog', 'wind'])
        
        # Reset effects
        self.particles = []
        self.fog_alpha = 0
        self.wind_offset = 0
    
    def update_rain(self):
        # Add new raindrops
        for _ in range(3):
            self.particles.append({
                'x': random.randint(-50, 950),
                'y': -10,
                'speed': random.randint(8, 12),
                'length': random.randint(10, 20)
            })
        
        # Update existing raindrops
        for particle in self.particles[:]:
            particle['y'] += particle['speed']
            particle['x'] += 2  # Slight angle
            
            if particle['y'] > 800:
                self.particles.remove(particle)
        
        # Limit particles
        if len(self.particles) > 100:
            self.particles = self.particles[-100:]
    
    def update_fog(self):
        # Gradually increase fog
        if self.fog_alpha < 100:
            self.fog_alpha += 1
    
    def update_wind(self):
        # Wind sway effect
        self.wind_offset += 0.1
    
    def draw(self, screen):
        if self.current_weather == 'rain':
            self.draw_rain(screen)
        elif self.current_weather == 'fog':
            self.draw_fog(screen)
        elif self.current_weather == 'wind':
            self.draw_wind(screen)
    
    def draw_rain(self, screen):
        for particle in self.particles:
            start_pos = (particle['x'], particle['y'])
            end_pos = (particle['x'] - 3, particle['y'] + particle['length'])
            pygame.draw.line(screen, (150, 150, 255), start_pos, end_pos, 2)
    
    def draw_fog(self, screen):
        if self.fog_alpha > 0:
            fog_surface = pygame.Surface((900, 800))
            fog_surface.set_alpha(self.fog_alpha)
            fog_surface.fill((200, 200, 200))
            screen.blit(fog_surface, (0, 0))
    
    def draw_wind(self, screen):
        # Draw wind lines
        for i in range(20):
            x = (i * 45 + self.wind_offset * 50) % 950
            y = random.randint(50, 600)
            end_x = x + 30 + math.sin(self.wind_offset + i) * 10
            pygame.draw.line(screen, (255, 255, 255, 100), (x, y), (end_x, y), 1)
    
    def draw_weather_indicator(self, screen, font):
        weather_text = font.render(f"Weather: {self.current_weather.title()}", True, (255, 255, 255))
        screen.blit(weather_text, (10, 50))
        
        # Weather effects description
        effects = {
            'clear': "Perfect shooting conditions!",
            'rain': "Reduced visibility, harder aiming!",
            'fog': "Heavy fog obscures targets!",
            'wind': "Wind affects projectile path!"
        }
        
        effect_text = font.render(effects[self.current_weather], True, (255, 255, 255))
        screen.blit(effect_text, (10, 75))
    
    def get_accuracy_modifier(self):
        """Returns accuracy modifier based on weather"""
        modifiers = {
            'clear': 1.0,
            'rain': 0.85,
            'fog': 0.7,
            'wind': 0.8
        }
        return modifiers[self.current_weather]
    
    def get_visibility_modifier(self):
        """Returns visibility modifier for target detection"""
        modifiers = {
            'clear': 1.0,
            'rain': 0.9,
            'fog': 0.6,
            'wind': 1.0
        }
        return modifiers[self.current_weather]
    
    def apply_wind_effect(self, mouse_pos):
        """Apply wind effect to mouse position"""
        if self.current_weather == 'wind':
            wind_strength = math.sin(self.wind_offset) * 15
            return (mouse_pos[0] + wind_strength, mouse_pos[1])
        return mouse_pos