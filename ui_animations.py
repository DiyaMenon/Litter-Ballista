import pygame
import math

class UIAnimations:
    def __init__(self):
        self.menu_offset = 0
        self.button_scales = {}
        self.fade_alpha = 0
        self.transition_active = False
        self.transition_timer = 0
        self.transition_type = 'fade'
        
    def update(self):
        """Update all UI animations"""
        self.menu_offset += 0.02
        
        # Update transition
        if self.transition_active:
            self.transition_timer += 1
            if self.transition_timer >= 60:  # 1 second transition
                self.transition_active = False
                self.transition_timer = 0
    
    def start_transition(self, transition_type='fade'):
        """Start a transition effect"""
        self.transition_active = True
        self.transition_timer = 0
        self.transition_type = transition_type
    
    def get_button_scale(self, button_id, is_hovered):
        """Get animated scale for button"""
        if button_id not in self.button_scales:
            self.button_scales[button_id] = 1.0
        
        target_scale = 1.1 if is_hovered else 1.0
        current_scale = self.button_scales[button_id]
        
        # Smooth interpolation
        self.button_scales[button_id] = current_scale + (target_scale - current_scale) * 0.1
        
        return self.button_scales[button_id]
    
    def draw_animated_button(self, screen, rect, color, text, font, mouse_pos, button_id):
        """Draw an animated button"""
        is_hovered = rect.collidepoint(mouse_pos)
        scale = self.get_button_scale(button_id, is_hovered)
        
        # Calculate scaled rect
        scaled_width = int(rect.width * scale)
        scaled_height = int(rect.height * scale)
        scaled_x = rect.centerx - scaled_width // 2
        scaled_y = rect.centery - scaled_height // 2
        scaled_rect = pygame.Rect(scaled_x, scaled_y, scaled_width, scaled_height)
        
        # Draw button with glow effect if hovered
        if is_hovered:
            glow_rect = pygame.Rect(scaled_x - 5, scaled_y - 5, scaled_width + 10, scaled_height + 10)
            pygame.draw.rect(screen, (255, 255, 255, 100), glow_rect)
        
        pygame.draw.rect(screen, color, scaled_rect)
        pygame.draw.rect(screen, (255, 255, 255), scaled_rect, 3)
        
        # Draw text
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=scaled_rect.center)
        screen.blit(text_surface, text_rect)
        
        return scaled_rect
    
    def draw_floating_elements(self, screen, elements):
        """Draw floating UI elements"""
        for element in elements:
            x, y, text, font, color = element
            float_y = y + math.sin(self.menu_offset + x * 0.01) * 3
            text_surface = font.render(text, True, color)
            screen.blit(text_surface, (x, float_y))
    
    def draw_transition(self, screen):
        """Draw transition effect"""
        if not self.transition_active:
            return
        
        if self.transition_type == 'fade':
            alpha = int(255 * (self.transition_timer / 60))
            overlay = pygame.Surface((900, 800))
            overlay.set_alpha(alpha)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
        
        elif self.transition_type == 'slide':
            offset = int(900 * (self.transition_timer / 60))
            overlay = pygame.Surface((900, 800))
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (offset, 0))
    
    def draw_particle_background(self, screen):
        """Draw animated particle background"""
        for i in range(20):
            x = (i * 45 + self.menu_offset * 30) % 950
            y = (i * 37 + self.menu_offset * 20) % 850
            size = 2 + math.sin(self.menu_offset + i) * 1
            alpha = int(100 + math.sin(self.menu_offset * 2 + i) * 50)
            
            # Create surface with alpha
            particle_surface = pygame.Surface((size * 2, size * 2))
            particle_surface.set_alpha(alpha)
            particle_surface.fill((255, 255, 255))
            screen.blit(particle_surface, (x, y))