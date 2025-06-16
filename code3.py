import pygame
import sys

# Initialize Pygame
pygame.init()

# Set the screen dimensions
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the title of the window
pygame.display.set_caption("Gravity Switcher Game")

# Load the background images for each level
backgrounds = [
    pygame.image.load('background_india.png').convert(),   # Level 1 background image
    pygame.image.load('background_paris.png').convert(),   # Level 2 background image
    pygame.image.load('background_egypt.png').convert()    # Level 3 background image
]

# Scale background images to fit the screen
backgrounds = [pygame.transform.scale(background, (screen_width, screen_height)) for background in backgrounds]

# Initialize the current level background
current_level_background = backgrounds[0]

# Load the background music
pygame.mixer.music.load('background_music1.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Load sound effects
jump_sound = pygame.mixer.Sound('jump.wav')
point_sound = pygame.mixer.Sound('point.wav')
land_sound = pygame.mixer.Sound('land.wav')
game_over_sound = pygame.mixer.Sound('game_over.wav')
start_game_sound = pygame.mixer.Sound('start_game.wav')
level_up_sound = pygame.mixer.Sound('level_up.wav')

# Load the intro background and kangaroo image
intro_background = pygame.Surface((screen_width, screen_height))
intro_background.fill((0, 0, 0))
kangaroo_image = pygame.image.load('kangaroo.png').convert_alpha()
kangaroo_image = pygame.transform.scale(kangaroo_image, (100, 100))

# Define some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Define the player character
player_width = 50
player_height = 50
player_x = 100
player_y = 100
player_speed = 8  # Increased speed
player_gravity = 0.5
player_jump_speed = -15
player_velocity_y = 0
player_is_jumping = False
gravity_direction = 1  # 1 for normal gravity, -1 for inverted gravity

# Load player image
player_image = pygame.image.load('kangaroo.png').convert_alpha()
player_image = pygame.transform.scale(player_image, (player_width, player_height))

# Define the platforms for each level
platforms_level_1 = [
    {"x": 0, "y": 400, "width": 640, "height": 20, "moving": False},  # Ground
    {"x": 200, "y": 300, "width": 100, "height": 20, "moving": False},  # Platform 1
    {"x": 400, "y": 200, "width": 100, "height": 20, "moving": True, "direction": 1, "range": 150, "speed": 2, "original_x": 400},  # Moving Platform
]

platforms_level_2 = [
    {"x": 0, "y": 400, "width": 640, "height": 20, "moving": False},  # Ground
    {"x": 150, "y": 350, "width": 100, "height": 20, "moving": True, "direction": 1, "range": 200, "speed": 3, "original_x": 150},  # Moving Platform 1
    {"x": 350, "y": 250, "width": 100, "height": 20, "moving": False},  # Platform 2
    {"x": 550, "y": 150, "width": 100, "height": 20, "moving": True, "direction": -1, "range": 150, "speed": 2, "original_x": 550},  # Moving Platform 2
]

platforms_level_3 = [
    {"x": 0, "y": 450, "width": 640, "height": 30, "moving": False},  # Ground
    {"x": 50, "y": 350, "width": 100, "height": 20, "moving": True, "direction": 1, "range": 150, "speed": 3, "original_x": 50},  # Moving Platform 1
    {"x": 400, "y": 250, "width": 100, "height": 20, "moving": True, "direction": -1, "range": 200, "speed": 2, "original_x": 400},  # Moving Platform 2
    {"x": 200, "y": 150, "width": 100, "height": 20, "moving": False},  # Platform 3
]

# Define the obstacles for each level
obstacles_level_1 = [
    {"x": 300, "y": 250, "width": 20, "height": 20},  # Spike 1
    {"x": 500, "y": 350, "width": 20, "height": 20},  # Spike 2
]

obstacles_level_2 = [
    {"x": 300, "y": 250, "width": 20, "height": 20},  # Spike 1
    {"x": 500, "y": 350, "width": 20, "height": 20},  # Spike 2
    {"x": 400, "y": 300, "width": 20, "height": 20},  # Spike 3
]

obstacles_level_3 = [
    {"x": 300, "y": 300, "width": 20, "height": 20},  # Spike 1
    {"x": 500, "y": 400, "width": 20, "height": 20},  # Spike 2
    {"x": 100, "y": 200, "width": 20, "height": 20},  # Spike 3
]

# Define the power-ups for each level
power_ups_level_1 = [
    {"x": 250, "y": 150, "width": 20, "height": 20, "type": "coin"},  # Coin 1
    {"x": 450, "y": 50, "width": 20, "height": 20, "type": "speed"},  # Speed Boost
]

power_ups_level_2 = [
    {"x": 100, "y": 300, "width": 20, "height": 20, "type": "coin"},  # Coin 1
    {"x": 450, "y": 50, "width": 20, "height": 20, "type": "invincibility"},  # Invincibility
    {"x": 250, "y": 100, "width": 20, "height": 20, "type": "coin"},  # Coin 3
]

power_ups_level_3 = [
    {"x": 250, "y": 100, "width": 20, "height": 20, "type": "coin"},  # Coin 1
    {"x": 450, "y": 50, "width": 20, "height": 20, "type": "speed"},  # Speed Boost
]

# Define the game states
INTRO = 0
RULES = 1
MENU = 2
PLAYING = 3
GAME_OVER = 4
WIN = 5

# Initialize the score
score = 0
font = pygame.font.SysFont(None, 36)

# Initialize the current level
current_level = 1
game_state = INTRO

# Initialize power-up effects
speed_boost_active = False
invincibility_active = False
power_up_timer = 0

# Function to display the score
def display_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

# Function to display end game message
def display_end_game_message(message):
    end_text = font.render(message, True, WHITE)
    screen.blit(end_text, (screen_width // 2 - end_text.get_width() // 2, screen_height // 2 - end_text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(3000)

# Function to display the rules
def display_rules():
    rules_text = [
        "Rules of the Game:",
        "1. Use LEFT and RIGHT arrows to move.",
        "2. Press SPACE to jump.",
        "3. Press 'G' to switch gravity.",
        "4. Collect coins for points.",
        "5. Avoid obstacles.",
        "6. Reach the end of each level to win.",
        "Press any key to start playing..."
    ]
    y_offset = 100
    for line in rules_text:
        text_surface = font.render(line, True, WHITE)
        screen.blit(text_surface, (screen_width // 2 - text_surface.get_width() // 2, y_offset))
        y_offset += 40

# Function to display the intro
def display_intro():
    screen.blit(intro_background, (0, 0))
    screen.blit(kangaroo_image, (screen_width // 2 - kangaroo_image.get_width() // 2, screen_height // 2 - kangaroo_image.get_height() // 2))
    intro_text = [
        "Hello! This is Shiro the Kangaroo! I want to go home,",
        "but I can only go if I win this game! Pls help me!!",
        "Press any key to continue..."
    ]
    y_offset = screen_height // 2 + kangaroo_image.get_height() // 2 + 20
    for line in intro_text:
        text_surface = font.render(line, True, WHITE)
        screen.blit(text_surface, (screen_width // 2 - text_surface.get_width() // 2, y_offset))
        y_offset += 40

# Function to reset the game to the initial state
def reset_game():
    global player_x, player_y, player_velocity_y, player_is_jumping, gravity_direction, current_level, score, speed_boost_active, invincibility_active, power_up_timer
    player_x = 100
    player_y = 100
    player_velocity_y = 0
    player_is_jumping = False
    gravity_direction = 1
    current_level = 1
    score = 0
    speed_boost_active = False
    invincibility_active = False
    power_up_timer = 0
    pygame.mixer.music.play(-1)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if game_state == INTRO:
                game_state = RULES
            elif game_state == RULES:
                game_state = MENU
            elif game_state == MENU:
                if event.key == pygame.K_RETURN:
                    game_state = PLAYING
                    start_game_sound.play()
            elif game_state == GAME_OVER or game_state == WIN:
                reset_game()
                game_state = MENU
            elif game_state == PLAYING:
                if event.key == pygame.K_SPACE and not player_is_jumping:
                    player_velocity_y = player_jump_speed * gravity_direction
                    player_is_jumping = True
                    jump_sound.play()
                if event.key == pygame.K_g:
                    gravity_direction *= -1
                    player_velocity_y *= -1

    # Game logic and rendering based on the current game state
    if game_state == INTRO:
        display_intro()
    elif game_state == RULES:
        screen.fill(BLACK)
        display_rules()
    elif game_state == MENU:
        screen.fill(BLACK)
        menu_text = font.render("Press ENTER to Start", True, WHITE)
        screen.blit(menu_text, (screen_width // 2 - menu_text.get_width() // 2, screen_height // 2 - menu_text.get_height() // 2))
    elif game_state == PLAYING:
        screen.blit(current_level_background, (0, 0))

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed

        # Gravity effect
        player_velocity_y += player_gravity * gravity_direction
        player_y += player_velocity_y

        # Check for collisions with platforms
        platforms = []
        obstacles = []
        power_ups = []
        if current_level == 1:
            platforms = platforms_level_1
            obstacles = obstacles_level_1
            power_ups = power_ups_level_1
        elif current_level == 2:
            platforms = platforms_level_2
            obstacles = obstacles_level_2
            power_ups = power_ups_level_2
        elif current_level == 3:
            platforms = platforms_level_3
            obstacles = obstacles_level_3
            power_ups = power_ups_level_3

        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        on_ground = False

        for platform in platforms:
            platform_rect = pygame.Rect(platform["x"], platform["y"], platform["width"], platform["height"])
            if player_rect.colliderect(platform_rect):
                if gravity_direction == 1 and player_velocity_y > 0:
                    player_y = platform["y"] - player_height
                    player_velocity_y = 0
                    player_is_jumping = False
                    on_ground = True
                elif gravity_direction == -1 and player_velocity_y < 0:
                    player_y = platform["y"] + platform["height"]
                    player_velocity_y = 0
                    player_is_jumping = False
                    on_ground = True

            if platform.get("moving"):
                platform["x"] += platform["speed"] * platform["direction"]
                if abs(platform["x"] - platform["original_x"]) > platform["range"]:
                    platform["direction"] *= -1

        # Check for collisions with obstacles
        for obstacle in obstacles:
            obstacle_rect = pygame.Rect(obstacle["x"], obstacle["y"], obstacle["width"], obstacle["height"])
            if player_rect.colliderect(obstacle_rect):
                if not invincibility_active:
                    game_over_sound.play()
                    game_state = GAME_OVER

        # Check for collisions with power-ups
        for power_up in power_ups:
            power_up_rect = pygame.Rect(power_up["x"], power_up["y"], power_up["width"], power_up["height"])
            if player_rect.colliderect(power_up_rect):
                if power_up["type"] == "coin":
                    point_sound.play()
                    score += 10
                elif power_up["type"] == "speed":
                    speed_boost_active = True
                    player_speed *= 2
                elif power_up["type"] == "invincibility":
                    invincibility_active = True
                power_ups.remove(power_up)

        if not on_ground:
            if gravity_direction == 1:
                if player_y > screen_height:
                    game_over_sound.play()
                    game_state = GAME_OVER
            elif gravity_direction == -1:
                if player_y < 0:
                    game_over_sound.play()
                    game_state = GAME_OVER

        # Check if player reached the right side of the screen and collected all power-ups
        if player_x + player_width > screen_width and len(power_ups) == 0:
            level_up_sound.play()
            current_level += 1
            if current_level > 3:
                game_state = WIN
            else:
                current_level_background = backgrounds[current_level - 1]
                player_x = 0
                player_y = 100
                player_velocity_y = 0
                player_is_jumping = False
                gravity_direction = 1

        # Draw the player
        screen.blit(player_image, (player_x, player_y))

        # Draw the platforms
        for platform in platforms:
            pygame.draw.rect(screen, GREEN, (platform["x"], platform["y"], platform["width"], platform["height"]))

        # Draw the obstacles
        for obstacle in obstacles:
            pygame.draw.rect(screen, RED, (obstacle["x"], obstacle["y"], obstacle["width"], obstacle["height"]))

        # Draw the power-ups
        for power_up in power_ups:
            color = YELLOW if power_up["type"] == "coin" else WHITE
            pygame.draw.rect(screen, color, (power_up["x"], power_up["y"], power_up["width"], power_up["height"]))

        display_score()

    elif game_state == GAME_OVER:
        screen.fill(BLACK)
        display_end_game_message("Game Over! Press any key to restart.")
    elif game_state == WIN:
        screen.fill(BLACK)
        display_end_game_message("Shiro has reached home!Press any key to restart.")

    pygame.display.flip()
    pygame.time.Clock().tick(30)

