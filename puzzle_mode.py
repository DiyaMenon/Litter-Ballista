import pygame
import random
import math

class PuzzleLevel:
    def __init__(self, level_id, name, description, pattern, shots_allowed, target_types):
        self.level_id = level_id
        self.name = name
        self.description = description
        self.pattern = pattern  # List of (x, y, target_type) tuples
        self.shots_allowed = shots_allowed
        self.target_types = target_types
        self.completed = False
        self.stars = 0  # 1-3 stars based on performance

class PuzzleMode:
    def __init__(self):
        self.active = False
        self.current_level = 0
        self.levels = []
        self.shots_used = 0
        self.targets_remaining = []
        self.level_complete = False
        self.mode_complete = False
        self.stars_earned = 0
        
        self.setup_levels()
    
    def setup_levels(self):
        """Create puzzle levels with specific patterns"""
        
        # Level 1: Simple Line
        pattern1 = [(300, 200), (400, 200), (500, 200), (600, 200)]
        self.levels.append(PuzzleLevel(
            1, "Straight Shot", "Hit all targets in a line", 
            pattern1, 4, [1, 1, 1, 1]
        ))
        
        # Level 2: Circle Pattern
        pattern2 = []
        center_x, center_y = 450, 300
        radius = 100
        for i in range(8):
            angle = (i / 8) * 2 * math.pi
            x = center_x + math.cos(angle) * radius
            y = center_y + math.sin(angle) * radius
            pattern2.append((x, y))
        self.levels.append(PuzzleLevel(
            2, "Circle of Targets", "Clear the circular formation",
            pattern2, 8, [1] * 8
        ))
        
        # Level 3: Diamond Formation
        pattern3 = [
            (450, 150),  # Top
            (350, 250), (550, 250),  # Middle sides
            (300, 350), (450, 350), (600, 350),  # Bottom row
            (450, 450)  # Bottom point
        ]
        self.levels.append(PuzzleLevel(
            3, "Diamond Formation", "Hit targets in diamond shape",
            pattern3, 6, [2, 1, 1, 2, 1, 2, 1]
        ))
        
        # Level 4: Moving Targets
        pattern4 = [(200, 200), (400, 300), (600, 200), (800, 300)]
        self.levels.append(PuzzleLevel(
            4, "Moving Targets", "Hit moving targets efficiently",
            pattern4, 5, [3, 2, 3, 2]
        ))
        
        # Level 5: Precision Challenge
        pattern5 = []
        for i in range(3):
            for j in range(3):
                x = 350 + j * 50
                y = 200 + i * 50
                pattern5.append((x, y))
        self.levels.append(PuzzleLevel(
            5, "Precision Grid", "Clear the tight formation",
            pattern5, 7, [1, 2, 1, 2, 3, 2, 1, 2, 1]
        ))
    
    def start_puzzle_mode(self):
        """Start puzzle mode"""
        self.active = True
        self.current_level = 0
        self.mode_complete = False
        self.start_level()
    
    def start_level(self):
        """Start current puzzle level"""
        if self.current_level >= len(self.levels):
            self.mode_complete = True
            return
        
        level = self.levels[self.current_level]
        self.shots_used = 0
        self.level_complete = False
        self.stars_earned = 0
        
        # Create target rectangles from pattern
        self.targets_remaining = []
        for i, (x, y) in enumerate(level.pattern):
            target_type = level.target_types[i] if i < len(level.target_types) else 1
            size = 60 - (target_type - 1) * 12
            target_rect = pygame.Rect(x - size//2, y - size//2, size, size)
            self.targets_remaining.append({
                'rect': target_rect,
                'type': target_type,
                'x': x,
                'y': y,
                'original_x': x,
                'original_y': y
            })
    
    def update(self):
        """Update puzzle mode"""
        if not self.active or self.mode_complete:
            return
        
        # Update moving targets for level 4
        if self.current_level == 3:  # Level 4 (0-indexed)
            for target in self.targets_remaining:
                # Simple back and forth movement
                target['x'] += math.sin(pygame.time.get_ticks() * 0.005) * 2
                target['rect'].centerx = target['x']
        
        # Check if level is complete
        if not self.targets_remaining and not self.level_complete:
            self.complete_level()
    
    def handle_shot(self, mouse_pos):
        """Handle shot in puzzle mode"""
        if not self.active or self.level_complete or self.mode_complete:
            return False
        
        level = self.levels[self.current_level]
        
        # Check if out of shots
        if self.shots_used >= level.shots_allowed:
            return False
        
        # Check for hits
        hit = False
        for target in self.targets_remaining[:]:
            if target['rect'].collidepoint(mouse_pos):
                self.targets_remaining.remove(target)
                hit = True
                break
        
        if hit:
            self.shots_used += 1
            return True
        
        # Miss - still count the shot
        self.shots_used += 1
        
        # Check if out of shots and targets remain
        if self.shots_used >= level.shots_allowed and self.targets_remaining:
            self.fail_level()
        
        return False
    
    def complete_level(self):
        """Complete current level and calculate stars"""
        self.level_complete = True
        level = self.levels[self.current_level]
        
        # Calculate stars based on shots used
        shots_ratio = self.shots_used / level.shots_allowed
        if shots_ratio <= 0.6:
            self.stars_earned = 3
        elif shots_ratio <= 0.8:
            self.stars_earned = 2
        else:
            self.stars_earned = 1
        
        level.completed = True
        level.stars = max(level.stars, self.stars_earned)
    
    def fail_level(self):
        """Fail current level"""
        self.level_complete = True
        self.stars_earned = 0
    
    def next_level(self):
        """Move to next level"""
        self.current_level += 1
        if self.current_level >= len(self.levels):
            self.mode_complete = True
        else:
            self.start_level()
    
    def restart_level(self):
        """Restart current level"""
        self.start_level()
    
    def draw(self, screen, font, big_font, target_images):
        """Draw puzzle mode"""
        if not self.active:
            return
        
        # Draw background
        screen.fill((20, 20, 40))
        
        # Draw level info
        level = self.levels[self.current_level]
        title_text = big_font.render(f"Puzzle {level.level_id}: {level.name}", True, (255, 255, 255))
        screen.blit(title_text, (50, 50))
        
        desc_text = font.render(level.description, True, (255, 255, 255))
        screen.blit(desc_text, (50, 100))
        
        shots_text = font.render(f"Shots: {self.shots_used}/{level.shots_allowed}", True, (255, 255, 255))
        screen.blit(shots_text, (50, 130))
        
        # Draw targets
        for target in self.targets_remaining:
            target_type = target['type'] - 1
            if target_type < len(target_images) and target_images[target_type]:
                image_index = min(target['type'] - 1, len(target_images[target_type]) - 1)
                if image_index < len(target_images[target_type]):
                    screen.blit(target_images[target_type][image_index], 
                              (target['rect'].x, target['rect'].y))
        
        # Draw level complete overlay
        if self.level_complete:
            self.draw_level_complete_overlay(screen, font, big_font)
        
        # Draw mode complete overlay
        if self.mode_complete:
            self.draw_mode_complete_overlay(screen, font, big_font)
    
    def draw_level_complete_overlay(self, screen, font, big_font):
        """Draw level completion overlay"""
        # Semi-transparent overlay
        overlay = pygame.Surface((900, 800))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Result box
        box = pygame.Rect(250, 250, 400, 300)
        pygame.draw.rect(screen, (50, 100, 50) if self.stars_earned > 0 else (100, 50, 50), box)
        pygame.draw.rect(screen, (255, 255, 255), box, 3)
        
        # Title
        if self.stars_earned > 0:
            title_text = big_font.render("LEVEL COMPLETE!", True, (255, 255, 255))
        else:
            title_text = big_font.render("LEVEL FAILED!", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(450, 300))
        screen.blit(title_text, title_rect)
        
        # Stars
        if self.stars_earned > 0:
            stars_text = font.render("★" * self.stars_earned + "☆" * (3 - self.stars_earned), True, (255, 255, 0))
            stars_rect = stars_text.get_rect(center=(450, 350))
            screen.blit(stars_text, stars_rect)
        
        # Shots info
        level = self.levels[self.current_level]
        shots_text = font.render(f"Shots used: {self.shots_used}/{level.shots_allowed}", True, (255, 255, 255))
        shots_rect = shots_text.get_rect(center=(450, 400))
        screen.blit(shots_text, shots_rect)
        
        # Buttons
        if self.stars_earned > 0:
            next_text = font.render("Click to continue", True, (255, 255, 255))
        else:
            next_text = font.render("Click to retry", True, (255, 255, 255))
        next_rect = next_text.get_rect(center=(450, 450))
        screen.blit(next_text, next_rect)
        
        menu_text = font.render("ESC for menu", True, (200, 200, 200))
        menu_rect = menu_text.get_rect(center=(450, 480))
        screen.blit(menu_text, menu_rect)
    
    def draw_mode_complete_overlay(self, screen, font, big_font):
        """Draw mode completion overlay"""
        # Semi-transparent overlay
        overlay = pygame.Surface((900, 800))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Result box
        box = pygame.Rect(200, 200, 500, 400)
        pygame.draw.rect(screen, (100, 50, 150), box)
        pygame.draw.rect(screen, (255, 255, 255), box, 3)
        
        # Title
        title_text = big_font.render("PUZZLE MODE", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(450, 250))
        screen.blit(title_text, title_rect)
        
        complete_text = big_font.render("COMPLETE!", True, (255, 255, 255))
        complete_rect = complete_text.get_rect(center=(450, 300))
        screen.blit(complete_text, complete_rect)
        
        # Total stars
        total_stars = sum(level.stars for level in self.levels)
        max_stars = len(self.levels) * 3
        stars_text = font.render(f"Total Stars: {total_stars}/{max_stars}", True, (255, 255, 0))
        stars_rect = stars_text.get_rect(center=(450, 350))
        screen.blit(stars_text, stars_rect)
        
        # Level breakdown
        y_offset = 400
        for i, level in enumerate(self.levels):
            level_text = font.render(f"Level {i+1}: {'★' * level.stars}{'☆' * (3 - level.stars)}", True, (255, 255, 255))
            level_rect = level_text.get_rect(center=(450, y_offset))
            screen.blit(level_text, level_rect)
            y_offset += 30
        
        # Return to menu
        menu_text = font.render("Click anywhere to return to menu", True, (200, 200, 200))
        menu_rect = menu_text.get_rect(center=(450, 550))
        screen.blit(menu_text, menu_rect)
    
    def handle_level_complete_click(self):
        """Handle click on level complete screen"""
        if self.level_complete:
            if self.stars_earned > 0:
                self.next_level()
            else:
                self.restart_level()
            return True
        return False
    
    def handle_mode_complete_click(self):
        """Handle click on mode complete screen"""
        if self.mode_complete:
            self.active = False
            return True
        return False