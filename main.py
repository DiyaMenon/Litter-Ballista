# Litter Ballista!!!
import pygame
import math
import random
from powerups import PowerUpManager
from environmental_facts import EnvironmentalFacts
from sorting_challenge import SortingChallenge
from weather_effects import WeatherEffect

pygame.init()

#set up variables 
fps = 60
timer = pygame.time.Clock()

#fonts
font = pygame.font.Font('assets/font/myFont.ttf', 32)
big_font = pygame.font.Font('assets/font/myFont.ttf', 60)
small_font = pygame.font.Font('assets/font/myFont.ttf', 24)

#dimensions
WIDTH = 900
HEIGHT = 800
screen = pygame.display.set_mode([WIDTH, HEIGHT])

#empty lists needed for bg, banners, guns and target images
bgs = []
banners = []
guns = []
target_images = [[], [], []]

#number of targets according to level
targets = {1: [10, 5, 3],
           2: [12, 8, 5],
           3: [15, 12, 8, 3]}
level = 0
points = 0
total_shots = 0

# Initialize new systems
power_up_manager = PowerUpManager()
environmental_facts = EnvironmentalFacts()
sorting_challenge = SortingChallenge()
weather_effect = WeatherEffect()


#for mode 0=freeplay, 1=accuracy, 2=timed
mode = 0
ammo = 0
time_passed = 0
time_remaining = 0
counter = 1
best_freeplay = 0
best_ammo = 0
best_timed = 0

shot = False
menu = True
game_over = False
pause = False
clicked = False
write_values = False
new_coords = True
show_challenge = False
challenge_cooldown = 0

one_coords = [[], [], []]
two_coords = [[], [], []]
three_coords = [[], [], [], []]

#LOADING THE IMAGES
menu_img = pygame.image.load(f'assets/menus/mainMenu.png')
game_over_img = pygame.image.load(f'assets/menus/gameOver.png')
pause_img = pygame.image.load(f'assets/menus/pause.png')

for i in range(1, 4):
    bgs.append(pygame.image.load(f'assets/bgs/{i}.png'))
    banners.append(pygame.image.load(f'assets/banners/{i}.png'))
    guns.append(pygame.transform.scale(pygame.image.load(f'assets/guns/{i}.png'), (100, 100)))
    if i < 3:
        for j in range(1, 4):
            target_images[i - 1].append(pygame.transform.scale(
                pygame.image.load(f'assets/targets/{i}/{j}.png'), (120 - (j * 18), 80 - (j * 12))))
    else:
        for j in range(1, 5):
            target_images[i - 1].append(pygame.transform.scale(
                pygame.image.load(f'assets/targets/{i}/{j}.png'), (120 - (j * 18), 80 - (j * 12))))



#OPENING THE HIGH SCORE TEXT FILE AND WRITING IF THE HIG SCORE CHANGES 

file = open('high_scores.txt', 'r')                                      #file = open ('name of file','r for read or w for write') 
#when we first open we want to read becuase we need to check whether the best scores are better than the pervious scores that time we dont need to write
#so we put the parameter 'r' in the open function for reading the file first
read_file = file.readlines()                                             #reading the file
file.close()                                                             #to protect the file as we dont want it open throughout
best_freeplay = int(read_file[0])
best_ammo = int(read_file[1])
best_timed = int(read_file[2])



#ADDING SOUNDS
pygame.mixer.init()
pygame.mixer.music.load('assets/sounds/bg_music.mp3')
plate_sound = pygame.mixer.Sound('assets/sounds/Splash water.mp3')
plate_sound.set_volume(2.5)
bird_sound = pygame.mixer.Sound('assets/sounds/Drill Gear.mp3')
bird_sound.set_volume(.2)
laser_sound = pygame.mixer.Sound('assets/sounds/Laser Gun.wav')
laser_sound.set_volume(.3)
pygame.mixer.music.play()




