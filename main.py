import pygame
import sys
import random
from galenzie import Branch
from ekran_kon import show_game_over_screen  # Importujemy funkcję z pliku ekran_kon.py

pygame.init()

# Ustawienia ekranu
screen_width, screen_height = 720, 1280
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("First Game")

# Wczytanie grafik
background = pygame.image.load("c:/Users/piotr/Documents/2a/pygame/tlo.jpg")
bird = pygame.image.load("c:/Users/piotr/Documents/2a/pygame/ptak.png")
bird = pygame.transform.scale(bird, (196, 146))

# Pozycja ptaka
bird_x, bird_y = screen_width // 2, screen_height - 250
bird_speed = 8

# Gałęzie
branches = []
branch_speed = 5
branch_height = 30
branch_spawn_delay = 1500  # co ile nowa
last_spawn_time = pygame.time.get_ticks()

# Wyniki
score = 0
high_score = 0  # najlepszy wynik
font = pygame.font.Font(None, 50)

# Ładowanie najlepszego wyniku z pliku
try:
    with open("high_score.txt", "r") as file:
        high_score = int(file.read())
except FileNotFoundError:
    high_score = 0

# Główna pętla gry
running = True
clock = pygame.time.Clock()

# Lista do przechowywania stanów, które gałęzie zostały ominięte
passed_branches = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Poruszanie ptakiem
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and bird_x > 0:
        bird_x -= bird_speed
    if keys[pygame.K_RIGHT] and bird_x < screen_width - bird.get_width():  # zeby nie wychodziło poza ekran
        bird_x += bird_speed

    # Generowanie gałęzi
    current_time = pygame.time.get_ticks()
    if current_time - last_spawn_time > branch_spawn_delay:
        gap = random.randint(200, 300)  # Większy gap (przerwa)
        branch_type = random.choice(["left", "right", "both"])

        if branch_type == "left":
            # Gałąź tylko z lewej strony
            max_left_length = screen_width // 2 - gap
            left_length = random.randint(300, max_left_length if max_left_length > 300 else 300)
            branches.append(Branch(0, 0, left_length, branch_height, branch_speed))

        elif branch_type == "right":
            # Gałąź tylko z prawej strony
            max_right_length = screen_width // 2 - gap
            right_length = random.randint(300, max_right_length if max_right_length > 300 else 300)
            branches.append(Branch(screen_width - right_length, 0, right_length, branch_height, branch_speed))

        elif branch_type == "both":
            # Gałęzie z obu stron
            max_left_length = screen_width // 2 - gap
            max_right_length = screen_width // 2 - gap
            left_length = random.randint(200, max_left_length if max_left_length > 200 else 200)
            right_length = random.randint(200, max_right_length if max_right_length > 200 else 200)
            branches.append(Branch(0, 0, left_length, branch_height, branch_speed))
            branches.append(Branch(screen_width - right_length, 0, right_length, branch_height, branch_speed))

        last_spawn_time = current_time

    # Rysowanie
    screen.blit(background, (0, 0))
    for branch in branches[:]:
        branch.move()
        branch.draw(screen)

        # Sprawdzanie, czy gałąź wyszła poza ekran
        if branch.off_screen(screen_height):
            if branch not in passed_branches:  # Sprawdzamy, czy nie naliczyliśmy już punktu za tę gałąź
                passed_branches.append(branch)
                score += 1  # Naliczamy punkt za ominięcie gałęzi

    screen.blit(bird, (bird_x, bird_y))
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    high_score_text = font.render(f"Best: {high_score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(high_score_text, (10, 50))

    # Kolizje
    bird_rect = pygame.Rect(bird_x, bird_y, bird.get_width(), bird.get_height())
    for branch in branches:
        branch_rect = pygame.Rect(branch.x, branch.y, branch.width, branch.height)
        if bird_rect.colliderect(branch_rect):  # sprawdzanie kolizji
            if score > high_score:
                high_score = score
                with open("high_score.txt", "w") as file:  # zapis nowego najlepszego wyniku
                    file.write(str(high_score))
            show_game_over_screen(score, screen, font, high_score)  # Używamy funkcji z pliku ekran_kon.py
            score = 0  # reset wyniku
            passed_branches.clear()  # resetujemy listę przeoczonych gałęzi
            branches.clear()  # usunięcie gałęzi
            bird_x, bird_y = screen_width // 2, screen_height - 250  # reset pozycji ptaka

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
