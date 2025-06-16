import pygame
import sys

# Initialize Pygame
pygame.init()

# Set the screen dimensions
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the title of the window
pygame.display.set_caption("Platformer Game")

# Load the background images for each level
backgrounds = [
    pygame.image.load('background_india.png').convert(),  # Level 1 background image
    pygame.image.load('background_paris.png').convert()   # Level 2 background image
]

# Scale background images to fit the screen
backgrounds[0] = pygame.transform.scale(backgrounds[0], (screen_width, screen_height))
backgrounds[1] = pygame.transform.scale(backgrounds[1], (screen_width, screen_height))

# Initialize the current level background
current_level_background = backgrounds[0]

# Load the background music
pygame.mixer.music.load('background_music1.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Load sound effects
jump_sound = pygame.mixer.Sound('jump.wav')
point_sound = pygame.mixer.Sound('point.wav')

# Define some colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Define the player character
player_width = 30
player_height = 30
player_x = 100
player_y = 100
player_speed = 5
player_gravity = 0.5
player_jump_speed = -15
player_velocity_y = 0
player_is_jumping = False

# Define the platforms for level 1
platforms_level_1 = [
    {"x": 0, "y": 400, "width": 640, "height": 20, "moving": False},  # Ground
    {"x": 200, "y": 300, "width": 100, "height": 20, "moving": False},  # Platform 1
    {"x": 400, "y": 200, "width": 100, "height": 20, "moving": True, "direction": 1, "range": 150, "speed": 2},
    # Moving Platform
]

# Define the obstacles for level 1
obstacles_level_1 = [
    {"x": 300, "y": 250, "width": 20, "height": 20},  # Spike 1
    {"x": 500, "y": 350, "width": 20, "height": 20},  # Spike 2
]

# Define the power-ups for level 1
power_ups_level_1 = [
    {"x": 250, "y": 150, "width": 20, "height": 20, "type": "coin"},  # Coin 1
    {"x": 450, "y": 50, "width": 20, "height": 20, "type": "speed"},  # Speed Boost
]

# Define the platforms for level 2
platforms_level_2 = [
    {"x": 0, "y": 400, "width": 640, "height": 20, "moving": False},  # Ground
    {"x": 150, "y": 350, "width": 100, "height": 20, "moving": True, "direction": 1, "range": 200, "speed": 3},
    # Moving Platform 1
    {"x": 350, "y": 250, "width": 100, "height": 20, "moving": False},  # Platform 2
    {"x": 550, "y": 150, "width": 100, "height": 20, "moving": True, "direction": -1, "range": 150, "speed": 2},
    # Moving Platform 2
]

# Define the obstacles for level 2
obstacles_level_2 = [
    {"x": 300, "y": 250, "width": 20, "height": 20},  # Spike 1
    {"x": 500, "y": 350, "width": 20, "height": 20},  # Spike 2
    {"x": 400, "y": 300, "width": 20, "height": 20},  # Spike 3
]

# Define the power-ups for level 2
power_ups_level_2 = [
    {"x": 100, "y": 300, "width": 20, "height": 20, "type": "coin"},  # Coin 1
    {"x": 450, "y": 50, "width": 20, "height": 20, "type": "invincibility"},  # Invincibility
    {"x": 250, "y": 100, "width": 20, "height": 20, "type": "coin"},  # Coin 3
]

# Initialize the score
score = 0
font = pygame.font.SysFont(None, 36)

# Initialize the current level
current_level = 1
game_over = False
win = False

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
    screen.blit(end_text,
                (screen_width // 2 - end_text.get_width() // 2, screen_height // 2 - end_text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(3000)


# Function to show the start screen
def show_start_screen():
    screen.fill((0, 0, 0))
    title_text = font.render("Platformer Game", True, WHITE)
    start_text = font.render("Press Enter to Start", True, WHITE)
    screen.blit(title_text, (
        screen_width // 2 - title_text.get_width() // 2, screen_height // 2 - title_text.get_height() // 2 - 20))
    screen.blit(start_text, (
        screen_width // 2 - start_text.get_width() // 2, screen_height // 2 - start_text.get_height() // 2 + 20))
    pygame.display.flip()


# Game loop
start_screen = True
while True:
    if start_screen:
        show_start_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    start_screen = False
    else:
        if game_over or win:
            if game_over:
                display_end_game_message("Game Over!")
            else:
                display_end_game_message("You Win!")
            pygame.quit()
            sys.exit()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not player_is_jumping:
                    player_velocity_y = player_jump_speed
                    player_is_jumping = True
                    jump_sound.play()  # Play jump sound effect

        # Move the player
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed

        # Apply gravity
        player_velocity_y += player_gravity
        player_y += player_velocity_y

        # Set the current level's platforms, obstacles, and power-ups
        if current_level == 1:
            platforms = platforms_level_1
            obstacles = obstacles_level_1
            power_ups = power_ups_level_1
            current_level_background = backgrounds[0]  # Set level 1 background
        else:
            platforms = platforms_level_2
            obstacles = obstacles_level_2
            power_ups = power_ups_level_2
            current_level_background = backgrounds[1]  # Set level 2 background

        # Update moving platforms
        for platform in platforms:
            if platform["moving"]:
                platform["x"] += platform["speed"] * platform["direction"]
                if platform["x"] <= 0 or platform["x"] + platform["width"] >= screen_width:
                    platform["direction"] *= -1

        # Check for collisions with platforms
        for platform in platforms:
            if (player_x + player_width > platform["x"] and
                    player_x < platform["x"] + platform["width"] and
                    player_y + player_height > platform["y"] and
                    player_y < platform["y"] + platform["height"]):
                player_y = platform["y"] - player_height
                player_velocity_y = 0
                player_is_jumping = False

        # Check for collisions with obstacles
        for obstacle in obstacles:
            if (player_x + player_width > obstacle["x"] and
                    player_x < obstacle["x"] + obstacle["width"] and
                    player_y + player_height > obstacle["y"] and
                    player_y < obstacle["y"] + obstacle["height"]):
                if not invincibility_active:
                    game_over = True

        # Check for collisions with power-ups
        for power_up in power_ups:
            if (player_x + player_width > power_up["x"] and
                    player_x < power_up["x"] + power_up["width"] and
                    player_y + player_height > power_up["y"] and
                    player_y < power_up["y"] + power_up["height"]):
                power_ups.remove(power_up)
                if power_up["type"] == "coin":
                    score += 10
                    point_sound.play()  # Play point sound effect
                elif power_up["type"] == "speed":
                    speed_boost_active = True
                    player_speed = 10
                    power_up_timer = pygame.time.get_ticks() + 5000  # 5 seconds duration
                elif power_up["type"] == "invincibility":
                    invincibility_active = True
                    power_up_timer = pygame.time.get_ticks() + 5000  # 5 seconds duration

        # Check if power-up effects should expire
        if speed_boost_active and pygame.time.get_ticks() > power_up_timer:
            speed_boost_active = False
            player_speed = 5
        if invincibility_active and pygame.time.get_ticks() > power_up_timer:
            invincibility_active = False

        # Check if all power-ups are collected to advance to the next level
        if len(power_ups) == 0:
            current_level += 1
            if current_level > 2:
                win = True

        # Clear the screen
        screen.blit(current_level_background, (0, 0))

        # Draw the platforms
        for platform in platforms:
            pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(platform["x"], platform["y"], platform["width"], platform["height"]))

        # Draw the obstacles
        for obstacle in obstacles:
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(obstacle["x"], obstacle["y"], obstacle["width"], obstacle["height"]))

        # Draw the power-ups
        for power_up in power_ups:
            color = (255, 255, 255) if power_up["type"] == "coin" else (0, 0, 255)
            pygame.draw.rect(screen, color, pygame.Rect(power_up["x"], power_up["y"], power_up["width"], power_up["height"]))

        # Draw the player
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(player_x, player_y, player_width, player_height))

        # Display the score
        display_score()

        # Update the screen
        pygame.display.flip()

        # Cap the frame rate
        pygame.time.Clock().tick(60)

