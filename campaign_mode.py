import pygame
import random

class CampaignLevel:
    def __init__(self, level_id, name, story_text, objective, background_id, special_rules=None):
        self.level_id = level_id
        self.name = name
        self.story_text = story_text
        self.objective = objective
        self.background_id = background_id
        self.special_rules = special_rules or {}
        self.completed = False
        self.score = 0

class CampaignMode:
    def __init__(self):
        self.active = False
        self.current_level = 0
        self.levels = []
        self.story_showing = False
        self.story_timer = 0
        self.level_complete = False
        self.campaign_complete = False
        
        self.setup_campaign()
    
    def setup_campaign(self):
        """Create campaign levels with story and objectives"""
        
        # Level 1: The Polluted Park
        self.levels.append(CampaignLevel(
            1, "The Polluted Park",
            "A once-beautiful park has been littered with trash. Help clean it up by shooting the litter into proper disposal!",
            "Clear all litter in under 2 minutes",
            1,
            {'time_limit': 120, 'accuracy_required': 70}
        ))
        
        # Level 2: Ocean Cleanup
        self.levels.append(CampaignLevel(
            2, "Ocean Cleanup",
            "Plastic waste is threatening marine life! Use your ballista to remove floating debris before it's too late.",
            "Save the ocean - hit 90% of targets",
            2,
            {'accuracy_required': 90, 'moving_targets': True}
        ))
        
        # Level 3: City Streets
        self.levels.append(CampaignLevel(
            3, "City Streets",
            "The city is overwhelmed with litter. Citizens are counting on you to restore cleanliness to the streets!",
            "Clean 150 items with limited ammo",
            1,
            {'target_count': 150, 'ammo_limit': 120}
        ))
        
        # Level 4: Industrial Zone
        self.levels.append(CampaignLevel(
            4, "Industrial Waste",
            "A factory has been illegally dumping waste. Stop the pollution by targeting the waste containers!",
            "Destroy all waste containers",
            3,
            {'boss_targets': True, 'special_targets': 5}
        ))
        
        # Level 5: The Final Cleanup
        self.levels.append(CampaignLevel(
            5, "Global Initiative",
            "You've proven yourself as an eco-warrior! Lead the final global cleanup effort to save our planet!",
            "Ultimate challenge - survive 5 minutes",
            2,
            {'survival_mode': True, 'time_limit': 300, 'increasing_difficulty': True}
        ))
    
    def start_campaign(self):
        """Start campaign mode"""
        self.active = True
        self.current_level = 0
        self.campaign_complete = False
        self.show_story()
    
    def show_story(self):
        """Show story for current level"""
        self.story_showing = True
        self.story_timer = 480  # 8 seconds
    
    def start_level(self):
        """Start current campaign level"""
        if self.current_level >= len(self.levels):
            self.campaign_complete = True
            return
        
        self.level_complete = False
        self.story_showing = False
        
        # Apply special rules for the level
        level = self.levels[self.current_level]
        return level.special_rules
    
    def update(self, game_stats):
        """Update campaign mode with game statistics"""
        if not self.active or self.campaign_complete:
            return
        
        if self.story_showing:
            self.story_timer -= 1
            if self.story_timer <= 0:
                self.story_showing = False
            return
        
        # Check level completion based on objectives
        level = self.levels[self.current_level]
        
        if self.check_level_objective(level, game_stats):
            self.complete_level(game_stats)
    
    def check_level_objective(self, level, game_stats):
        """Check if level objective is met"""
        rules = level.special_rules
        
        # Time limit check
        if 'time_limit' in rules:
            if game_stats.get('time_passed', 0) >= rules['time_limit']:
                return True
        
        # Accuracy requirement
        if 'accuracy_required' in rules:
            total_shots = game_stats.get('total_shots', 1)
            hits = game_stats.get('targets_hit', 0)
            accuracy = (hits / total_shots) * 100 if total_shots > 0 else 0
            if accuracy < rules['accuracy_required'] and total_shots > 10:
                self.fail_level()
                return False
        
        # Target count
        if 'target_count' in rules:
            if game_stats.get('targets_hit', 0) >= rules['target_count']:
                return True
        
        # Ammo limit
        if 'ammo_limit' in rules:
            if game_stats.get('total_shots', 0) >= rules['ammo_limit']:
                return True
        
        # Boss targets
        if 'boss_targets' in rules:
            if game_stats.get('special_targets_destroyed', 0) >= rules.get('special_targets', 5):
                return True
        
        # Survival mode
        if 'survival_mode' in rules:
            if game_stats.get('time_passed', 0) >= rules['time_limit']:
                return True
        
        # Check if all targets are cleared (default win condition)
        if game_stats.get('targets_remaining', 1) == 0:
            return True
        
        return False
    
    def complete_level(self, game_stats):
        """Complete current level"""
        self.level_complete = True
        level = self.levels[self.current_level]
        level.completed = True
        level.score = game_stats.get('points', 0)
    
    def fail_level(self):
        """Fail current level"""
        self.level_complete = True
        # Don't mark as completed, allow retry
    
    def next_level(self):
        """Move to next level"""
        self.current_level += 1
        if self.current_level >= len(self.levels):
            self.campaign_complete = True
        else:
            self.show_story()
    
    def restart_level(self):
        """Restart current level"""
        self.show_story()
    
    def draw_story(self, screen, font, big_font):
        """Draw story overlay"""
        if not self.story_showing:
            return
        
        # Semi-transparent overlay
        overlay = pygame.Surface((900, 800))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 50))
        screen.blit(overlay, (0, 0))
        
        # Story box
        story_box = pygame.Rect(100, 200, 700, 400)
        pygame.draw.rect(screen, (25, 25, 75), story_box)
        pygame.draw.rect(screen, (255, 255, 255), story_box, 3)
        
        level = self.levels[self.current_level]
        
        # Level title
        title_text = big_font.render(f"Level {level.level_id}: {level.name}", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(450, 250))
        screen.blit(title_text, title_rect)
        
        # Story text (word wrap)
        words = level.story_text.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] < 650:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + " "
        if current_line:
            lines.append(current_line.strip())
        
        y_offset = 320
        for line in lines:
            story_text = font.render(line, True, (255, 255, 255))
            story_rect = story_text.get_rect(center=(450, y_offset))
            screen.blit(story_text, story_rect)
            y_offset += 35
        
        # Objective
        objective_title = font.render("OBJECTIVE:", True, (255, 255, 100))
        objective_title_rect = objective_title.get_rect(center=(450, y_offset + 20))
        screen.blit(objective_title, objective_title_rect)
        
        objective_text = font.render(level.objective, True, (255, 255, 255))
        objective_rect = objective_text.get_rect(center=(450, y_offset + 50))
        screen.blit(objective_text, objective_rect)
        
        # Timer or click instruction
        if self.story_timer > 120:
            continue_text = font.render(f"Starting in {(self.story_timer // 60) + 1}...", True, (200, 200, 200))
        else:
            continue_text = font.render("Click anywhere to start!", True, (200, 200, 200))
        continue_rect = continue_text.get_rect(center=(450, 550))
        screen.blit(continue_text, continue_rect)
    
    def draw_level_complete(self, screen, font, big_font):
        """Draw level completion overlay"""
        if not self.level_complete:
            return
        
        # Semi-transparent overlay
        overlay = pygame.Surface((900, 800))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        level = self.levels[self.current_level]
        
        # Result box
        box_color = (50, 100, 50) if level.completed else (100, 50, 50)
        box = pygame.Rect(250, 250, 400, 300)
        pygame.draw.rect(screen, box_color, box)
        pygame.draw.rect(screen, (255, 255, 255), box, 3)
        
        # Title
        if level.completed:
            title_text = big_font.render("MISSION SUCCESS!", True, (255, 255, 255))
        else:
            title_text = big_font.render("MISSION FAILED!", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(450, 300))
        screen.blit(title_text, title_rect)
        
        # Score
        if level.completed:
            score_text = font.render(f"Score: {level.score}", True, (255, 255, 255))
            score_rect = score_text.get_rect(center=(450, 350))
            screen.blit(score_text, score_rect)
        
        # Buttons
        if level.completed:
            if self.current_level < len(self.levels) - 1:
                next_text = font.render("Click for next mission", True, (255, 255, 255))
            else:
                next_text = font.render("Campaign Complete!", True, (255, 255, 100))
        else:
            next_text = font.render("Click to retry mission", True, (255, 255, 255))
        next_rect = next_text.get_rect(center=(450, 400))
        screen.blit(next_text, next_rect)
        
        menu_text = font.render("ESC for menu", True, (200, 200, 200))
        menu_rect = menu_text.get_rect(center=(450, 450))
        screen.blit(menu_text, menu_rect)
    
    def draw_campaign_complete(self, screen, font, big_font):
        """Draw campaign completion overlay"""
        if not self.campaign_complete:
            return
        
        # Semi-transparent overlay
        overlay = pygame.Surface((900, 800))
        overlay.set_alpha(200)
        overlay.fill((0, 50, 0))
        screen.blit(overlay, (0, 0))
        
        # Victory box
        box = pygame.Rect(150, 150, 600, 500)
        pygame.draw.rect(screen, (34, 139, 34), box)
        pygame.draw.rect(screen, (255, 255, 255), box, 4)
        
        # Title
        title_text = big_font.render("CAMPAIGN COMPLETE!", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(450, 220))
        screen.blit(title_text, title_rect)
        
        # Congratulations
        congrats_text = font.render("Congratulations, Eco-Warrior!", True, (255, 255, 255))
        congrats_rect = congrats_text.get_rect(center=(450, 280))
        screen.blit(congrats_text, congrats_rect)
        
        # Total score
        total_score = sum(level.score for level in self.levels)
        score_text = font.render(f"Total Score: {total_score}", True, (255, 255, 100))
        score_rect = score_text.get_rect(center=(450, 320))
        screen.blit(score_text, score_rect)
        
        # Level breakdown
        y_offset = 370
        for level in self.levels:
            status = "✓" if level.completed else "✗"
            level_text = font.render(f"{status} {level.name}: {level.score}", True, (255, 255, 255))
            level_rect = level_text.get_rect(center=(450, y_offset))
            screen.blit(level_text, level_rect)
            y_offset += 30
        
        # Final message
        final_text = font.render("You've saved the planet! Thank you!", True, (255, 255, 255))
        final_rect = final_text.get_rect(center=(450, y_offset + 30))
        screen.blit(final_text, final_rect)
        
        # Return to menu
        menu_text = font.render("Click anywhere to return to menu", True, (200, 200, 200))
        menu_rect = menu_text.get_rect(center=(450, 600))
        screen.blit(menu_text, menu_rect)
    
    def handle_story_click(self):
        """Handle click during story"""
        if self.story_showing:
            self.story_showing = False
            return True
        return False
    
    def handle_level_complete_click(self):
        """Handle click on level complete screen"""
        if self.level_complete:
            level = self.levels[self.current_level]
            if level.completed:
                self.next_level()
            else:
                self.restart_level()
            return True
        return False
    
    def handle_campaign_complete_click(self):
        """Handle click on campaign complete screen"""
        if self.campaign_complete:
            self.active = False
            return True
        return False
    
    def get_current_level_rules(self):
        """Get special rules for current level"""
        if self.current_level < len(self.levels):
            return self.levels[self.current_level].special_rules
        return {}