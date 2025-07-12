import pygame
import random
import math

class Particle:
    def __init__(self, x, y, color, velocity, lifetime, particle_type='normal'):
        self.x = x
        self.y = y
        self.color = color
        self.velocity = velocity  # (vx, vy)
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.particle_type = particle_type
        self.size = random.randint(2, 6)
        self.gravity = 0.1
        self.fade = True
        
    def update(self):
        # Update position
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        
        # Apply gravity for certain particle types
        if self.particle_type in ['debris', 'sparks']:
            self.velocity = (self.velocity[0] * 0.98, self.velocity[1] + self.gravity)
        
        # Update lifetime
        self.lifetime -= 1
        
        # Shrink over time
        if self.lifetime < self.max_lifetime * 0.3:
            self.size = max(1, self.size - 0.1)
    
    def draw(self, screen):
        if self.lifetime <= 0:
            return
        
        # Calculate alpha based on lifetime
        alpha = int(255 * (self.lifetime / self.max_lifetime)) if self.fade else 255
        alpha = max(0, min(255, alpha))
        
        # Create surface with alpha
        if alpha > 0:
            if self.particle_type == 'sparkle':
                # Draw sparkle effect
                points = []
                for i in range(4):
                    angle = i * math.pi / 2
                    px = self.x + math.cos(angle) * self.size
                    py = self.y + math.sin(angle) * self.size
                    points.append((px, py))
                
                if len(points) >= 3:
                    pygame.draw.polygon(screen, (*self.color, alpha), points)
            else:
                # Draw regular circle
                pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))
    
    def is_alive(self):
        return self.lifetime > 0 and self.size > 0

class ParticleSystem:
    def __init__(self):
        self.particles = []
        self.max_particles = 500
    
    def add_hit_effect(self, x, y, target_type):
        """Add particles for target hit"""
        colors = {
            1: [(255, 100, 100), (255, 150, 150), (255, 200, 200)],  # Red tones
            2: [(100, 255, 100), (150, 255, 150), (200, 255, 200)],  # Green tones
            3: [(100, 100, 255), (150, 150, 255), (200, 200, 255)]   # Blue tones
        }
        
        target_colors = colors.get(target_type, [(255, 255, 255)])
        
        # Explosion particles
        for _ in range(15):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 8)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            color = random.choice(target_colors)
            lifetime = random.randint(30, 60)
            
            particle = Particle(x, y, color, (vx, vy), lifetime, 'debris')
            self.particles.append(particle)
        
        # Sparkle effect
        for _ in range(8):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 4)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            color = (255, 255, 100)
            lifetime = random.randint(20, 40)
            
            particle = Particle(x, y, color, (vx, vy), lifetime, 'sparkle')
            self.particles.append(particle)
    
    def add_power_up_effect(self, x, y, power_type):
        """Add particles for power-up collection"""
        colors = {
            'rapid_fire': (255, 100, 100),
            'multi_shot': (100, 255, 100),
            'time_freeze': (100, 100, 255),
            'score_multiplier': (255, 255, 100)
        }
        
        color = colors.get(power_type, (255, 255, 255))
        
        # Ring explosion
        for i in range(20):
            angle = (i / 20) * 2 * math.pi
            speed = random.uniform(3, 6)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            lifetime = random.randint(40, 80)
            
            particle = Particle(x, y, color, (vx, vy), lifetime, 'sparkle')
            self.particles.append(particle)
    
    def add_muzzle_flash(self, x, y, angle):
        """Add muzzle flash effect when shooting"""
        for _ in range(5):
            # Calculate direction based on gun angle
            spread = random.uniform(-0.3, 0.3)
            flash_angle = angle + spread
            speed = random.uniform(3, 8)
            vx = math.cos(flash_angle) * speed
            vy = math.sin(flash_angle) * speed
            
            color = random.choice([(255, 255, 100), (255, 200, 100), (255, 150, 100)])
            lifetime = random.randint(10, 20)
            
            particle = Particle(x, y, color, (vx, vy), lifetime, 'sparks')
            self.particles.append(particle)
    
    def add_level_complete_effect(self, screen_width, screen_height):
        """Add celebration particles for level completion"""
        colors = [(255, 100, 100), (100, 255, 100), (100, 100, 255), 
                 (255, 255, 100), (255, 100, 255), (100, 255, 255)]
        
        # Fireworks effect
        for _ in range(50):
            x = random.randint(100, screen_width - 100)
            y = random.randint(100, screen_height - 300)
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 10)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            color = random.choice(colors)
            lifetime = random.randint(60, 120)
            
            particle = Particle(x, y, color, (vx, vy), lifetime, 'sparkle')
            self.particles.append(particle)
    
    def add_trail_effect(self, x, y, color):
        """Add trail effect for special shots"""
        for _ in range(3):
            offset_x = random.uniform(-5, 5)
            offset_y = random.uniform(-5, 5)
            vx = random.uniform(-1, 1)
            vy = random.uniform(-1, 1)
            lifetime = random.randint(15, 30)
            
            particle = Particle(x + offset_x, y + offset_y, color, (vx, vy), lifetime, 'trail')
            self.particles.append(particle)
    
    def update(self):
        """Update all particles"""
        # Update existing particles
        for particle in self.particles[:]:
            particle.update()
            if not particle.is_alive():
                self.particles.remove(particle)
        
        # Limit particle count for performance
        if len(self.particles) > self.max_particles:
            self.particles = self.particles[-self.max_particles:]
    
    def draw(self, screen):
        """Draw all particles"""
        for particle in self.particles:
            particle.draw(screen)
    
    def clear(self):
        """Clear all particles"""
        self.particles.clear()

class ScreenShake:
    def __init__(self):
        self.shake_intensity = 0
        self.shake_duration = 0
        self.shake_offset = (0, 0)
    
    def add_shake(self, intensity, duration):
        """Add screen shake effect"""
        self.shake_intensity = max(self.shake_intensity, intensity)
        self.shake_duration = max(self.shake_duration, duration)
    
    def update(self):
        """Update screen shake"""
        if self.shake_duration > 0:
            self.shake_duration -= 1
            
            # Calculate shake offset
            shake_x = random.randint(-self.shake_intensity, self.shake_intensity)
            shake_y = random.randint(-self.shake_intensity, self.shake_intensity)
            self.shake_offset = (shake_x, shake_y)
            
            # Reduce intensity over time
            self.shake_intensity = max(0, self.shake_intensity - 0.5)
        else:
            self.shake_offset = (0, 0)
            self.shake_intensity = 0
    
    def get_offset(self):
        """Get current shake offset"""
        return self.shake_offset