#TO DISPLAY THE SCORE OF EACH OF THE MODES
def draw_score():
    points_text = font.render(f'Points: {points}', True, 'black')
    screen.blit(points_text, (320, 660))
    shots_text = font.render(f'Total Shots: {total_shots}', True, 'black')
    screen.blit(shots_text, (320, 687))
    time_text = font.render(f'Time Elapsed: {time_passed}', True, 'black')
    screen.blit(time_text, (320, 714))
    if mode == 0:
        mode_text = font.render(f'Freeplay!', True, 'black')
    if mode == 1:
        mode_text = font.render(f'Ammo Remaining: {ammo}', True, 'black')
    if mode == 2:
        mode_text = font.render(f'Time Remaining {time_remaining}', True, 'black')
    screen.blit(mode_text, (320, 741))




#making the gun and making it rotate to shoot
def draw_gun():
    global shot, total_shots
    mouse_pos = pygame.mouse.get_pos()
    
    # Apply weather effects to mouse position
    mouse_pos = weather_effect.apply_wind_effect(mouse_pos)
    
    gun_point = (WIDTH / 2, HEIGHT - 200)
    lasers = ['red', 'purple', 'green']
    clicks = pygame.mouse.get_pressed()                                             #storing the clicked status of the mouse in a list
    
    # Handle rapid fire power-up
    rapid_fire_active = power_up_manager.is_active('rapid_fire')
    
    if mouse_pos[0] != gun_point[0]:
        slope = (mouse_pos[1] - gun_point[1]) / (mouse_pos[0] - gun_point[0])
    else:
        slope = -100000                                                              #setting a very high negative slope
   
    
    angle = math.atan(slope)                                                         #inverse tangent of slope of a line = angle between horizontal axis and the line
    rotation = math.degrees(angle)                                                   #converting to degrees


    if mouse_pos[0] < WIDTH / 2:                                                     #if mouse position is on left of the screen we need to flip the gun to look natural
        gun = pygame.transform.flip(guns[level - 1], True, False)
        if mouse_pos[1] < 600:
            screen.blit(pygame.transform.rotate(gun, 90 - rotation), (WIDTH / 2 - 90, HEIGHT - 250))
            if clicks[0]:
                # Multi-shot power-up
                if power_up_manager.is_active('multi_shot'):
                    for i in range(3):
                        offset_x = mouse_pos[0] + (i - 1) * 20
                        offset_y = mouse_pos[1] + (i - 1) * 10
                        pygame.draw.circle(screen, lasers[level - 1], (offset_x, offset_y), 5)
                else:
                    pygame.draw.circle(screen, lasers[level - 1], mouse_pos, 5)
    else:
        gun = guns[level - 1]
        if mouse_pos[1] < 600:
            screen.blit(pygame.transform.rotate(gun, 270 - rotation), (WIDTH / 2 - 30, HEIGHT - 250))
            if clicks[0]:
                # Multi-shot power-up
                if power_up_manager.is_active('multi_shot'):
                    for i in range(3):
                        offset_x = mouse_pos[0] + (i - 1) * 20
                        offset_y = mouse_pos[1] + (i - 1) * 10
                        pygame.draw.circle(screen, lasers[level - 1], (offset_x, offset_y), 5)
                else:
                    pygame.draw.circle(screen, lasers[level - 1], mouse_pos, 5)




#moving between the levels 
def move_level(coords):
    # Time freeze power-up slows down movement
    speed_modifier = 0.3 if power_up_manager.is_active('time_freeze') else 1.0
    
    if level == 1 or level == 2:
        max_val = 3
    else:
        max_val = 4
    for i in range(max_val):
        for j in range(len(coords[i])):
            my_coords = coords[i][j]
            if my_coords[0] < -150:
                coords[i][j] = (WIDTH, my_coords[1])                                 # if it moves to the left this code will keep moving it to the right
            else:
                move_speed = (2 ** i) * speed_modifier
                coords[i][j] = (my_coords[0] - move_speed, my_coords[1])
    return coords





