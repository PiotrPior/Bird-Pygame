import pygame
import sys
import random
from galenzie import Branch
from ekran_kon import show_game_over_screen
import os

pygame.init()

# Wymiary ekranu
screen_width, screen_height = 720, 1280
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("First Game")

# Tło i ptak
background = pygame.image.load("c:/Users/piotr/Documents/2a/pygame/tlo.jpg")
bird_image = pygame.image.load("c:/Users/piotr/Documents/2a/pygame/ptak.png")
bird_image = pygame.transform.scale(bird_image, (196, 146))

# Wyniki
score = 0
best_score = 0
font = pygame.font.Font(None, 50)

# Parametry ptaka i gałęzi
bird_x, bird_y = screen_width // 2, screen_height - 250
bird_speed = 8
bird_mask = pygame.mask.from_surface(bird_image)
branches = []
branch_speed = 5
branch_spawn_delay = 1500
last_spawn_time = pygame.time.get_ticks()

running = True
clock = pygame.time.Clock()

# Funkcja resetująca stan gry
def reset_game():
    global bird_x, bird_y, score, branches, last_spawn_time
    bird_x, bird_y = screen_width // 2, screen_height - 250
    score = 0
    branches = []
    last_spawn_time = pygame.time.get_ticks()

# Funkcja wczytująca najlepszy wynik z pliku
def load_best_score():
    if os.path.exists("best_score.txt"):
        with open("best_score.txt", "r") as file:
            return int(file.read())
    return 0  # Domyślny najlepszy wynik to 0, jeśli plik nie istnieje

# Funkcja zapisująca najlepszy wynik do pliku
def save_best_score(score):
    with open("best_score.txt", "w") as file:
        file.write(str(score))

# Wczytanie najlepszego wyniku z pliku
best_score = load_best_score()

# Główna pętla gry
while running:
    # Resetowanie gry po zakończeniu
    reset_game()

    while True:  # Pętla gry
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Poruszanie ptaka
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and bird_x > 0:
            bird_x -= bird_speed
        if keys[pygame.K_RIGHT] and bird_x < screen_width - bird_image.get_width():
            bird_x += bird_speed

        # Generowanie gałęzi
        current_time = pygame.time.get_ticks()
        if current_time - last_spawn_time > branch_spawn_delay:
            gap = random.randint(200, 300)  # Przerwa między gałęziami
            branch_type = random.choice(["left", "right", "both"])

            if branch_type == "left":
                left_length = random.randint(200, min(500, screen_width // 2))
                branches.append(Branch(0, 0, left_length, 30, branch_speed))
            elif branch_type == "right":
                right_length = random.randint(200, min(500, screen_width // 2))
                branches.append(Branch(screen_width - right_length, 0, right_length, 30, branch_speed))
            elif branch_type == "both":
                gap_between = random.randint(200, 300)
                left_length = random.randint(200, screen_width // 2 - gap_between // 2)
                right_length = random.randint(200, screen_width // 2 - gap_between // 2)
                branches.append(Branch(0, 0, left_length, 30, branch_speed))
                branches.append(Branch(screen_width - right_length, 0, right_length, 30, branch_speed))

            last_spawn_time = current_time

        # Rysowanie
        screen.blit(background, (0, 0))
        screen.blit(bird_image, (bird_x, bird_y))

        # Aktualizacja gałęzi
        for branch in branches[:]:
            branch.move()
            branch.draw(screen)
            if branch.off_screen(screen_height):
                branches.remove(branch)
                score += 1  # Dodanie punktu za ominięcie przeszkody

        # Wyświetlanie wyników
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        best_score_text = font.render(f"Best: {best_score}", True, (255, 215, 0))
        screen.blit(score_text, (10, 10))
        screen.blit(best_score_text, (10, 50))

        # Kolizje
        bird_rect = pygame.Rect(bird_x, bird_y, bird_image.get_width(), bird_image.get_height())
        for branch in branches:
            branch_rect = pygame.Rect(branch.x, branch.y, branch.width, branch.height)
            if bird_mask.overlap(pygame.mask.Mask((branch.width, branch.height), True), (branch.x - bird_x, branch.y - bird_y)):
                running = False
                best_score = max(best_score, score)
                save_best_score(best_score)
                show_game_over_screen(screen, font, score, best_score)

                # Po zakończeniu gry czekamy na naciśnięcie R do restartu
                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                            reset_game()  # Reset gry do początku
                            waiting = False
                            break

                break

        pygame.display.flip()
        clock.tick(60)

pygame.quit()
sys.exit()
