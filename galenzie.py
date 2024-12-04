import pygame

class Branch:
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.color = (139, 69, 19)  # Kolor brązowy

    def move(self):
        """Przesuwa gałąź w dół."""
        self.y += self.speed

    def draw(self, screen):
        """Rysuje gałąź na ekranie."""
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def off_screen(self, screen_height):
        """Sprawdza, czy gałąź wyszła poza ekran."""
        return self.y > screen_height
