import pygame
import sys
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
        self.image = pygame.Surface((GRID_SIZE * 4, GRID_SIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.topleft = ((WIDTH - self.rect.width) // 2, HEIGHT - GRID_SIZE * 2)
        self.speed = 10

    def move_left(self):
        self.rect.x -= self.speed
        if self.rect.left < 0:
            self.rect.left = 0

    def move_right(self):
        self.rect.x += self.speed
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.topleft = ((WIDTH - GRID_SIZE) // 2, HEIGHT - GRID_SIZE * 4)
        self.speed = 5
        self.dx = random.choice([-1, 1])
        self.dy = -1

    def update(self):
        self.rect.x += self.speed * self.dx
        self.rect.y += self.speed * self.dy

    def bounce_x(self):
        self.dx *= -1

    def bounce_y(self):
        self.dy *= -1


class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((GRID_SIZE * 2, GRID_SIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.game_over = False

        self.all_sprites = pygame.sprite.Group()
        self.paddle = Paddle()
        self.ball = Ball()
        self.bricks = pygame.sprite.Group()

        self.all_sprites.add(self.paddle, self.ball)

        # Re-create bricks
        brick_width = GRID_SIZE * 2
        brick_spacing = 5

        for row in range(5):
            for col in range(WIDTH // (brick_width + brick_spacing)):
                brick = Brick(
                    col * (brick_width + brick_spacing),
                    row * (GRID_SIZE + brick_spacing),
                )
                self.all_sprites.add(brick)
                self.bricks.add(brick)

    def update(self):
        if not self.game_over:
            self.all_sprites.update()

            # Check for collisions with paddle
            if pygame.sprite.spritecollide(self.ball, [self.paddle], False):
                self.ball.bounce_y()

            # Check for collisions with bricks
            brick_collisions = pygame.sprite.spritecollide(self.ball, self.bricks, True)
            if brick_collisions:
                self.ball.bounce_y()

            # Check for collisions with walls
            if self.ball.rect.left <= 0 or self.ball.rect.right >= WIDTH:
                self.ball.bounce_x()
            if self.ball.rect.top <= 0:
                self.ball.bounce_y()

            # Check if the ball missed the paddle
            if self.ball.rect.bottom >= HEIGHT:
                self.game_over = True

    def render_game(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(FPS)

    def reset_game(self):
        self.game_over = False
        self.all_sprites.empty()
        self.bricks.empty()
        brick_width = GRID_SIZE * 2
        brick_spacing = 5

        for row in range(5):
            for col in range(WIDTH // (brick_width + brick_spacing)):
                brick = Brick(
                    col * (brick_width + brick_spacing),
                    row * (GRID_SIZE + brick_spacing),
                )
                self.all_sprites.add(brick)
                self.bricks.add(brick)

        # Reset paddle and ball
        self.paddle.rect.topleft = (
            (WIDTH - self.paddle.rect.width) // 2,
            HEIGHT - GRID_SIZE * 2,
        )
        self.ball.rect.topleft = ((WIDTH - GRID_SIZE) // 2, HEIGHT - GRID_SIZE * 4)
        self.ball.dx = random.choice([-1, 1])
        self.ball.dy = -1

        # Add paddle and ball back to the sprite group
        self.all_sprites.add(self.paddle, self.ball)

        # Wait for a moment before restarting to avoid instant key press recognition
        pygame.time.wait(500)

    def run(self, event):

        if event.type == pygame.QUIT:
            pygame.quit()
            return False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.paddle.move_left()
            elif event.key == pygame.K_RIGHT:
                self.paddle.move_right()

        self.update()
        self.render_game()

        # Check if the game is over and ask for a restart
        if self.game_over:
            font = pygame.font.Font(None, 74)
            text = font.render("Game Over", True, WHITE)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(text, text_rect)
            restart_text = font.render("Press R to restart", True, WHITE)
            restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
            self.screen.blit(restart_text, restart_rect)
            pygame.display.flip()
            pygame.time.wait(1000)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_r:
                        self.reset_game()
                    elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return False
        return True


if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
