import pygame
import sys
from tkinter import *
from tkinter import messagebox

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Create a Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("D:/Wasir's Project/Space Ship Game/spaceship.png")
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2 - self.rect.width // 2
        self.rect.y = HEIGHT - self.rect.height - 20

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spaceship Game")

# Set initial player speed
player_speed = 5

# Create a clock object to control the frame rate
clock = pygame.time.Clock()

# Create a group for bullets and player
bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

# Create a player object
player = Player()
all_sprites.add(player)

# Create a function to handle game over
def game_over():
    messagebox.showinfo("Game Over", "Your spaceship was destroyed!")
    pygame.quit()
    sys.exit()

# Main game loop
def game_loop():
    global player

    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Create a bullet and add it to the group
                    bullet = pygame.Rect(player.rect.centerx - 2, player.rect.top - 10, 4, 10)
                    bullets.add(bullet)

        # Move the player
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.rect.x > 0:
            player.rect.x -= player_speed
        if keys[pygame.K_RIGHT] and player.rect.x < WIDTH - player.rect.width:
            player.rect.x += player_speed

        # Move the bullets
        bullets.update()

        # Remove bullets that go off-screen
        for bullet in bullets.copy():
            if bullet.bottom < 0:
                bullets.remove(bullet)

        # Check for collision with player and bullets
        if pygame.sprite.spritecollide(player, bullets, True):
            game_over()

        # Draw everything
        screen.fill(BLACK)
        all_sprites.draw(screen)

        # Draw bullets
        for bullet in bullets:
            pygame.draw.rect(screen, WHITE, bullet)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)

# Create a Tkinter window
root = Tk()
root.title("Spaceship Game")

# Create a button to start the game
start_button = Button(root, text="Start Game", command=game_loop)
start_button.pack(pady=20)

# Run the Tkinter main loop
root.mainloop()
