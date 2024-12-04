import pygame

# Funkcja wyświetlająca ekran końcowy
def show_game_over_screen(final_score, screen, font, high_score):
    screen.fill((0, 0, 0))  # Czarny ekran
    game_over_text = font.render("Game Over!", True, (255, 255, 255))
    score_text = font.render(f"Score: {final_score}", True, (255, 255, 255))
    high_score_text = font.render(f"Best: {high_score}", True, (255, 255, 255))
    retry_text = font.render("Press R to Retry", True, (255, 255, 255))

    # Rysowanie tekstu na ekranie
    screen.blit(game_over_text, (screen.get_width() // 2 - 100, screen.get_height() // 2 - 100))
    screen.blit(score_text, (screen.get_width() // 2 - 100, screen.get_height() // 2 - 50))
    screen.blit(high_score_text, (screen.get_width() // 2 - 100, screen.get_height() // 2))
    screen.blit(retry_text, (screen.get_width() // 2 - 150, screen.get_height() // 2 + 100))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                waiting = False
