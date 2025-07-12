# fact_popup.py
import pygame
import random

environmental_facts = [
    "Recycling one aluminum can saves enough energy to run a TV for 3 hours.",
    "Plastic takes over 400 years to degrade in the environment.",
    "1 ton of recycled paper saves 17 trees and 7,000 gallons of water.",
    "Composting food waste reduces methane emissions from landfills.",
    "Recycling 1 ton of plastic saves 16 barrels of oil.",
    "Every ton of recycled steel saves 2,500 pounds of iron ore.",
    "Over 1 million marine animals die each year from plastic pollution.",
    "The average person produces over 4 pounds of trash per day.",
    "Recycling a glass bottle saves enough energy to power a computer for 30 minutes.",
    "Only 9% of plastic ever produced has been recycled.",
    "It takes 500–1,000 years for plastic to degrade in landfills.",
    "Producing new paper from recycled paper uses 70% less energy.",
    "Cutting down trees for paper is one of the leading causes of deforestation.",
    "Electronic waste is the fastest-growing waste stream in the world.",
    "A single plastic bag can kill multiple marine animals if mistaken for food.",
    "Landfills are the third-largest source of methane emissions globally.",
    "You can save 1,460 gallons of water per year by turning off the tap while brushing your teeth.",
    "A leaky faucet can waste over 3,000 gallons of water a year.",
    "Transporting bottled water uses over 17 million barrels of oil per year.",
    "Using a reusable water bottle can save an average of 167 plastic bottles per person annually.",
    "Fast fashion is responsible for 10% of global carbon emissions.",
    "Producing meat generates significantly more CO2 than growing vegetables.",
    "Burning trash releases toxic chemicals and greenhouse gases into the atmosphere.",
    "Switching to LED bulbs can reduce your carbon footprint significantly.",
    "Protecting forests helps absorb 2.6 billion tons of CO2 every year."
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
