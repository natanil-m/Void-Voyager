import pygame
import random
import math
import os

pygame.init()

# Constants
WIDTH, HEIGHT = 1000, 800
SPACESHIP_SPEED = 5
ASTEROID_SIZE = 25
COLLECTIBLE_SIZE = 10
BACKGROUND_COLOR = (50, 100, 100)
HEALTH_SIZE = (100, 30)
BASE_PATH = os.path.join(os.getcwd(), 'Assets/')
BEST_SCORE = 0
ANGLE_SPEED = 6
THRUST = 0.3
DECEL = 0.98
N_ASTEROIDS = 5
BLACK_HOLE_RADIUS = 300

# Initial Setup for the background
screen_size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Void Voyager")

# Load images
player_scale = (40, 30)
player_img_plain = pygame.image.load(BASE_PATH + "spaceship.png")
player_img_plain = pygame.transform.scale(player_img_plain, player_scale)

player_img_thrust1 = pygame.image.load(BASE_PATH + "spaceship1.png")
player_img_thrust1 = pygame.transform.scale(player_img_thrust1, player_scale)

player_img_thrust2 = pygame.image.load(BASE_PATH + "spaceship2.png")
player_img_thrust2 = pygame.transform.scale(player_img_thrust2, player_scale)

player_img_left = pygame.image.load(BASE_PATH + "spaceshipleft.png")
player_img_left = pygame.transform.scale(player_img_left, player_scale)

player_img_right = pygame.image.load(BASE_PATH + "spaceshipright.png")
player_img_right = pygame.transform.scale(player_img_right, player_scale)

asteroid_img = pygame.image.load(BASE_PATH + "asteroid.png")
asteroid_img = pygame.transform.scale(asteroid_img, (ASTEROID_SIZE, ASTEROID_SIZE))

collectible_img = pygame.image.load(BASE_PATH + "collectible.png")
collectible_img = pygame.transform.scale(collectible_img, (COLLECTIBLE_SIZE, COLLECTIBLE_SIZE))

repair_img = pygame.image.load(BASE_PATH + "gear.png")
repair_img = pygame.transform.scale(repair_img, (30, 30))

health_images = [pygame.image.load(BASE_PATH + f'health{i}.png') for i in range(4)]
health_images = [pygame.transform.scale(img, HEALTH_SIZE) for img in health_images]

player_x, player_y = WIDTH // 2, HEIGHT // 2 - 50
spaceship_angle = 0
spaceship_speed_x, spaceship_speed_y = 0, 0
is_thrusting = False

clock = pygame.time.Clock()

asteroids = []
collectibles = []
repairs = []

game_over = False
player_lives = 3
score = 0

invincible = False
invincibility_timer = 0

running = True

# Load background images
background_image = pygame.image.load(BASE_PATH + "background_img.png")
background_image = pygame.transform.scale(background_image, screen_size)

background_image2 = pygame.image.load(BASE_PATH + "background_img2.png")
background_image2 = pygame.transform.scale(background_image2, screen_size)

