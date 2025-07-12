# fact_popup.py
import pygame
import random

environmental_facts = [
    "Recycling one can saves enough energy to run a TV for 3 hours.",
    "Plastic takes over 400 years to degrade in nature.",
    "1 ton of recycled paper saves 17 trees.",
    "Composting food waste reduces landfill methane.",
    "Recycling 1 ton of plastic saves 16 barrels of oil."
]

def show_fact_popup(screen, font):
    fact = random.choice(environmental_facts)

    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  # semi-transparent background

    lines = split_text(fact, font, screen.get_width() - 100)
    y_offset = (screen.get_height() - len(lines) * 30) // 2

    for i, line in enumerate(lines):
        text = font.render(line, True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen.get_width() // 2, y_offset + i * 30))
        overlay.blit(text, text_rect)

    continue_text = font.render("Press any key to continue...", True, (255, 255, 255))
    continue_rect = continue_text.get_rect(center=(screen.get_width() // 2, screen.get_height() - 60))
    overlay.blit(continue_text, continue_rect)

    screen.blit(overlay, (0, 0))
    pygame.display.flip()

    wait_for_keypress()

def wait_for_keypress():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return

def split_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = ''
    for word in words:
        test_line = current_line + word + ' '
        if font.size(test_line)[0] < max_width:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = word + ' '
    lines.append(current_line.strip())
    return lines
