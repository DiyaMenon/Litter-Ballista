import pygame
import json
import os

class Achievement:
    def __init__(self, id, name, description, icon, unlock_condition, reward_type, reward_data):
        self.id = id
        self.name = name
        self.description = description
        self.icon = icon
        self.unlock_condition = unlock_condition
        self.reward_type = reward_type  # 'gun', 'background', 'effect'
        self.reward_data = reward_data
        self.unlocked = False
        self.progress = 0
        self.max_progress = unlock_condition.get('target', 1)

class AchievementSystem:
    def __init__(self):
        self.achievements = {}
        self.unlocked_guns = [1]  # Start with gun 1
        self.unlocked_backgrounds = [1]  # Start with background 1
        self.unlocked_effects = ['normal']
        self.current_gun = 1
        self.current_background = 1
        self.current_effect = 'normal'
        
        self.notification_queue = []
        self.showing_notification = False
        self.notification_timer = 0
        
        self.setup_achievements()
        self.load_progress()
    
    def setup_achievements(self):
        """Define all achievements"""
        achievements_data = [
            {
                'id': 'first_shot',
                'name': 'First Shot',
                'description': 'Fire your first shot',
                'icon': '🎯',
                'condition': {'type': 'shots_fired', 'target': 1},
                'reward_type': 'effect',
                'reward_data': 'sparkle'
            },
            {
                'id': 'sharpshooter',
                'name': 'Sharpshooter',
                'description': 'Hit 50 targets',
                'icon': '🏹',
                'condition': {'type': 'targets_hit', 'target': 50},
                'reward_type': 'gun',
                'reward_data': 2
            },
            {
                'id': 'eco_warrior',
                'name': 'Eco Warrior',
                'description': 'Clean 100 items',
                'icon': '🌍',
                'condition': {'type': 'items_cleaned', 'target': 100},
                'reward_type': 'background',
                'reward_data': 2
            },
            {
                'id': 'speed_demon',
                'name': 'Speed Demon',
                'description': 'Complete level 1 in under 30 seconds',
                'icon': '⚡',
                'condition': {'type': 'level_time', 'target': 30, 'level': 1},
                'reward_type': 'gun',
                'reward_data': 3
            },
            {
                'id': 'perfectionist',
                'name': 'Perfectionist',
                'description': 'Achieve 90% accuracy in a game',
                'icon': '💎',
                'condition': {'type': 'accuracy', 'target': 90},
                'reward_type': 'effect',
                'reward_data': 'rainbow'
            },
            {
                'id': 'tree_saver',
                'name': 'Tree Saver',
                'description': 'Save 10 trees through recycling',
                'icon': '🌳',
                'condition': {'type': 'trees_saved', 'target': 10},
                'reward_type': 'background',
                'reward_data': 3
            },
            {
                'id': 'master_cleaner',
                'name': 'Master Cleaner',
                'description': 'Clean 500 items total',
                'icon': '👑',
                'condition': {'type': 'items_cleaned', 'target': 500},
                'reward_type': 'gun',
                'reward_data': 4
            }
        ]
        
        for data in achievements_data:
            achievement = Achievement(
                data['id'], data['name'], data['description'], data['icon'],
                data['condition'], data['reward_type'], data['reward_data']
            )
            self.achievements[data['id']] = achievement
    
    def update_progress(self, event_type, value, **kwargs):
        """Update achievement progress based on game events"""
        for achievement in self.achievements.values():
            if achievement.unlocked:
                continue
            
            condition = achievement.unlock_condition
            
            if condition['type'] == event_type:
                if event_type == 'level_time' and kwargs.get('level') == condition.get('level'):
                    if value <= condition['target']:
                        self.unlock_achievement(achievement.id)
                elif event_type == 'accuracy':
                    if value >= condition['target']:
                        self.unlock_achievement(achievement.id)
                elif event_type in ['shots_fired', 'targets_hit', 'items_cleaned', 'trees_saved']:
                    achievement.progress = min(achievement.progress + value, achievement.max_progress)
                    if achievement.progress >= achievement.max_progress:
                        self.unlock_achievement(achievement.id)
    
    def unlock_achievement(self, achievement_id):
        """Unlock an achievement and grant rewards"""
        if achievement_id not in self.achievements:
            return
        
        achievement = self.achievements[achievement_id]
        if achievement.unlocked:
            return
        
        achievement.unlocked = True
        
        # Grant reward
        if achievement.reward_type == 'gun':
            if achievement.reward_data not in self.unlocked_guns:
                self.unlocked_guns.append(achievement.reward_data)
        elif achievement.reward_type == 'background':
            if achievement.reward_data not in self.unlocked_backgrounds:
                self.unlocked_backgrounds.append(achievement.reward_data)
        elif achievement.reward_type == 'effect':
            if achievement.reward_data not in self.unlocked_effects:
                self.unlocked_effects.append(achievement.reward_data)
        
        # Add notification
        self.notification_queue.append(achievement)
        self.save_progress()
    
    def update(self):
        """Update notification system"""
        if not self.showing_notification and self.notification_queue:
            self.showing_notification = True
            self.notification_timer = 300  # 5 seconds
        
        if self.showing_notification:
            self.notification_timer -= 1
            if self.notification_timer <= 0:
                self.showing_notification = False
                if self.notification_queue:
                    self.notification_queue.pop(0)
    
    def draw_notification(self, screen, font):
        """Draw achievement unlock notification"""
        if not self.showing_notification or not self.notification_queue:
            return
        
        achievement = self.notification_queue[0]
        
        # Notification box
        box_width = 400
        box_height = 100
        box_x = (900 - box_width) // 2
        box_y = 50
        
        notification_box = pygame.Rect(box_x, box_y, box_width, box_height)
        pygame.draw.rect(screen, (255, 215, 0), notification_box)
        pygame.draw.rect(screen, (255, 255, 255), notification_box, 3)
        
        # Achievement unlocked text
        unlock_text = font.render("ACHIEVEMENT UNLOCKED!", True, (0, 0, 0))
        unlock_rect = unlock_text.get_rect(center=(box_x + box_width//2, box_y + 25))
        screen.blit(unlock_text, unlock_rect)
        
        # Achievement name and icon
        name_text = font.render(f"{achievement.icon} {achievement.name}", True, (0, 0, 0))
        name_rect = name_text.get_rect(center=(box_x + box_width//2, box_y + 50))
        screen.blit(name_text, name_rect)
        
        # Reward text
        reward_text = font.render(f"Unlocked: {achievement.reward_type.title()}", True, (0, 0, 0))
        reward_rect = reward_text.get_rect(center=(box_x + box_width//2, box_y + 75))
        screen.blit(reward_text, reward_rect)
    
    def draw_achievements_menu(self, screen, font, big_font):
        """Draw achievements menu overlay"""
        # Semi-transparent overlay
        overlay = pygame.Surface((900, 800))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Menu box
        menu_box = pygame.Rect(100, 50, 700, 700)
        pygame.draw.rect(screen, (50, 50, 100), menu_box)
        pygame.draw.rect(screen, (255, 255, 255), menu_box, 3)
        
        # Title
        title_text = big_font.render("ACHIEVEMENTS", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(450, 100))
        screen.blit(title_text, title_rect)
        
        # Achievement list
        y_offset = 150
        for achievement in self.achievements.values():
            # Achievement box
            ach_box = pygame.Rect(120, y_offset, 660, 80)
            color = (100, 200, 100) if achievement.unlocked else (100, 100, 100)
            pygame.draw.rect(screen, color, ach_box)
            pygame.draw.rect(screen, (255, 255, 255), ach_box, 2)
            
            # Icon and name
            icon_text = font.render(achievement.icon, True, (255, 255, 255))
            screen.blit(icon_text, (130, y_offset + 10))
            
            name_text = font.render(achievement.name, True, (255, 255, 255))
            screen.blit(name_text, (170, y_offset + 10))
            
            # Description
            desc_text = font.render(achievement.description, True, (255, 255, 255))
            screen.blit(desc_text, (170, y_offset + 35))
            
            # Progress bar
            if not achievement.unlocked and achievement.max_progress > 1:
                progress_bg = pygame.Rect(170, y_offset + 55, 200, 15)
                pygame.draw.rect(screen, (50, 50, 50), progress_bg)
                
                progress_width = int((achievement.progress / achievement.max_progress) * 200)
                progress_fill = pygame.Rect(170, y_offset + 55, progress_width, 15)
                pygame.draw.rect(screen, (0, 255, 0), progress_fill)
                
                progress_text = font.render(f"{achievement.progress}/{achievement.max_progress}", True, (255, 255, 255))
                screen.blit(progress_text, (380, y_offset + 55))
            
            y_offset += 90
        
        # Close instruction
        close_text = font.render("Press ESC to close", True, (200, 200, 200))
        close_rect = close_text.get_rect(center=(450, 720))
        screen.blit(close_text, close_rect)
    
    def save_progress(self):
        """Save achievement progress to file"""
        data = {
            'achievements': {aid: {'unlocked': ach.unlocked, 'progress': ach.progress} 
                           for aid, ach in self.achievements.items()},
            'unlocked_guns': self.unlocked_guns,
            'unlocked_backgrounds': self.unlocked_backgrounds,
            'unlocked_effects': self.unlocked_effects,
            'current_gun': self.current_gun,
            'current_background': self.current_background,
            'current_effect': self.current_effect
        }
        
        try:
            with open('achievements.json', 'w') as f:
                json.dump(data, f)
        except:
            pass  # Fail silently if can't save
    
    def load_progress(self):
        """Load achievement progress from file"""
        try:
            if os.path.exists('achievements.json'):
                with open('achievements.json', 'r') as f:
                    data = json.load(f)
                
                # Load achievement progress
                for aid, progress in data.get('achievements', {}).items():
                    if aid in self.achievements:
                        self.achievements[aid].unlocked = progress.get('unlocked', False)
                        self.achievements[aid].progress = progress.get('progress', 0)
                
                # Load unlocked items
                self.unlocked_guns = data.get('unlocked_guns', [1])
                self.unlocked_backgrounds = data.get('unlocked_backgrounds', [1])
                self.unlocked_effects = data.get('unlocked_effects', ['normal'])
                self.current_gun = data.get('current_gun', 1)
                self.current_background = data.get('current_background', 1)
                self.current_effect = data.get('current_effect', 'normal')
        except:
            pass  # Fail silently if can't load