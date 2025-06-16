import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set the screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set the title of the window
pygame.display.set_caption("Gravity Switcher Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Fonts
font = pygame.font.Font(None, 36)

# Load player image
player_img = pygame.image.load('kangaroo.png')
player_img = pygame.transform.scale(player_img, (50, 50))  # Scale the player image
player_rect = player_img.get_rect()

# Load background images
backgrounds = [
    pygame.image.load('background_india.png').convert(),
    pygame.image.load('background_paris.png').convert(),
    pygame.image.load('background_egypt.png').convert(),
    pygame.image.load('background_beach.png').convert(),
    pygame.image.load('background_italy.png').convert()
]
backgrounds = [pygame.transform.scale(bg, (WIDTH, HEIGHT)) for bg in backgrounds]

# Load and scale welcome screen background image
welcome_background = pygame.image.load('welcome_background.png').convert()
welcome_background = pygame.transform.scale(welcome_background, (WIDTH, HEIGHT))

#Load and scale instructions screen background image
instructions_background = pygame.image.load('instructions.png').convert()
instructions_background = pygame.transform.scale(instructions_background, (WIDTH, HEIGHT))

#Load and scale gameover screen background image
game_over_background = pygame.image.load('gameover.jpg').convert()
game_over_background = pygame.transform.scale(game_over_background, (WIDTH, HEIGHT))

# Load the background music
pygame.mixer.music.load('background_music1.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Load sound effects
jump_sound = pygame.mixer.Sound('jump.wav')
point_sound = pygame.mixer.Sound('point.wav')

# Define player properties
player_width = 50
player_height = 50
player_x = 100
player_y = 100
player_speed = 5
player_gravity = 0.5
player_jump_speed = -12
player_velocity_x = 0
player_velocity_y = 0
player_is_jumping = False
jump_start_y = player_y
max_jump_count = 2
jump_count = 0

# Initialize the score and level index
score = 0
level_index = 0

# Other properties
clock = pygame.time.Clock()
FPS = 60

# Buttons
start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
instructions_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50)

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

def draw_instructions():
    screen.blit(instructions_background,(0,0))
    rules = [
        "Rules of the Game:",
        "1. Use LEFT and RIGHT arrows to move.",
        "2. Press SPACE or UP arrow to jump.",
        "3. Collect power-ups for points.",
        "4. Avoid obstacles.",
        "5. Reach the end to advance levels.",
        "Press any key to continue to the main menu."
    ]
    # for i, rule in enumerate(rules):
    #     draw_text(rule, font, WHITE, screen, 20, 20 + i * 40)
    # Calculate the total height of the instructions block
     # Calculate the total height of the instructions block
    total_text_height = len(rules) * 40  # Adjust line spacing as needed
    start_y = (HEIGHT - total_text_height) // 2  # Start position for vertical centering

    # Draw each line of instructions
    for i, rule in enumerate(rules):
        text_obj = font.render(rule, True, WHITE)
        text_rect = text_obj.get_rect()
        text_rect.centerx = WIDTH // 2  # Center horizontally
        text_rect.y = start_y + i * 40  # Position vertically
        screen.blit(text_obj, text_rect)
    pygame.display.flip()

def main_menu():
    while True:
        screen.blit(welcome_background, (0, 0))
        draw_text('Gravity Switcher Game', font, WHITE, screen, WIDTH // 2 - 150, HEIGHT // 2 - 100)
        
        pygame.draw.rect(screen, GREEN, start_button)
        draw_text('Start Game', font, BLACK, screen, start_button.x + 20, start_button.y + 10)
        
        pygame.draw.rect(screen, GREEN, instructions_button)
        draw_text('Instructions', font, BLACK, screen, instructions_button.x + 20, instructions_button.y + 10)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    level_selection()
                if instructions_button.collidepoint(event.pos):
                    show_instructions()
                    
        clock.tick(FPS)

def show_instructions():
    while True:
        draw_instructions()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                return

def level_selection():
    easy_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
    medium_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50)
    hard_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 90, 200, 50)
    
    while True:
        screen.blit(welcome_background,(0,0))
        draw_text('Select Difficulty', font, WHITE, screen, WIDTH // 2 - 100, HEIGHT // 2 - 150)
        
        pygame.draw.rect(screen, GREEN, easy_button)
        draw_text('Easy', font, BLACK, screen, easy_button.x + 50, easy_button.y + 10)
        
        pygame.draw.rect(screen, GREEN, medium_button)
        draw_text('Medium', font, BLACK, screen, medium_button.x + 50, medium_button.y + 10)
        
        pygame.draw.rect(screen, GREEN, hard_button)
        draw_text('Hard', font, BLACK, screen, hard_button.x + 50, hard_button.y + 10)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_button.collidepoint(event.pos):
                    run_game('easy')
                if medium_button.collidepoint(event.pos):
                    run_game('medium')
                if hard_button.collidepoint(event.pos):
                    run_game('hard')
                    
        clock.tick(FPS)

def difficulty_to_int(difficulty):
    if difficulty == 'easy':
        return 0
    elif difficulty == 'medium':
        return 1
    elif difficulty == 'hard':
        return 2
    else:
        raise ValueError("Invalid difficulty level")

def generate_level(difficulty):
    difficulty_level = difficulty_to_int(difficulty)
    level = {"platforms": [], "obstacles": [], "power_ups": [], "player_speed": 5 + difficulty_level * 2}

    def overlaps(new_rect, objects):
        for obj in objects:
            # Check for overlap
            if (new_rect["x"] < obj["x"] + obj["width"] and
                new_rect["x"] + new_rect["width"] > obj["x"] and
                new_rect["y"] < obj["y"] + obj["height"] and
                new_rect["y"] + new_rect["height"] > obj["y"]):
                return True
        return False

    # Minimum distance between platforms
    min_distance = 50

    # Generate platforms
    moving_platform_count = max(1, 5 - 2 * difficulty_level)  # Reduce moving platforms with difficulty
    total_platforms = 3 + difficulty_level  # Total platforms based on difficulty

    for i in range(total_platforms):
        while True:
            platform_width = random.randint(100, 200)  # Wider platforms
            platform_height = 20
            platform_x = random.randint(0, WIDTH - platform_width)
            platform_y = random.randint(50 + player_height, HEIGHT - platform_height - 50)
            is_moving = (moving_platform_count > 0) and (difficulty_level == 0) and (random.choice([True, False]))

            new_platform = {
                "x": platform_x, "y": platform_y,
                "width": platform_width, "height": platform_height,
                "moving": is_moving,
                "range": 100,
                "direction": random.choice([-1, 1]),
                "speed": 2  # Adjust speed as needed
            }
            
            # Check for overlaps and minimum distance with existing platforms
            if not overlaps(new_platform, level["platforms"]):
                is_far_enough = True
                for existing_platform in level["platforms"]:
                    if (abs(new_platform["x"] - existing_platform["x"]) < min_distance or
                        abs(new_platform["y"] - existing_platform["y"]) < min_distance):
                        is_far_enough = False
                        break
                
                if is_far_enough:
                    level["platforms"].append(new_platform)
                    if is_moving:
                        moving_platform_count -= 1
                    break

    # Generate obstacles
    obstacle_speed = 3 + difficulty_level * 2  # Speed increases with difficulty
    for i in range(2 + difficulty_level):  # More obstacles as difficulty increases
        while True:
            obstacle_width = 20
            obstacle_height = 20
            obstacle_x = random.randint(0, WIDTH - obstacle_width)
            obstacle_y = random.randint(50 + player_height, HEIGHT - obstacle_height - 50)
            direction = "horizontal" if difficulty_level == 1 else random.choice(["horizontal", "vertical"])
            new_obstacle = {
                "x": obstacle_x,
                "y": obstacle_y,
                "width": obstacle_width,
                "height": obstacle_height,
                "direction": direction if difficulty_level > 0 else "static",  # Non-moving obstacles for easy level
                "speed": obstacle_speed
            }
            if (not overlaps(new_obstacle, level["obstacles"]) and
                not overlaps(new_obstacle, level["platforms"])):
                level["obstacles"].append(new_obstacle)
                break

    # Generate power-ups
    for i in range(2 + difficulty_level):  # More power-ups as difficulty increases
        while True:
            power_up_x = random.randint(0, WIDTH - 20)
            power_up_y = random.randint(50 + player_height, HEIGHT - 70)
            new_power_up = {
                "x": power_up_x,
                "y": power_up_y,
                "width": 20,
                "height": 20
            }
            if (not overlaps(new_power_up, level["power_ups"]) and
                not overlaps(new_power_up, level["platforms"]) and
                not overlaps(new_power_up, level["obstacles"])):
                level["power_ups"].append(new_power_up)
                break
    
    return level

# def generate_level(difficulty):
#     difficulty_level = difficulty_to_int(difficulty)
#     level = {"platforms": [], "obstacles": [], "power_ups": [], "player_speed": 5 + difficulty_level * 2}
    
#     def overlaps(new_rect, objects):
#         for obj in objects:
#             if (new_rect["x"] < obj["x"] + obj["width"] and
#                 new_rect["x"] + new_rect["width"] > obj["x"] and
#                 new_rect["y"] < obj["y"] + obj["height"] and
#                 new_rect["y"] + new_rect["height"] > obj["y"]):
#                 return True
#         return False
    
#     # Generate platforms
#     moving_platform_count = max(1, 5 - 2 * difficulty_level)  # Reduce moving platforms with difficulty
#     total_platforms = 3 + difficulty_level  # Total platforms based on difficulty

#     for i in range(total_platforms):
#         while True:
#             platform_width = random.randint(100, 200)  # Wider platforms
#             platform_height = 20
#             platform_x = random.randint(0, WIDTH - platform_width)
#             platform_y = random.randint(50 + player_height, HEIGHT - platform_height - 50)
#             is_moving = (moving_platform_count > 0) and (difficulty_level == 0) and (random.choice([True, False]))

#             new_platform = {
#                 "x": platform_x, "y": platform_y,
#                 "width": platform_width, "height": platform_height,
#                 "moving": is_moving,
#                 "range": 100,
#                 "direction": random.choice([-1, 1]),
#                 "speed": 2  # Adjust speed as needed
#             }
#             # Check for overlaps only with already created platforms
#             if not overlaps(new_platform, level["platforms"]):
#                 level["platforms"].append(new_platform)
#                 if is_moving:
#                     moving_platform_count -= 1
#                 break
    
#     # Generate obstacles
#     obstacle_speed = 3 + difficulty_level * 2  # Speed increases with difficulty
#     for i in range(2 + difficulty_level):  # More obstacles as difficulty increases
#         while True:
#             obstacle_width = 20
#             obstacle_height = 20
#             obstacle_x = random.randint(0, WIDTH - obstacle_width)
#             obstacle_y = random.randint(50 + player_height, HEIGHT - obstacle_height - 50)
#             direction = "horizontal" if difficulty_level == 1 else random.choice(["horizontal", "vertical"])
#             new_obstacle = {
#                 "x": obstacle_x,
#                 "y": obstacle_y,
#                 "width": obstacle_width,
#                 "height": obstacle_height,
#                 "direction": direction if difficulty_level > 0 else "static",  # Non-moving obstacles for easy level
#                 "speed": obstacle_speed
#             }
#             if (not overlaps(new_obstacle, level["obstacles"]) and
#                 not overlaps(new_obstacle, level["platforms"])):
#                 level["obstacles"].append(new_obstacle)
#                 break

#     # Generate power-ups
#     for i in range(2 + difficulty_level):  # More power-ups as difficulty increases
#         while True:
#             power_up_x = random.randint(0, WIDTH - 20)
#             power_up_y = random.randint(50 + player_height, HEIGHT - 70)
#             new_power_up = {
#                 "x": power_up_x,
#                 "y": power_up_y,
#                 "width": 20,
#                 "height": 20
#             }
#             if (not overlaps(new_power_up, level["power_ups"]) and
#                 not overlaps(new_power_up, level["platforms"]) and
#                 not overlaps(new_power_up, level["obstacles"])):
#                 level["power_ups"].append(new_power_up)
#                 break
    
#     return level

def run_game(difficulty):
    global player_x, player_y, player_velocity_y, player_velocity_x, jump_count, player_is_jumping, score, level_index
    level_index = 0
    score = 0
    
    while True:
        level = generate_level(difficulty)
        player_x = 100
        player_y = 100
        player_velocity_y = 0
        player_velocity_x = 0
        player_is_jumping = False
        jump_count = 0
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player_velocity_x = -player_speed
                    if event.key == pygame.K_RIGHT:
                        player_velocity_x = player_speed
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                        if jump_count < max_jump_count:
                            player_velocity_y = player_jump_speed
                            jump_count += 1
                            jump_sound.play()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        player_velocity_x = 0
            
            player_velocity_y += player_gravity
            player_x += player_velocity_x
            player_y += player_velocity_y
            
            if player_x < 0:
                player_x = 0
            if player_x > WIDTH - player_width:
                player_x = WIDTH - player_width
            if player_y > HEIGHT - player_height:
                player_y = HEIGHT - player_height
                jump_count = 0
            
            # Collisions with platforms
            for platform in level["platforms"]:
                if (player_x + player_width > platform["x"] and
                    player_x < platform["x"] + platform["width"] and
                    player_y + player_height > platform["y"] and
                    player_y + player_height < platform["y"] + platform["height"] and
                    player_velocity_y > 0):
                    player_velocity_y = 0
                    jump_count = 0
                    player_y = platform["y"] - player_height  # Adjust player position

            # Move platforms (easy level)
            for platform in level["platforms"]:
                if platform["moving"]:
                    platform["x"] += platform["direction"] * platform["speed"]
                    if platform["x"] < 0 or platform["x"] + platform["width"] > WIDTH:
                        platform["direction"] *= -1
            
            # Move obstacles
            for obstacle in level["obstacles"]:
                if obstacle["direction"] == "horizontal":
                    obstacle["x"] += obstacle["speed"]
                    if obstacle["x"] < 0 or obstacle["x"] + obstacle["width"] > WIDTH:
                        obstacle["speed"] *= -1
                elif obstacle["direction"] == "vertical":
                    obstacle["y"] += obstacle["speed"]
                    if obstacle["y"] < 0 or obstacle["y"] + obstacle["height"] > HEIGHT:
                        obstacle["speed"] *= -1
            
            # Collision with obstacles
            for obstacle in level["obstacles"]:
                if (player_x < obstacle["x"] + obstacle["width"] and
                    player_x + player_width > obstacle["x"] and
                    player_y < obstacle["y"] + obstacle["height"] and
                    player_y + player_height > obstacle["y"]):
                    # Player has collided with an obstacle
                    show_game_over()
                    return

            # Collect power-ups
            for power_up in level["power_ups"]:
                if (player_x < power_up["x"] + power_up["width"] and
                    player_x + player_width > power_up["x"] and
                    player_y < power_up["y"] + power_up["height"] and
                    player_y + player_height > power_up["y"]):
                    # Collect power-up
                    level["power_ups"].remove(power_up)
                    score += 10
                    point_sound.play()

            # Clear the screen
            screen.blit(backgrounds[level_index], (0, 0))
            
            # Draw platforms
            for platform in level["platforms"]:
                pygame.draw.rect(screen, GREEN, (platform["x"], platform["y"], platform["width"], platform["height"]))
            
            # Draw obstacles
            for obstacle in level["obstacles"]:
                pygame.draw.rect(screen, RED, (obstacle["x"], obstacle["y"], obstacle["width"], obstacle["height"]))
            
            # Draw power-ups
            for power_up in level["power_ups"]:
                pygame.draw.rect(screen, YELLOW, (power_up["x"], power_up["y"], power_up["width"], power_up["height"]))
            
            # Draw player
            screen.blit(player_img, (player_x, player_y))
            
            # Draw score
            draw_text(f"Score: {score}", font, WHITE, screen, 10, 10)
            
            # Update the display
            pygame.display.flip()
            
            # Check if all power-ups are collected to advance the level
            if not level["power_ups"]:
                level_index = (level_index + 1) % len(backgrounds)
                break
            
            # Limit the frame rate
            clock.tick(FPS)

def show_game_over():
    while True:
        screen.blit(game_over_background,(0,0))
        draw_text('Game Over', font, BLACK, screen, WIDTH // 2 - 60, HEIGHT // 2 - 100)
        #draw_text(f'Final Score: {score}', font, WHITE, screen, WIDTH // 2 - 100, HEIGHT // 2 - 50)
        
        # Restart button
        restart_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 20, 200, 50)
        #restart_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 20, 200, 50)
        back_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 60, 200, 50)
        #back_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 120, 200, 50)
        
        pygame.draw.rect(screen, GREEN, restart_button)
        draw_text('Restart', font, BLACK, screen, restart_button.x + 50, restart_button.y + 10)
        
        pygame.draw.rect(screen, GREEN, back_button)
        draw_text('Back to Menu', font, BLACK, screen, back_button.x + 20, back_button.y + 10)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    level_selection()
                if back_button.collidepoint(event.pos):
                    main_menu()
                    
        clock.tick(FPS)

if __name__ == "__main__":
    main_menu()

