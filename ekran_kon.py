import pygame

def show_game_over_screen(screen, font, score, best_score):
    """Wyświetla ekran końcowy."""
    screen.fill((0, 0, 0))  # Czarne tło

    game_over_text = font.render("Game Over", True, (255, 0, 0))
    score_text = font.render(f"Your Score: {score}", True, (255, 255, 255))
    best_score_text = font.render(f"Best Score: {best_score}", True, (255, 255, 0))
    restart_text = font.render("Press R to Restart", True, (255, 255, 255))

    screen.blit(game_over_text, (screen.get_width() // 2 - game_over_text.get_width() // 2, 300))
    screen.blit(score_text, (screen.get_width() // 2 - score_text.get_width() // 2, 400))
    screen.blit(best_score_text, (screen.get_width() // 2 - best_score_text.get_width() // 2, 450))
    screen.blit(restart_text, (screen.get_width() // 2 - restart_text.get_width() // 2, 600))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                waiting = False
