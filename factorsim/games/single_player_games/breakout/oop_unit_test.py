import unittest
from unittest.mock import MagicMock, patch
import pygame
import sys
import importlib
import json
import os

os.environ["SDL_VIDEODRIVER"] = "dummy"


if len(sys.argv) > 1:
    # Pop the last argument from sys.argv, which is the path to the game implementation
    implementation_path = sys.argv.pop()
    print(implementation_path)
    spec = importlib.util.spec_from_file_location("", implementation_path)
    game_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(game_module)

    Game = game_module.Game
    Ball = game_module.Ball
    Brick = game_module.Brick
    Paddle = game_module.Paddle
    WIDTH = game_module.WIDTH
    HEIGHT = game_module.HEIGHT
    GRID_SIZE = game_module.GRID_SIZE

else:
    from oop import Game, Ball, Brick, Paddle, WIDTH, HEIGHT, GRID_SIZE


class JsonTestResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_results = []

    def addSuccess(self, test):
        super().addSuccess(test)
        test_name = test._testMethodName
        test_number = getattr(test, "test_number", None)
        self.test_results.append(
            {"function_name": test_name, "test_number": test_number, "status": "OK"}
        )

    def addError(self, test, err):
        super().addError(test, err)
        test_name = test._testMethodName
        test_number = getattr(test, "test_number", None)
        self.test_results.append(
            {
                "function_name": test_name,
                "test_number": test_number,
                "message": str(err),
                "status": "ERROR",
            }
        )

    def addFailure(self, test, err):
        super().addFailure(test, err)
        test_name = test._testMethodName
        test_number = getattr(test, "test_number", None)
        self.test_results.append(
            {
                "function_name": test_name,
                "test_number": test_number,
                "message": str(err),
                "status": "FAIL",
            }
        )


class JsonTestRunner(unittest.TextTestRunner):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resultclass = JsonTestResult

    def run(self, test):
        result = super().run(test)
        with open("test_results.json", "w") as f:
            json.dump(result.test_results, f, indent=4)
        return result


class TestBreakoutGame(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.game = Game()

    def tearDown(self) -> None:
        pygame.quit()

    def test_paddle_move(self):
        self.test_number = 1
        self.game.run(event=pygame.event.Event(pygame.NOEVENT))
        self.game.run(event=pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_LEFT}))
        self.assertEqual(
            self.game.paddle.rect.x,
            (WIDTH - GRID_SIZE * 4) // 2 - self.game.paddle.speed,
        )

        self.game.run(event=pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RIGHT}))
        self.assertEqual(self.game.paddle.rect.x, (WIDTH - GRID_SIZE * 4) // 2)

    def test_ball_update(self):
        self.test_number = 3

        initial_y = self.game.ball.rect.y
        initial_dy = self.game.ball.dy

        # Simulate game loop running for one frame
        self.game.update()

        # Check if the ball's position and direction have been updated correctly
        self.assertEqual(
            self.game.ball.rect.y, initial_y + self.game.ball.speed * initial_dy
        )
        self.assertEqual(
            self.game.ball.dx, self.game.ball.dx
        )  # Direction remains unchanged
        self.assertEqual(self.game.ball.dy, initial_dy)  # Direction remains unchanged

    def test_brick_init(self):
        self.test_number = 4
        brick = Brick(10, 20)
        self.assertEqual(brick.rect.topleft, (10, 20))

    def test_ball_init(self):
        self.test_number = 2
        ball = Ball()
        self.assertEqual(
            ball.rect.topleft, ((WIDTH - GRID_SIZE) // 2, HEIGHT - GRID_SIZE * 4)
        )

    def test_update_collide(self):
        self.test_number = 5
        brick_mock = MagicMock()
        brick_mock.rect = pygame.Rect(0, 0, GRID_SIZE * 2, GRID_SIZE)

        self.game.ball.rect.topleft = (
            (WIDTH - GRID_SIZE) // 2,
            HEIGHT - GRID_SIZE * 2,
        )
        self.game.ball.dy = 1  # To make it move down
        self.game.paddle.rect.topleft = (
            (WIDTH - GRID_SIZE * 4) // 2,
            HEIGHT - GRID_SIZE * 2,
        )
        self.game.run(event=pygame.event.Event(pygame.NOEVENT))
        self.assertEqual(self.game.ball.dy, -1)

        with patch("pygame.sprite.spritecollide", return_value=[brick_mock]):
            self.game.run(event=pygame.event.Event(pygame.NOEVENT))
            self.assertEqual(self.game.ball.dy, -1)

        self.game.ball.rect.topleft = (0, HEIGHT - GRID_SIZE * 4)
        self.game.ball.dx = -1
        self.game.run(event=pygame.event.Event(pygame.NOEVENT))
        self.assertEqual(self.game.ball.dx, 1)

    def test_game_over(self):
        self.test_number = 8

        self.game.ball.rect.y = HEIGHT
        self.game.run(event=pygame.event.Event(pygame.NOEVENT))
        self.assertTrue(self.game.game_over)

    def test_reset_game(self):
        self.test_number = 9
        initial_paddle_pos = self.game.paddle.rect.topleft
        initial_ball_pos = self.game.ball.rect.topleft
        initial_bricks = len(self.game.bricks)

        self.game.reset_game()

        self.assertEqual(self.game.paddle.rect.topleft, initial_paddle_pos)
        self.assertEqual(self.game.ball.rect.topleft, initial_ball_pos)
        self.assertEqual(len(self.game.bricks), initial_bricks)
        self.assertFalse(self.game.game_over)


if __name__ == "__main__":
    unittest.main(testRunner=JsonTestRunner(verbosity=2))
