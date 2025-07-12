import pygame
import random

class SortingChallenge:
    def __init__(self):
        self.active = False
        self.items = []
        self.correct_order = []
        self.player_order = []
        self.current_instruction = ""
        self.timer = 0
        self.challenge_timer = 600  # 10 seconds
        self.completed = False
        self.success = False
        
        # Recycling categories and items
        self.categories = {
            'plastic': ['Plastic Bottle', 'Food Container', 'Shopping Bag'],
            'paper': ['Newspaper', 'Cardboard Box', 'Magazine'],
            'glass': ['Glass Bottle', 'Jar', 'Window Glass'],
            'metal': ['Aluminum Can', 'Steel Can', 'Foil']
        }
        
        self.category_colors = {
            'plastic': (255, 100, 100),
            'paper': (100, 255, 100),
            'glass': (100, 100, 255),
            'metal': (255, 255, 100)
        }
    
    def start_challenge(self):
        self.active = True
        self.completed = False
        self.success = False
        self.player_order = []
        self.timer = self.challenge_timer
        
        # Select random category
        category = random.choice(list(self.categories.keys()))
        self.items = random.sample(self.categories[category], 3)
        self.correct_order = self.items.copy()
        random.shuffle(self.items)
        
        self.current_instruction = f"Sort {category.upper()} items in alphabetical order!"
    
    def update(self):
        if self.active and not self.completed:
            self.timer -= 1
            if self.timer <= 0:
                self.completed = True
                self.success = False
    
    def handle_click(self, mouse_pos):
        if not self.active or self.completed:
            return False
        
        # Check if clicking on items
        item_width = 150
        item_height = 60
        start_x = 375
        start_y = 400
        
        for i, item in enumerate(self.items):
            item_rect = pygame.Rect(start_x, start_y + i * 80, item_width, item_height)
            if item_rect.collidepoint(mouse_pos) and item not in self.player_order:
                self.player_order.append(item)
                
                # Check if challenge is complete
                if len(self.player_order) == len(self.items):
                    self.completed = True
                    self.success = self.player_order == sorted(self.correct_order)
                return True
        
        return False
    
    def draw(self, screen, font, big_font):
        if not self.active:
            return
        
        # Semi-transparent overlay
        overlay = pygame.Surface((900, 800))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Challenge box
        challenge_box = pygame.Rect(50, 150, 800, 500)
        pygame.draw.rect(screen, (30, 30, 60), challenge_box)
        pygame.draw.rect(screen, (255, 255, 255), challenge_box, 3)
        
        # Title
        title_text = big_font.render("SORTING CHALLENGE", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(450, 200))
        screen.blit(title_text, title_rect)
        
        # Instruction
        instruction_text = font.render(self.current_instruction, True, (255, 255, 255))
        instruction_rect = instruction_text.get_rect(center=(450, 250))
        screen.blit(instruction_text, instruction_rect)
        
        # Timer
        if not self.completed:
            timer_text = font.render(f"Time: {self.timer // 60 + 1}s", True, (255, 255, 255))
            screen.blit(timer_text, (750, 170))
        
        # Items to sort
        item_width = 150
        item_height = 60
        start_x = 375
        start_y = 400
        
        for i, item in enumerate(self.items):
            item_rect = pygame.Rect(start_x, start_y + i * 80, item_width, item_height)
            
            # Color based on selection
            if item in self.player_order:
                color = (100, 100, 100)
                text_color = (150, 150, 150)
                order_num = self.player_order.index(item) + 1
            else:
                color = (80, 80, 120)
                text_color = (255, 255, 255)
                order_num = None
            
            pygame.draw.rect(screen, color, item_rect)
            pygame.draw.rect(screen, (255, 255, 255), item_rect, 2)
            
            # Item text
            item_text = font.render(item, True, text_color)
            item_text_rect = item_text.get_rect(center=item_rect.center)
            screen.blit(item_text, item_text_rect)
            
            # Order number
            if order_num:
                order_text = font.render(str(order_num), True, (255, 255, 0))
                screen.blit(order_text, (item_rect.right - 25, item_rect.top + 5))
        
        # Results
        if self.completed:
            if self.success:
                result_text = big_font.render("SUCCESS! +50 BONUS POINTS!", True, (0, 255, 0))
            else:
                result_text = big_font.render("FAILED! Try again next time!", True, (255, 0, 0))
            
            result_rect = result_text.get_rect(center=(450, 580))
            screen.blit(result_text, result_rect)
            
            continue_text = font.render("Click anywhere to continue...", True, (200, 200, 200))
            continue_rect = continue_text.get_rect(center=(450, 620))
            screen.blit(continue_text, continue_rect)
    
    def get_bonus_points(self):
        if self.completed and self.success:
            return 50
        return 0
    
    def handle_completion_click(self):
        if self.completed:
            self.active = False
            return True
        return False