#what to do when we are drawing a level- drawing all the enemies 
# lets say we have passed in a list of coordinates of all the enemies(parameter)
def draw_level(coords):
    if level == 1 or level == 2:
        target_rects = [[], [], []]
    else:
        target_rects = [[], [], [], []]
    for i in range(len(coords)):
        for j in range(len(coords[i])):
            target_rects[i].append(pygame.rect.Rect((coords[i][j][0] + 20, coords[i][j][1]),
                                                    (60 - i * 12, 60 - i * 12)))
            screen.blit(target_images[level - 1][i], coords[i][j])
    return target_rects




#checking when we have shot and we need to pass in the list of targets and the coordniate list 
def check_shot(targets, coords):
    global points
    mouse_pos = pygame.mouse.get_pos()
    
    # Apply weather accuracy modifier
    accuracy_mod = weather_effect.get_accuracy_modifier()
    hit_detected = False
    
    # Multi-shot power-up increases hit area
    hit_positions = [mouse_pos]
    if power_up_manager.is_active('multi_shot'):
        hit_positions.extend([
            (mouse_pos[0] - 20, mouse_pos[1] - 10),
            (mouse_pos[0] + 20, mouse_pos[1] + 10)
        ])
    
    for i in range(len(targets)):
        for j in range(len(targets[i])):
            for hit_pos in hit_positions:
                # Apply weather accuracy - random chance to miss
                if random.random() > accuracy_mod:
                    continue
                    
                if targets[i][j].collidepoint(hit_pos):
                    coords[i].pop(j)
                    base_points = 10 + 10 * (i ** 2)
                    score_multiplier = power_up_manager.get_score_multiplier()
                    points += base_points * score_multiplier
                    hit_detected = True
                    
                    if level == 1:
                        bird_sound.play()
                    elif level == 2:
                        plate_sound.play()
                    elif level == 3:
                        laser_sound.play()
                    break
            if hit_detected:
                break
        if hit_detected:
            break
    return coords





def draw_menu():
    global game_over, pause, mode, level, menu, time_passed, total_shots, points, ammo
    global time_remaining, best_freeplay, best_ammo, best_timed, write_values, clicked, new_coords
    global challenge_cooldown
    game_over = False
    pause = False
    challenge_cooldown = 0
    screen.blit(menu_img, (0, 0))
    mouse_pos = pygame.mouse.get_pos()
    clicks = pygame.mouse.get_pressed()
    freeplay_button = pygame.rect.Rect((170, 524), (260, 100))
    screen.blit(font.render(f'{best_freeplay}', True, 'black'), (340, 580))
    ammo_button = pygame.rect.Rect((475, 524), (260, 100))
    screen.blit(font.render(f'{best_ammo}', True, 'black'), (650, 580))
    timed_button = pygame.rect.Rect((170, 661), (260, 100))
    screen.blit(font.render(f'{best_timed}', True, 'black'), (350, 710))
    reset_button = pygame.rect.Rect((475, 661), (260, 100))
    if freeplay_button.collidepoint(mouse_pos) and clicks[0] and not clicked:
        mode = 0
        level = 1
        menu = False
        time_passed = 0
        total_shots = 0
        points = 0
        clicked = True
        new_coords = True
        environmental_facts.show_random_fact()
    if ammo_button.collidepoint(mouse_pos) and clicks[0] and not clicked:
        mode = 1
        level = 1
        menu = False
        time_passed = 0
        ammo = 81
        total_shots = 0
        points = 0
        clicked = True
        new_coords = True
        environmental_facts.show_random_fact()
    if timed_button.collidepoint(mouse_pos) and clicks[0] and not clicked:
        mode = 2
        level = 1
        menu = False
        time_remaining = 30
        time_passed = 0
        total_shots = 0
        points = 0
        clicked = True
        new_coords = True
        environmental_facts.show_random_fact()
    if reset_button.collidepoint(mouse_pos) and clicks[0] and not clicked:
        best_freeplay = 0
        best_ammo = 0
        best_timed = 0
        clicked = True
        write_values = True

    #button = pygame.draw.rect (screen, 'green',[125, 500, 300, 125],3) 
    #^to see the rectangle drawn then change the code to 