while running:
    player_img = player_img_plain

    screen.blit(background_image, (0, 0))

    if player_lives > 0:
        screen.blit(health_images[player_lives], (WIDTH - HEALTH_SIZE[0] - 20, 20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            spaceship_angle += ANGLE_SPEED
            player_img = player_img_left
        if keys[pygame.K_RIGHT]:
            spaceship_angle -= ANGLE_SPEED
            player_img = player_img_right
        if keys[pygame.K_SPACE]:
            is_thrusting = True
            player_img = player_img_thrust1
        else:
            is_thrusting = False

        if is_thrusting:
            spaceship_speed_x += THRUST * math.cos(math.radians(spaceship_angle))
            spaceship_speed_y -= THRUST * math.sin(math.radians(spaceship_angle))
            spaceship_speed = math.sqrt(spaceship_speed_x**2 + spaceship_speed_y**2)
            if spaceship_speed >4:
               player_img = player_img_thrust2

        spaceship_speed_x *= DECEL
        spaceship_speed_y *= DECEL

        player_x += spaceship_speed_x
        player_y += spaceship_speed_y

        player_x = max(0, min(WIDTH, player_x))
        player_y = max(0, min(HEIGHT, player_y))

        # Attract asteroids towards the black hole
        new_asteroids = []
        for asteroid in asteroids:
            asteroid_x, asteroid_y, asteroid_angle, asteroid_distance = asteroid
            asteroid_speed = 1 + (500 - asteroid_distance) * 0.01
            asteroid_angle += 0.02
            asteroid_distance -= asteroid_speed
            asteroid_x = WIDTH // 2 - asteroid_distance * math.cos(asteroid_angle)
            asteroid_y = HEIGHT // 2 - asteroid_distance * math.sin(asteroid_angle)
            if asteroid_distance > 0:
                new_asteroids.append([asteroid_x, asteroid_y, asteroid_angle, asteroid_distance])
        asteroids = new_asteroids

        # Attract collectibles towards the black hole
        new_collectibles = []
        for collectible in collectibles:
            collectible_x, collectible_y, collectible_angle, collectible_distance = collectible
            collectible_speed = 1 + (300 - collectible_distance) * 0.01
            collectible_angle += 0.02
            collectible_distance -= collectible_speed
            collectible_x = WIDTH // 2 - collectible_distance * math.cos(collectible_angle)
            collectible_y = HEIGHT // 2 - collectible_distance * math.sin(collectible_angle)
            if collectible_distance > 0:
                new_collectibles.append([collectible_x, collectible_y, collectible_angle, collectible_distance])
        collectibles = new_collectibles

        # Attract repairs towards the black hole
        new_repairs = []
        for repair in repairs:
            repair_x, repair_y, repair_angle, repair_distance = repair
            repair_speed = 1 + (300 - repair_distance) * 0.01
            repair_angle += 0.03
            repair_distance -= repair_speed
            repair_x = WIDTH // 2 - repair_distance * math.cos(repair_angle)
            repair_y = HEIGHT // 2 - repair_distance * math.sin(repair_angle)
            if repair_distance > 0:
                new_repairs.append([repair_x, repair_y, repair_angle, repair_distance])
        repairs = new_repairs

        # Check for collisions between the player and asteroids
        if not invincible:
            for asteroid in asteroids:
                asteroid_x, asteroid_y, _, _ = asteroid
                player_rect = player_img.get_rect(center=(int(player_x), int(player_y)))
                asteroid_rect = asteroid_img.get_rect(center=(int(asteroid_x), int(asteroid_y)))
                if player_rect.colliderect(asteroid_rect):
                    player_lives -= 1
                    if player_lives <= 0:
                        game_over = True
                    else:
                        invincible = True
                        invincibility_timer = 60  # 60 frames (1 second) of invincibility

        if invincibility_timer > 0:
            invincibility_timer -= 1

        if invincibility_timer <= 0:
            invincible = False

        # Check for collisions between the player and collectibles
        for collectible in collectibles:
            collectible_x, collectible_y, _, _ = collectible
            player_rect = player_img.get_rect(center=(int(player_x), int(player_y)))
            collectible_rect = collectible_img.get_rect(center=(int(collectible_x), int(collectible_y)))
            if player_rect.colliderect(collectible_rect):
                score += 10
                collectibles.remove(collectible)

        # Check for collisions between the player and repairs
        for repair in repairs:
            repair_x, repair_y, _, _ = repair
            player_rect = player_img.get_rect(center=(int(player_x), int(player_y)))
            repair_rect = repair_img.get_rect(center=(int(repair_x), int(repair_y)))
            if player_rect.colliderect(repair_rect):
                if player_lives < 3:
                    player_lives += 1
                repairs.remove(repair)

        # Check if there are fewer asteroids than a certain number and add new asteroids off-screen
        while len(asteroids) < N_ASTEROIDS:
            asteroid_distance = random.randint(400, 600)
            asteroid_angle = random.uniform(0, 2 * math.pi)
            asteroid_x = WIDTH // 2 - asteroid_distance * math.cos(asteroid_angle)
            asteroid_y = HEIGHT // 2 - asteroid_distance * math.sin(asteroid_angle)
            asteroids.append([asteroid_x, asteroid_y, asteroid_angle, asteroid_distance])

        # Check if there are fewer collectibles than a certain number and add new collectibles off-screen
        while len(collectibles) < 4:
            collectible_distance = random.randint(200, 400)
            collectible_angle = random.uniform(0, 2 * math.pi)
            collectible_x = WIDTH // 2 - collectible_distance * math.cos(collectible_angle)
            collectible_y = HEIGHT // 2 - collectible_distance * math.sin(collectible_angle)
            collectibles.append([collectible_x, collectible_y, collectible_angle, collectible_distance])

        # Check if there are fewer repairs than a certain number and add new repairs off-screen
        while len(repairs) < 1:
            repair_distance = random.randint(200, 400)
            repair_angle = random.uniform(0, 2 * math.pi)
            repair_x = WIDTH // 2 - repair_distance * math.cos(repair_angle)
            repair_y = HEIGHT // 2 - repair_distance * math.sin(repair_angle)
            repairs.append([repair_x, repair_y, repair_angle, repair_distance])

    # Move and draw objects
    for asteroid in asteroids:
        asteroid_x, asteroid_y, _, _ = asteroid
        screen.blit(asteroid_img, (int(asteroid_x), int(asteroid_y)))

    for collectible in collectibles:
        collectible_x, collectible_y, _, _ = collectible
        screen.blit(collectible_img, (int(collectible_x), int(collectible_y)))

    for repair in repairs:
        repair_x, repair_y, _, _ = repair
        screen.blit(repair_img, (int(repair_x), int(repair_y)))

    # Draw the spaceship
    if not invincible or (invincible and invincibility_timer % 10 < 5):
        rotated_spaceship = pygame.transform.rotate(player_img, spaceship_angle)
        rect = rotated_spaceship.get_rect()
        rect.center = (player_x, player_y)
        screen.blit(rotated_spaceship, rect)

    # Draw the score
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

    if game_over:
        screen.blit(background_image2, (0, 0))
        if BEST_SCORE < score:
            BEST_SCORE = score
        # Game over menu
        text = font.render("Game Over", True, (255, 0, 0))
        text_rect = text.get_rect(center=(WIDTH // 2 + 30, HEIGHT // 2 - 150))
        screen.blit(text, text_rect)
        text = font.render(f"Your Score: {score}", True, (221, 100, 100))
        text_rect = text.get_rect(center=(WIDTH // 2 + 30, HEIGHT // 2 - 100))
        screen.blit(text, text_rect)
        text = font.render(f"Best Score: {BEST_SCORE}", True, (120, 255, 100))
        text_rect = text.get_rect(center=(WIDTH // 2 + 30, HEIGHT // 2 - 50))
        screen.blit(text, text_rect)
        text = font.render("Press R to Restart", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH // 2 + 30, HEIGHT // 2 + 50))
        screen.blit(text, text_rect)
        text = font.render("Press Q to Quit", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH // 2 + 30, HEIGHT // 2 + 100))
        screen.blit(text, text_rect)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            player_lives = 3
            game_over = False
            asteroids.clear()
            collectibles.clear()
            repairs.clear()
            player_x, player_y = WIDTH // 2, HEIGHT // 2 - 50
            score = 0
        elif keys[pygame.K_q]:
            running = False

    pygame.display.update()
    screen.fill(BACKGROUND_COLOR)
    clock.tick(50)

# Quit Pygame
pygame.quit()
