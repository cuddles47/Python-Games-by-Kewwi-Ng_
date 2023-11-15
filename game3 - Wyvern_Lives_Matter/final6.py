import pygame
import sys
import random
import os

# Constants
WIDTH, HEIGHT = 1324,699
WYVERN_SPEED = 13
ARROW_LENGTH = 100
ARROW_SPEED = 14
SPAWN_PROBABILITY = 0.185

# Initialize pygame
pygame.init()

# Load images
head_image = pygame.image.load("Wyvern_Head_Left.png")
head_image = pygame.transform.scale(head_image, (100,36))

leg_image = pygame.image.load("Wyvern_Legs.png")
leg_image = pygame.transform.scale(leg_image, (50,54))

body1_image = pygame.image.load("Wyvern_Body.png")
body1_image = pygame.transform.scale(body1_image, (44,32))

body2_image = pygame.image.load("Wyvern_Body_2.png")
body2_image = pygame.transform.scale(body2_image, (44,28))

body3_image = pygame.image.load("Wyvern_Body_3.png")
body3_image = pygame.transform.scale(body3_image, (44,24))

tail_image = pygame.image.load("Wyvern_Tail.png")
tail_image = pygame.transform.scale(tail_image, (96,19))

arrow_image = pygame.image.load("arrow.png")
background_image = pygame.image.load("terraria_background.png")

# Create a list to store dragon segments
wyvern_segments = [head_image, leg_image, body1_image, body1_image, body1_image, leg_image, body2_image, body3_image, tail_image]

class Wyvern:
    def __init__(self):
        self.segments = []
        for i in range(len(dragon_segments)):
            self.segments.append((WIDTH // 2 - i * 2 * SEGMENT_SIZE, HEIGHT // 4))
        self.hitbox = pygame.Rect(
            self.segments[0][0] - SEGMENT_SIZE,
            self.segments[0][1] - SEGMENT_SIZE,
            2 * SEGMENT_SIZE * len(self.segments),
            2 * SEGMENT_SIZE,
        )

    def move(self):
        # Simulate a simple flying movement for the Wyvern
        self.segments[0] = (self.segments[0][0], self.segments[0][1] - DRAGON_SPEED // 2)

        # Update the hitbox position
        self.hitbox.topleft = (
            self.segments[0][0] - SEGMENT_SIZE,
            self.segments[0][1] - SEGMENT_SIZE,
        )

    def draw(self):
        for i, segment in enumerate(self.segments):
            screen.blit(dragon_segments[i], (segment[0] - SEGMENT_SIZE, segment[1] - SEGMENT_SIZE))


class Arrow:
    def __init__(self):
        self.x = 0
        self.y = random.randint(0, HEIGHT)
        self.image = arrow_image
        self.image_rect = self.image.get_rect()
        self.image_rect.topleft = (self.x, self.y - self.image_rect.height // 2)
        self.colliding = False

    def move(self):
        self.x += ARROW_SPEED
        self.image_rect.topleft = (self.x, self.y - self.image_rect.height // 2)

    def draw(self):
        screen.blit(self.image, self.image_rect)

    # Inside the Arrow class
    def check_collision(self, dragon_hitbox):
        if self.colliding:
            return False

        arrow_rect = pygame.Rect(
            self.x, self.y - self.image_rect.height // 2, self.image_rect.width, self.image_rect.height
        )

        if arrow_rect.colliderect(dragon_hitbox):
            self.colliding = True
            return True
        else:
            return False


# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dragon Dodge Arrows")

# Game variables
arrows = []
game_over = False
score = 0
high_score = 0
start_time = 0

if os.path.isfile("highscore.txt"):
    with open("highscore.txt", "r") as file:
        high_score = int(file.read())

options_menu = False

running = True
clock = pygame.time.Clock()

dragon = Dragon()
wyvern = Wyvern()  # Create an instance of the Wyvern class

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            options_menu = not options_menu

    if not options_menu:
        keys = pygame.key.get_pressed()

        if start_time == 0:
            start_time = pygame.time.get_ticks()
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000

        if random.random() < SPAWN_PROBABILITY:
            arrows.append(Arrow())

        for arrow in arrows[:]:
            arrow.move()
            if arrow.x > WIDTH:
                arrows.remove(arrow)

        for arrow in arrows:
            if arrow.check_collision(wyvern.hitbox):
                game_over = True
                break

        # Draw the background
        screen.fill((255, 255, 255))
        screen.blit(background_image, (0, 0))

        # Draw arrows
        for arrow in arrows:
            arrow.draw()

        # Move and draw the Wyvern
        wyvern.move()
        wyvern.draw()

        # Move and draw the Dragon
        dragon.move(keys)
        dragon.draw()

        font_large = pygame.font.Font(None, 72)
        font_medium = pygame.font.Font(None, 36)
        font_small = pygame.font.Font(None, 24)

        text = font_small.render(f"Time: {elapsed_time} seconds", True, (0, 0, 0))
        screen.blit(text, (10, 10))

        text = font_small.render(f"Score: {score}   High Score: {high_score}", True, (0, 0, 0))
        screen.blit(text, (10, 40))

        if options_menu:
            text = font_medium.render("OPTIONS", True, (0, 0, 0))
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

            text = font_small.render("Press ESC to resume", True, (0, 0, 0))
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 + 50))

        pygame.display.flip()
        clock.tick(60)

        if game_over:
            text = font_large.render("YOU LOSE", True, (255, 0, 0))
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

            pygame.display.flip()

            sound = pygame.mixer.Sound("game_over_sound.wav")  # Replace with the actual filename
            sound.play()

            pygame.display.flip()

            with open("highscore.txt", "w") as file:
                file.write(str(high_score))

            pygame.time.delay(2000)  # Introduce a 2000-millisecond delay
            game_over = False
            arrows = []
            start_time = pygame.time.get_ticks()
            elapsed_time = 0
            score = 0

pygame.quit()
sys.exit()