def draw_game_over():
    global clicked, level, pause, game_over, menu, points, total_shots, time_passed, time_remaining
    if mode == 0:
        display_score = time_passed
    else:
        display_score = points
    screen.blit(game_over_img, (0, 0))
    mouse_pos = pygame.mouse.get_pos()
    clicks = pygame.mouse.get_pressed()
    exit_button = pygame.rect.Rect((170, 661), (260, 100))
    menu_button = pygame.rect.Rect((475, 661), (260, 100))
    screen.blit(big_font.render(f'{display_score}', True, 'black'), (650, 570))
    if menu_button.collidepoint(mouse_pos) and clicks[0] and not clicked:
        clicked = True
        level = 0
        pause = False
        game_over = False
        menu = True
        points = 0
        total_shots = 0
        time_passed = 0
        time_remaining = 0
    if exit_button.collidepoint(mouse_pos) and clicks[0] and not clicked:
        global run
        run = False




def draw_pause():
    global level, pause, menu, points, total_shots, time_passed, time_remaining, clicked, new_coords
    global challenge_cooldown
    screen.blit(pause_img, (0, 0))
    mouse_pos = pygame.mouse.get_pos()
    clicks = pygame.mouse.get_pressed()
    resume_button = pygame.rect.Rect((170, 661), (260, 100))
    menu_button = pygame.rect.Rect((475, 661), (260, 100))
    if resume_button.collidepoint(mouse_pos) and clicks[0] and not clicked:
        level = resume_level
        pause = False
        clicked = True
    if menu_button.collidepoint(mouse_pos) and clicks[0] and not clicked:
        pygame.mixer.music.play()
        level = 0
        pause = False
        menu = True
        points = 0
        total_shots = 0
        time_passed = 0
        time_remaining = 0
        clicked = True
        new_coords = True
        challenge_cooldown = 0



