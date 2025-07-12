import random

class EnvironmentalFacts:
    def __init__(self):
        self.facts = [
            "🌍 Plastic bottles take 450 years to decompose in landfills!",
            "♻️ Recycling one aluminum can saves enough energy to power a TV for 3 hours!",
            "🌊 8 million tons of plastic waste enter our oceans every year!",
            "🌳 Recycling one ton of paper saves 17 trees and 7,000 gallons of water!",
            "⚡ Glass can be recycled endlessly without losing quality!",
            "🐢 Over 1 million marine animals die each year from plastic pollution!",
            "🌱 Composting food waste reduces methane emissions by 50%!",
            "🔋 E-waste is the fastest growing waste stream globally!",
            "💧 It takes 1,000 years for a plastic bag to decompose!",
            "🌟 Recycling creates 6 times more jobs than landfilling!",
            "🏭 Manufacturing recycled paper uses 60% less energy than new paper!",
            "🌈 Every minute, 1 million plastic bottles are purchased worldwide!",
            "🦋 Proper recycling can reduce greenhouse gas emissions by 35%!",
            "🌺 Food waste accounts for 30% of all household garbage!",
            "⭐ Recycling steel saves 75% of the energy needed to make new steel!"
        ]
        
        self.current_fact = ""
        self.display_timer = 0
        self.showing = False
    
    def show_random_fact(self):
        self.current_fact = random.choice(self.facts)
        self.display_timer = 300  # Show for 5 seconds
        self.showing = True
    
    def update(self):
        if self.showing:
            self.display_timer -= 1
            if self.display_timer <= 0:
                self.showing = False
    
    def draw(self, screen, font, big_font):
        if self.showing:
            # Semi-transparent overlay
            overlay = pygame.Surface((900, 800))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
            
            # Fact box
            fact_box = pygame.Rect(100, 300, 700, 200)
            pygame.draw.rect(screen, (50, 150, 50), fact_box)
            pygame.draw.rect(screen, (255, 255, 255), fact_box, 3)
            
            # Title
            title_text = big_font.render("ECO FACT!", True, (255, 255, 255))
            title_rect = title_text.get_rect(center=(450, 340))
            screen.blit(title_text, title_rect)
            
            # Fact text (word wrap)
            words = self.current_fact.split()
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
            
            y_offset = 380
            for line in lines:
                fact_text = font.render(line, True, (255, 255, 255))
                fact_rect = fact_text.get_rect(center=(450, y_offset))
                screen.blit(fact_text, fact_rect)
                y_offset += 30
            
            # Continue instruction
            continue_text = font.render("Click anywhere to continue...", True, (200, 200, 200))
            continue_rect = continue_text.get_rect(center=(450, 460))
            screen.blit(continue_text, continue_rect)
    
    def handle_click(self):
        if self.showing:
            self.showing = False
            return True
        return False