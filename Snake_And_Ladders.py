# Full Name: Reshma Sri Murakonda
# Student Number: 101282055

import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Constants
BOARD_COLS, BOARD_ROWS = 10, 10  # 100 squares
SQUARE_SIZE = 60
BOARD_WIDTH = BOARD_COLS * SQUARE_SIZE
BOARD_HEIGHT = BOARD_ROWS * SQUARE_SIZE
INFO_WIDTH = 300
WIDTH, HEIGHT = BOARD_WIDTH + INFO_WIDTH, BOARD_HEIGHT
FPS = 30
DICE_SIZE = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snakes and Ladders")
clock = pygame.time.Clock()

# Load the board image
board_image = pygame.image.load('S.jpg')  # Make sure 'S.png' is in the same directory
board_image = pygame.transform.scale(board_image, (BOARD_WIDTH, BOARD_HEIGHT))

# Game elements
snakes = {30: 7, 47: 15, 56: 19, 73: 51, 82: 42, 92: 75, 98: 55}
ladders = {4: 25, 21: 39, 29: 74, 43: 76, 63: 80, 71: 89}

# Function to draw the board
def draw_board():
    screen.blit(board_image, (0, 0))

# Function to draw players
def draw_players(pos1, pos2):
    for pos, color in [(pos1, RED), (pos2, BLUE)]:
        x = (pos - 1) % BOARD_COLS
        y = BOARD_ROWS - 1 - (pos - 1) // BOARD_COLS
        pygame.draw.circle(screen, color, (x * SQUARE_SIZE + SQUARE_SIZE // 2, y * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 3)

# Function to display player info
def display_player_info(player, pos, roll):
    font = pygame.font.Font(None, 30)
    color = RED if player == 1 else BLUE
    y_offset = 10 if player == 1 else HEIGHT // 2
    
    pygame.draw.rect(screen, GRAY, (BOARD_WIDTH, y_offset, INFO_WIDTH, HEIGHT // 2 - 10))
    
    text = font.render(f"Player {player}", True, color)
    screen.blit(text, (BOARD_WIDTH + 10, y_offset + 10))
    
    text = font.render(f"Position: {pos}", True, BLACK)
    screen.blit(text, (BOARD_WIDTH + 10, y_offset + 50))
    
    text = font.render(f"Last Roll: {roll}", True, BLACK)
    screen.blit(text, (BOARD_WIDTH + 10, y_offset + 90))

# Function to draw a single die
def draw_die(value, x, y):
    pygame.draw.rect(screen, WHITE, (x, y, DICE_SIZE, DICE_SIZE))
    pygame.draw.rect(screen, BLACK, (x, y, DICE_SIZE, DICE_SIZE), 2)
    
    dot_radius = 5
    dot_positions = {
        1: [(0, 0)],
        2: [(-1, -1), (1, 1)],
        3: [(-1, -1), (0, 0), (1, 1)],
        4: [(-1, -1), (-1, 1), (1, -1), (1, 1)],
        5: [(-1, -1), (-1, 1), (0, 0), (1, -1), (1, 1)],
        6: [(-1, -1), (-1, 0), (-1, 1), (1, -1), (1, 0), (1, 1)]
    }
    
    for dx, dy in dot_positions[value]:
        cx = x + DICE_SIZE // 2 + dx * (DICE_SIZE // 4)
        cy = y + DICE_SIZE // 2 + dy * (DICE_SIZE // 4)
        pygame.draw.circle(screen, BLACK, (cx, cy), dot_radius)

# Function to draw dice
def draw_dice(dice1, dice2, player):
    x_offset = BOARD_WIDTH + 10
    y_offset = 150 if player == 1 else HEIGHT // 2 + 140
    
    draw_die(dice1, x_offset, y_offset)
    draw_die(dice2, x_offset + DICE_SIZE + 10, y_offset)

# Main game loop
def game_loop():
    player1_pos = 1
    player2_pos = 1
    player1_roll = 0
    player2_roll = 0
    current_player = 1

    while player1_pos < 100 and player2_pos < 100:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill(WHITE)
        draw_board()

        # Roll dice
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
        roll = dice1 + dice2
        
        # Move player
        if current_player == 1:
            player1_pos = min(player1_pos + roll, 100)
            if player1_pos in snakes:
                player1_pos = snakes[player1_pos]
            elif player1_pos in ladders:
                player1_pos = ladders[player1_pos]
            player1_roll = roll
        else:
            player2_pos = min(player2_pos + roll, 100)
            if player2_pos in snakes:
                player2_pos = snakes[player2_pos]
            elif player2_pos in ladders:
                player2_pos = ladders[player2_pos]
            player2_roll = roll

        draw_players(player1_pos, player2_pos)
        display_player_info(1, player1_pos, player1_roll)
        display_player_info(2, player2_pos, player2_roll)
        draw_dice(dice1, dice2, current_player)

        pygame.display.flip()
        clock.tick(FPS)
        time.sleep(1)  # Pause to show each move

        current_player = 3 - current_player  # Switch players (1 -> 2, 2 -> 1)

    # Game over
    font = pygame.font.Font(None, 72)
    winner = 1 if player1_pos >= 100 else 2
    text = font.render(f"Player {winner} wins!", True, GREEN)
    screen.blit(text, (BOARD_WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    time.sleep(3)

# Run the game
game_loop()
pygame.quit()