run = True
while run:
    timer.tick(fps)
    if level != 0:
        if counter < 60:
            counter += 1
        else:
            counter = 1
            time_passed += 1
            if mode == 2:
                time_remaining -= 1
            
            # Update challenge cooldown
            if challenge_cooldown > 0:
                challenge_cooldown -= 1

    # Update systems
    if level > 0:
        power_up_manager.update()
        weather_effect.update()
        
        # Trigger sorting challenge randomly
        if not sorting_challenge.active and challenge_cooldown <= 0 and random.randint(1, 1800) == 1:  # ~30 second average
            sorting_challenge.start_challenge()
            challenge_cooldown = 1800  # 30 second cooldown
    
    environmental_facts.update()
    sorting_challenge.update()

    if new_coords:
        # initialize enemy coordinates
        one_coords = [[], [], []]
        two_coords = [[], [], []]
        three_coords = [[], [], [], []]
        for i in range(3):
            my_list = targets[1]
            for j in range(my_list[i]):
                one_coords[i].append((WIDTH // (my_list[i]) * j, 300 - (i * 150) + 30 * (j % 2)))
        for i in range(3):
            my_list = targets[2]
            for j in range(my_list[i]):
                two_coords[i].append((WIDTH // (my_list[i]) * j, 300 - (i * 150) + 30 * (j % 2)))
        for i in range(4):
            my_list = targets[3]
            for j in range(my_list[i]):
                three_coords[i].append((WIDTH // (my_list[i]) * j, 300 - (i * 100) + 30 * (j % 2)))
        new_coords = False

    screen.fill('black')
    screen.blit(bgs[level - 1], (0, 0))
    screen.blit(banners[level - 1], (0, HEIGHT - 200))
    if menu:
        level = 0
        draw_menu()
    if game_over:
        level = 0
        draw_game_over()
    if pause:
        level = 0
        draw_pause()

    if level == 1:
        target_boxes = draw_level(one_coords)
        one_coords = move_level(one_coords)
        if shot:
            one_coords = check_shot(target_boxes, one_coords)
            shot = False
    elif level == 2:
        target_boxes = draw_level(two_coords)
        two_coords = move_level(two_coords)
        if shot:
            two_coords = check_shot(target_boxes, two_coords)
            shot = False
    elif level == 3:
        target_boxes = draw_level(three_coords)
        three_coords = move_level(three_coords)
        if shot:
            three_coords = check_shot(target_boxes, three_coords)
            shot = False
    if level > 0:
        draw_gun()
        draw_score()
        
        # Draw new systems
        power_up_manager.draw(screen, small_font)
        power_up_manager.draw_active_effects(screen, small_font)
        weather_effect.draw(screen)
        weather_effect.draw_weather_indicator(screen, small_font)
    
    # Draw overlays (always on top)
    environmental_facts.draw(screen, font, big_font)
    sorting_challenge.draw(screen, font, big_font)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_position = pygame.mouse.get_pos()
            
            # Handle environmental facts click
            if environmental_facts.handle_click():
                continue
            
            # Handle sorting challenge clicks
            if sorting_challenge.handle_completion_click():
                points += sorting_challenge.get_bonus_points()
                continue
            
            if sorting_challenge.handle_click(mouse_position):
                continue
            
            # Handle power-up collection
            if level > 0:
                power_up_manager.check_collection(mouse_position, True)
            
            if (0 < mouse_position[0] < WIDTH) and (0 < mouse_position[1] < HEIGHT - 200):
                shot = True
                total_shots += 1
                if mode == 1:
                    ammo -= 1
            if (670 < mouse_position[0] < 860) and (660 < mouse_position[1] < 715):
                resume_level = level
                pause = True
                clicked = True
            if (670 < mouse_position[0] < 860) and (715 < mouse_position[1] < 760):
                menu = True
                pygame.mixer.music.play()
                clicked = True
                new_coords = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and clicked:
            clicked = False



     #what to do next when a level is over
    if level > 0:
        if target_boxes == [[], [], []] and level < 3:                                           # if target boxes is empty and level <3 go to next level
            level += 1
        if (level == 3 and target_boxes == [[], [], [], []]) or (mode == 1 and ammo == 0) or (
                mode == 2 and time_remaining == 0):
            new_coords = True
            challenge_cooldown = 0

            pygame.mixer.music.play()

            #we need to track whats the actual score there and rewrite the best score if its greater than the older score 

            #freeplay = in freeplay mode the time should be less than the older time or it should be 0 (when we have never played before)

            if mode == 0:
                if time_passed < best_freeplay or best_freeplay == 0:
                    best_freeplay = time_passed
                    write_values = True


            #accuracy mode = points should be greater thna old score then overwirte the score
            if mode == 1:
                if points > best_ammo:
                    best_ammo = points
                    write_values = True
            
            #timed mode = the points should be greater than old score then overwrite the score
            if mode == 2:
                if points > best_timed:
                    best_timed = points
                    write_values = True
            
            # Show environmental fact at game over
            environmental_facts.show_random_fact()
            game_over = True
    if write_values:
        file = open('high_scores.txt', 'w')                             #opening the highscore text file and w for write since we are going to be editing the high scores
        file.write(f'{best_freeplay}\n{best_ammo}\n{best_timed}')       #overwriting - we need add each one everytime
        file.close()
        write_values = False
    pygame.display.flip()                       #take everything that we told to draw on the screen and put it on the screen
pygame.quit()
