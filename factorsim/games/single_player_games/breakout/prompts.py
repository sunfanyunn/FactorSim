iterative_prompts = """
Create a paddle character, represented as a horizontal rectangle, that is controlled by the player using the left and right arrow keys. The paddle moves only along the horizontal axis at the bottom of the game window.
Design a ball character as a small circle that initially rests on the paddle. When the game starts, allow the ball to move in a random direction upon a player's mouse click or key press.
Implement  gravity, causing the ball to fall downward. If the ball hits the paddle, ensure it bounces off at an angle dependent on the point of contact.
Introduce bricks scattered across the top of the game window, forming a wall. Each brick should be breakable, and when hit by the ball, it should disappear. 
Implement collision detection to determine when the ball hits a brick, the paddle, or the walls of the game window. When the ball hits a brick, increase the player's score.
Create a scoring system where the player earns points for each brick destroyed. Display the current score at the top-left corner of the screen during gameplay.
Ensure that the game has no predefined end and that new levels or rows of bricks continue to appear, maintaining consistent difficulty as the game progresses.
Ensure the game ends if the ball touches the bottom of the game window. When the game ends, display a "Game Over!" message.
Allow the player to restart the game after it ends by providing a "Restart" option on the game over screen.
"""

context_prompt_code = """
import pygame
import random

# Constants
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)


class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        \"\"\"
        self.rect is the pygame.Rect rectangle representing the bird
        \"\"\"
        self.rect = ...

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        \"\"\"
        self.rect is the pygame.Rect rectangle representing the bird
        \"\"\"
        self.rect = ...

    def update(self):
        \"\"\"
        This will be called every game loop
        \"\"\"

class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        \"\"\"
        Initialize the x, y location of this brick
        self.rect is the pygame.Rect rectangle representing the brick
        \"\"\"
        self.rect = self.image.get_rect()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.game_over = False
        self.reset_game()

    def reset_game(self):
        \"\"\"
        Initialize / reset the game
        self.game_over is a boolean representing whether the game is over
        \"\"\"
        self.all_sprites = pygame.sprite.Group()
        self.paddle = Paddle()
        self.ball = Ball()
        self.bricks = pygame.sprite.Group()

        self.all_sprites.add(self.paddle, self.ball)
        ...


    def run(self, event):
        \"\"\" 
        please implement the main game loop here
        \"\"\"


if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
"""
