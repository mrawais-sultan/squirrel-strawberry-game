import pygame
import random
import time

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
FPS = 60
KOALA_SIZE = 40
STRAWBERRY_SIZE = 40
SQUIRREL_SIZE = 40
SPAWN_TIME_STRAWBERRY = 1000  # in milliseconds
SPAWN_TIME_SQUIRREL = 3000  # in milliseconds
DARK_BG_COLOR = (30, 30, 30)
RETRO_TEXT_COLOR = (255, 200, 0)

# Load images
koala_img = pygame.transform.scale(pygame.image.load("koala.png"), (KOALA_SIZE, KOALA_SIZE))
strawberry_img = pygame.transform.scale(pygame.image.load("strawberry.png"), (STRAWBERRY_SIZE, STRAWBERRY_SIZE))
squirrel_img = pygame.transform.scale(pygame.image.load("squirrel.png"), (SQUIRREL_SIZE, SQUIRREL_SIZE))

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Squirrel Finder")

# Clock and font
clock = pygame.time.Clock()
font = pygame.font.SysFont("Retro", 24)

# Timer and game states
game_over = False
start_time = None
game_started = False
winner = None

# Player and score tracking
players = []
current_player_idx = 0
scores = {}

# Helper functions
def input_players():
    """Function to input player names and set up the game."""
    global players, current_player_idx, scores
    screen.fill(DARK_BG_COLOR)
    
    # Instructions for entering number of players
    instructions = "Enter number of players (1-4):"
    input_text = ''
    active = True
    
    while active:
        screen.fill(DARK_BG_COLOR)
        text_surface = font.render(instructions, True, RETRO_TEXT_COLOR)
        screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT // 4))
        
        # Display current input for the number of players
        input_surface = font.render(input_text, True, RETRO_TEXT_COLOR)
        screen.blit(input_surface, (WIDTH // 2 - input_surface.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    try:
                        num_players = int(input_text)
                        if 1 <= num_players <= 4:
                            active = False
                        else:
                            instructions = "Please enter a valid number between 1 and 4:"
                    except ValueError:
                        instructions = "Invalid input. Enter a number (1-4):"
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

    # Input player names
    for i in range(num_players):
        name = ''
        active = True
        instructions = f"Enter name for Player {i + 1}:"
        
        while active:
            screen.fill(DARK_BG_COLOR)
            name_prompt_surface = font.render(instructions, True, RETRO_TEXT_COLOR)
            screen.blit(name_prompt_surface, (WIDTH // 2 - name_prompt_surface.get_width() // 2, HEIGHT // 4))
            
            name_input_surface = font.render(name, True, RETRO_TEXT_COLOR)
            screen.blit(name_input_surface, (WIDTH // 2 - name_input_surface.get_width() // 2, HEIGHT // 2))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and name:
                        players.append(name)
                        scores[name] = 0
                        active = False
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        name += event.unicode

def show_instructions():
    screen.fill(DARK_BG_COLOR)
    instructions = [
        "Welcome to Squirrel Finder!",
        "You are the koala. Move with arrow keys.",
        "Avoid the bouncing strawberry!",
        "Touch the squirrel to win!",
        "Press any key to start."
    ]
    y_offset = 100
    for line in instructions:
        text = font.render(line, True, RETRO_TEXT_COLOR)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y_offset))
        y_offset += 40
    pygame.display.flip()

def reset_game():
    global koala_rect, strawberry_rect, squirrel_rect, strawberry_spawned, squirrel_spawned, start_time, game_over, game_started, winner, current_player_idx

    # Koala (player)
    koala_rect = koala_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    # Strawberry and Squirrel
    strawberry_rect = None
    squirrel_rect = None

    strawberry_spawned = False
    squirrel_spawned = False

    # Reset timer
    start_time = pygame.time.get_ticks()
    game_over = False
    game_started = True
    winner = None

def move_bouncing_icon(rect, speed):
    rect.x += speed[0]
    rect.y += speed[1]

    if rect.left <= 0 or rect.right >= WIDTH:
        speed[0] = -speed[0]
    if rect.top <= 0 or rect.bottom >= HEIGHT:
        speed[1] = -speed[1]
    return speed

def display_game_over_message():
    screen.fill(DARK_BG_COLOR)
    if winner == "win":
        message = f"{players[current_player_idx]} found the squirrel! They win!"
        scores[players[current_player_idx]] += 1
    elif winner == "lose":
        message = f"{players[current_player_idx]} hit the strawberry! Game over!"
    
    game_over_text = font.render(message, True, RETRO_TEXT_COLOR)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    time.sleep(2)  # Pause for 2 seconds before resetting the game

def display_scores():
    """Display the current scores."""
    y_offset = 30
    for player, score in scores.items():
        score_text = font.render(f"{player}: {score} points", True, RETRO_TEXT_COLOR)
        screen.blit(score_text, (10, y_offset))
        y_offset += 30

# Main game loop
input_players()  # Input player names
running = True
reset_game()

while running:
    clock.tick(FPS)
    screen.fill(DARK_BG_COLOR)

    # Display timer
    if game_started and not game_over:
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        timer_text = font.render(f"Time: {elapsed_time}", True, RETRO_TEXT_COLOR)
        screen.blit(timer_text, (10, 10))

    # Display player scores
    display_scores()

    # Display current player turn
    current_player_text = font.render(f"Player Turn: {players[current_player_idx]}", True, RETRO_TEXT_COLOR)
    screen.blit(current_player_text, (WIDTH // 2 - current_player_text.get_width() // 2, HEIGHT - 50))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and not game_started:
            reset_game()

    if not game_started:
        show_instructions()
        continue

    # Koala Movement
    keys = pygame.key.get_pressed()
    koala_speed = 5
    if keys[pygame.K_LEFT]:
        koala_rect.x -= koala_speed
    if keys[pygame.K_RIGHT]:
        koala_rect.x += koala_speed
    if keys[pygame.K_UP]:
        koala_rect.y -= koala_speed
    if keys[pygame.K_DOWN]:
        koala_rect.y += koala_speed

    # Keep koala within screen bounds
    koala_rect.clamp_ip(screen.get_rect())

    # Spawn strawberry after 1 second
    if not strawberry_spawned and pygame.time.get_ticks() - start_time >= SPAWN_TIME_STRAWBERRY:
        strawberry_spawned = True
        strawberry_rect = strawberry_img.get_rect(center=(random.randint(40, WIDTH - 40), random.randint(40, HEIGHT - 40)))
        strawberry_speed = [random.choice([-3, 3]), random.choice([-3, 3])]

    # Move and display strawberry
    if strawberry_spawned:
        strawberry_speed = move_bouncing_icon(strawberry_rect, strawberry_speed)
        screen.blit(strawberry_img, strawberry_rect)

    # Spawn squirrel after 3 seconds
    if not squirrel_spawned and pygame.time.get_ticks() - start_time >= SPAWN_TIME_SQUIRREL:
        squirrel_spawned = True
        squirrel_rect = squirrel_img.get_rect(center=(random.randint(40, WIDTH - 40), random.randint(40, HEIGHT - 40)))
        squirrel_speed = [random.choice([-2, 2]), random.choice([-2, 2])]

    # Move and display squirrel
    if squirrel_spawned:
        squirrel_speed = move_bouncing_icon(squirrel_rect, squirrel_speed)
        screen.blit(squirrel_img, squirrel_rect)

    # Check for collisions
    if strawberry_spawned and koala_rect.colliderect(strawberry_rect):
        game_over = True
        winner = "lose"
        display_game_over_message()
        current_player_idx = (current_player_idx + 1) % len(players)  # Switch to the next player
        reset_game()

    if squirrel_spawned and koala_rect.colliderect(squirrel_rect):
        game_over = True
        winner = "win"
        display_game_over_message()
        current_player_idx = (current_player_idx + 1) % len(players)  # Switch to the next player
        reset_game()

    # Display koala
    screen.blit(koala_img, koala_rect)

    pygame.display.flip()

pygame.quit()
