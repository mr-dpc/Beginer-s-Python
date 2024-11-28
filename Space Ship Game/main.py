import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)

# Load images (using relative paths)
player_image = pygame.image.load("D:/Wasir's Project/Space Ship Game/spaceship.png")
enemy_image = pygame.image.load("D:/Wasir's Project/Space Ship Game/enemy.png")
villain_image = pygame.image.load("D:/Wasir's Project/Space Ship Game/renemy.png")
bullet_image = pygame.image.load("D:/Wasir's Project/Space Ship Game/bullet.png")

# Player spaceship
player_size = 50
player_speed = 5
player_rect = player_image.get_rect()
player_rect.center = (WIDTH // 2, HEIGHT - 2 * player_size)

# Enemy spaceship
enemy_size = 50
enemy_speed = 3
enemies = []

# Villain spaceship
villain_size = 100
villain_speed = 2
villain_rect = villain_image.get_rect()
villain_rect.center = (WIDTH // 2, 50)

# Bullet
bullet_speed = 7
bullets = []

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Space Ship Game")
clock = pygame.time.Clock()

# Function to handle events
def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                fire_bullet()

# Function to move the player
def move_player():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.left - player_speed > 0:
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT] and player_rect.right + player_speed < WIDTH:
        player_rect.x += player_speed
    if keys[pygame.K_UP] and player_rect.top - player_speed > 0:
        player_rect.y -= player_speed
    if keys[pygame.K_DOWN] and player_rect.bottom + player_speed < HEIGHT:
        player_rect.y += player_speed

# Function to generate enemies
def generate_enemies():
    enemy_rect = enemy_image.get_rect()
    for _ in range(5):  # Adjust the number of enemies as needed
        enemy_rect.x = random.randint(0, WIDTH - enemy_size)
        enemy_rect.y = random.randint(0, HEIGHT - enemy_size)
        enemies.append(enemy_rect.copy())

# Function to move enemies
def move_enemies():
    for enemy in enemies:
        enemy.y += enemy_speed
        if enemy.y > HEIGHT:
            enemy.y = 0
            enemy.x = random.randint(0, WIDTH - enemy_size)

# Function to move the villain
def move_villain():
    global villain_speed
    villain_rect.x += villain_speed
    if villain_rect.left <= 0 or villain_rect.right >= WIDTH:
        villain_speed = -villain_speed

# Function to move bullets
def move_bullets():
    for bullet in bullets:
        bullet.y -= bullet_speed
        if bullet.y < 0:
            bullets.remove(bullet)

# Function to check collisions
def check_collisions():
    # Check collisions between player and enemies
    for enemy in enemies:
        if player_rect.colliderect(enemy):
            game_over()

    # Check collision between player and villain
    if player_rect.colliderect(villain_rect):
        you_win()

# Function to handle game over
def game_over():
    print("Game Over!")
    pygame.quit()
    sys.exit()

# Function to handle victory
def you_win():
    print("You Win!")
    pygame.quit()
    sys.exit()

# Function to fire a bullet
def fire_bullet():
    bullet_rect = bullet_image.get_rect()
    bullet_rect.center = player_rect.center
    bullets.append(bullet_rect)

# Main game loop
generate_enemies()  # Call the function to generate enemies at the start

while True:
    handle_events()
    move_player()
    move_enemies()
    move_villain()
    move_bullets()
    check_collisions()

    # Draw everything
    screen.fill(WHITE)
    screen.blit(player_image, player_rect)
    screen.blit(villain_image, villain_rect)
    for enemy in enemies:
        screen.blit(enemy_image, enemy)
    for bullet in bullets:
        screen.blit(bullet_image, bullet)

    pygame.display.flip()
    clock.tick(FPS)
