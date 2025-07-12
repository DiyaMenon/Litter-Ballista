import pygame
import math

class ImpactTracker:
    def __init__(self):
        self.total_items_cleaned = 0
        self.plastic_cleaned = 0
        self.paper_cleaned = 0
        self.glass_cleaned = 0
        self.metal_cleaned = 0
        
        # Environmental impact calculations (per item)
        self.impact_data = {
            'trees_saved_per_paper': 0.017,  # 17 trees per 1000 paper items
            'co2_reduced_per_plastic': 0.5,  # 0.5 kg CO2 per plastic item
            'water_saved_per_glass': 2.5,    # 2.5 liters per glass item
            'energy_saved_per_metal': 1.2    # 1.2 kWh per metal item
        }
        
        self.display_timer = 0
        self.showing = False
        self.animate_offset = 0
    
    def add_item(self, item_type, level):
        """Add cleaned item and calculate impact"""
        self.total_items_cleaned += 1
        
        # Determine item type based on level and add to specific counter
        if level == 1:  # Birds/nature level - mixed items
            item_types = ['plastic', 'paper', 'glass', 'metal']
            actual_type = item_types[self.total_items_cleaned % 4]
        elif level == 2:  # Plates level - mostly glass/ceramic
            actual_type = 'glass'
        elif level == 3:  # Space level - mostly metal/plastic
            actual_type = 'metal' if self.total_items_cleaned % 2 == 0 else 'plastic'
        else:
            actual_type = 'plastic'
        
        if actual_type == 'plastic':
            self.plastic_cleaned += 1
        elif actual_type == 'paper':
            self.paper_cleaned += 1
        elif actual_type == 'glass':
            self.glass_cleaned += 1
        elif actual_type == 'metal':
            self.metal_cleaned += 1
    
    def get_trees_saved(self):
        return round(self.paper_cleaned * self.impact_data['trees_saved_per_paper'], 2)
    
    def get_co2_reduced(self):
        return round(self.plastic_cleaned * self.impact_data['co2_reduced_per_plastic'], 1)
    
    def get_water_saved(self):
        return round(self.glass_cleaned * self.impact_data['water_saved_per_glass'], 1)
    
    def get_energy_saved(self):
        return round(self.metal_cleaned * self.impact_data['energy_saved_per_metal'], 1)
    
    def show_impact_summary(self):
        """Show impact summary overlay"""
        self.display_timer = 480  # 8 seconds
        self.showing = True
        self.animate_offset = 0
    
    def update(self):
        if self.showing:
            self.display_timer -= 1
            self.animate_offset += 0.05
            if self.display_timer <= 0:
                self.showing = False
    
    def draw_mini_tracker(self, screen, font):
        """Draw small impact tracker during gameplay"""
        y_offset = 100
        
        # Background
        tracker_bg = pygame.Rect(10, y_offset, 200, 120)
        pygame.draw.rect(screen, (0, 0, 0, 150), tracker_bg)
        pygame.draw.rect(screen, (255, 255, 255), tracker_bg, 2)
        
        # Title
        title_text = font.render("IMPACT", True, (255, 255, 255))
        screen.blit(title_text, (15, y_offset + 5))
        
        # Stats
        stats = [
            f"🌳 {self.get_trees_saved()} trees",
            f"💨 {self.get_co2_reduced()}kg CO2",
            f"💧 {self.get_water_saved()}L water",
            f"⚡ {self.get_energy_saved()}kWh"
        ]
        
        for i, stat in enumerate(stats):
            stat_text = font.render(stat, True, (255, 255, 255))
            screen.blit(stat_text, (15, y_offset + 30 + i * 20))
    
    def draw_impact_summary(self, screen, font, big_font):
        """Draw detailed impact summary overlay"""
        if not self.showing:
            return
        
        # Semi-transparent overlay
        overlay = pygame.Surface((900, 800))
        overlay.set_alpha(200)
        overlay.fill((0, 50, 0))
        screen.blit(overlay, (0, 0))
        
        # Main impact box with animation
        box_y = 150 + math.sin(self.animate_offset) * 5
        impact_box = pygame.Rect(100, box_y, 700, 500)
        pygame.draw.rect(screen, (34, 139, 34), impact_box)
        pygame.draw.rect(screen, (255, 255, 255), impact_box, 4)
        
        # Title
        title_text = big_font.render("ENVIRONMENTAL IMPACT", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(450, box_y + 50))
        screen.blit(title_text, title_rect)
        
        # Total items
        total_text = font.render(f"Total Items Cleaned: {self.total_items_cleaned}", True, (255, 255, 255))
        total_rect = total_text.get_rect(center=(450, box_y + 100))
        screen.blit(total_text, total_rect)
        
        # Impact stats with icons and colors
        impacts = [
            (f"🌳 Trees Saved: {self.get_trees_saved()}", (144, 238, 144)),
            (f"💨 CO2 Reduced: {self.get_co2_reduced()} kg", (135, 206, 235)),
            (f"💧 Water Saved: {self.get_water_saved()} liters", (64, 224, 208)),
            (f"⚡ Energy Saved: {self.get_energy_saved()} kWh", (255, 215, 0))
        ]
        
        for i, (impact_text, color) in enumerate(impacts):
            # Background for each stat
            stat_bg = pygame.Rect(150, box_y + 150 + i * 70, 600, 50)
            pygame.draw.rect(screen, color, stat_bg)
            pygame.draw.rect(screen, (255, 255, 255), stat_bg, 2)
            
            # Text
            text = font.render(impact_text, True, (0, 0, 0))
            text_rect = text.get_rect(center=stat_bg.center)
            screen.blit(text, text_rect)
        
        # Motivational message
        if self.total_items_cleaned > 50:
            message = "Amazing! You're making a real difference! 🌍"
        elif self.total_items_cleaned > 20:
            message = "Great work! Keep cleaning for the planet! 🌱"
        else:
            message = "Every item counts! Keep going! ♻️"
        
        message_text = font.render(message, True, (255, 255, 255))
        message_rect = message_text.get_rect(center=(450, box_y + 450))
        screen.blit(message_text, message_rect)
        
        # Continue instruction
        continue_text = font.render("Click anywhere to continue...", True, (200, 200, 200))
        continue_rect = continue_text.get_rect(center=(450, box_y + 480))
        screen.blit(continue_text, continue_rect)
    
    def handle_click(self):
        """Handle click to close impact summary"""
        if self.showing:
            self.showing = False
            return True
        return False