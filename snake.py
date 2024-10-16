# Importing libraries
import pygame
import random

# Constants
snake_speed = 8
window_x = 720
window_y = 480
grid_size_x = 24  # Number of squares horizontally
grid_size_y = 16  # Number of squares vertically
square_size = min(window_x // grid_size_x, window_y // grid_size_y)  # Calculate square size dynamically

# Defining colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
dark_green = pygame.Color(0, 155, 0)
gray = pygame.Color(200, 200, 200)

# Define a function to get adjusted green color
def adjusted_green_color(index):
    adjustedGreen = 165 + (index * 5)
    if adjustedGreen > 255:
        adjustedGreen = 255
    return pygame.Color(0, adjustedGreen, 0)

# Initialize pygame
pygame.init()

# Initialize game window
pygame.display.set_caption('Simple Snake')
game_window = pygame.display.set_mode((window_x, window_y + 40))  # Additional space for the white bar

# FPS (frames per second) controller
fps = pygame.time.Clock()

# Initial game setup
highscore = 0

# Restart the game setup
def restart_game():
    starting_x = 10 * square_size
    starting_y = 8 * square_size

    global snake_position, snake_body, fruit_position, fruit_spawn, direction, change_to, score
    snake_position = [starting_x, starting_y]
    snake_body = [[starting_x, starting_y], [starting_x - square_size, starting_y], [starting_x - (2 * square_size), starting_y]]
    fruit_position = [random.randrange(1, (window_x // square_size)) * square_size,
                      random.randrange(1, (window_y // square_size)) * square_size]
    fruit_spawn = True
    direction = 'RIGHT'
    change_to = direction
    score = 0

# Start with the initial game state
restart_game()

# Displaying Score function in the white bar
def show_score(color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score: ' + str(score), True, color)
    game_window.blit(score_surface, (10, window_y + 10))

# Displaying Highscore function in the white bar
def show_highscore(color, font, size):
    highscore_font = pygame.font.SysFont(font, size)
    highscore_surface = highscore_font.render("Highscore: " + str(highscore), True, color)
    game_window.blit(highscore_surface, (window_x - 150, window_y + 10))

# Game over function with restart button and white background
def game_over():
    global highscore
    
    if score > highscore:
        highscore = score

    # White background for the restart button
    pygame.draw.rect(game_window, white, pygame.Rect((window_x / 2) - 300, (window_y / 2) - 200, 600, 400))

    # Display Game Over score
    my_font = pygame.font.SysFont('Arial', 50)
    game_over_surface = my_font.render(f"Your Score: {score}", True, black)
    game_over_rect = game_over_surface.get_rect(center=(window_x / 2, (window_y / 2) - 100))
    game_window.blit(game_over_surface, game_over_rect)

    # Display Highscore
    highscore_surface = my_font.render(f"Highscore: {highscore}", True, black)
    highscore_rect = highscore_surface.get_rect(center=(window_x / 2, (window_y / 2) - 30))
    game_window.blit(highscore_surface, highscore_rect)

    # Create a restart button
    button_font = pygame.font.SysFont('Arial', 30)
    restart_surface = button_font.render('Restart', True, black)
    restart_rect = pygame.Rect((window_x / 2) - 70, (window_y / 2) + 40, 140, 80)
    pygame.draw.rect(game_window, gray, restart_rect)
    game_window.blit(restart_surface, ((window_x / 2) - 48, (window_y / 2) + 60))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rect.collidepoint(event.pos):
                    restart_game()

                    return  # Exit the game_over loop and restart the game

# Main Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                change_to = 'UP'

            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                change_to = 'DOWN'

            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                change_to = 'LEFT'

            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'

    # Ensure the snake cannot move in the opposite direction
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'

    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'

    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'

    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Move the snake
    if direction == 'UP':
        snake_position[1] -= square_size

    if direction == 'DOWN':
        snake_position[1] += square_size

    if direction == 'LEFT':
        snake_position[0] -= square_size

    if direction == 'RIGHT':
        snake_position[0] += square_size

    # Snake body growing mechanism
    snake_body.insert(0, list(snake_position))
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
        score += 1

        if score > highscore:
            highscore = score

        fruit_spawn = False

    else:
        snake_body.pop()

    if not fruit_spawn:
        fruit_position = [random.randrange(1, (window_x // square_size)) * square_size,
                          random.randrange(1, (window_y // square_size)) * square_size]
        
    fruit_spawn = True

    # Fill the grid background with white (play area)
    game_window.fill(white)
    for x in range(0, window_x, square_size):
        for y in range(0, window_y, square_size):
            pygame.draw.rect(game_window, gray, pygame.Rect(x, y, square_size, square_size), 1)

    # Draw the snake
    for i, pos in enumerate(snake_body):
        color = dark_green if i == 0 else adjusted_green_color(i)  # Darker color for the head
        pygame.draw.rect(game_window, color, pygame.Rect(pos[0], pos[1], square_size, square_size))

    # Draw the fruit
    pygame.draw.rect(game_window, red, pygame.Rect(fruit_position[0], fruit_position[1], square_size, square_size))

    # Draw the white bar above the play area for the score and highscore
    pygame.draw.rect(game_window, white, pygame.Rect(0, window_y, window_x, 40))
    pygame.draw.line(game_window, black, (0, window_y), (window_x, window_y), 2)

    # Display score and highscore in the white bar
    show_score(black, 'Arial', 20)
    show_highscore(black, 'Arial', 20)

    # Game Over conditions (you can enable the wrap-around by commenting these lines)
    if snake_position[0] < 0 or snake_position[0] > window_x - square_size or snake_position[1] < 0 or snake_position[1] > window_y - square_size:
        game_over()

    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()

    # Update display
    pygame.display.update()

    # Control the frame rate
    fps.tick(snake_speed)
