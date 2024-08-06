import json
import importlib
import unittest
import pygame
import sys
import os
from unittest.mock import Mock

os.environ["SDL_VIDEODRIVER"] = "dummy"


if len(sys.argv) > 1:
    # Pop the last argument from sys.argv, which is the path to the game implementation
    implementation_path = sys.argv.pop()
    print(implementation_path)
    spec = importlib.util.spec_from_file_location("", implementation_path)
    game_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(game_module)

    Game = game_module.Game
else:
    from mdp import Game


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


class TestSpaceInvadersGame(unittest.TestCase):
    def setUp(self):
        pygame.init()

    def tearDown(self):
        pygame.quit()

    def test_create_aliens(self):
        self.test_number = 3

        game = Game()
        game.run(event=pygame.event.Event(pygame.NOEVENT))
        self.assertEqual(len(game.state_manager.alien_positions), 25)

    def test_player_movement(self):
        self.test_number = 2

        game = Game()
        initial_x_position = game.state_manager.player_position["x"]
        print(initial_x_position)
        # Simulate pressing the left arrow key
        event = pygame.event.Event(pygame.KEYDOWN, {"key": getattr(pygame, f"K_LEFT")})
        game.run(event=event)
        self.assertEqual(
            game.state_manager.player_position["x"],
            initial_x_position - game.state_manager.player_speed,
        )
        initial_x_position = game.state_manager.player_position["x"]

        # Simulate pressing the right arrow key
        event = pygame.event.Event(pygame.KEYDOWN, {"key": getattr(pygame, f"K_RIGHT")})
        game.run(event=event)
        self.assertEqual(
            game.state_manager.player_position["x"],
            initial_x_position + game.state_manager.player_speed,
        )

    def test_score_increment(self):
        self.test_number = 7

        game = Game()
        initial_score = game.state_manager.score
        # Simulate pressing the spacebar when bullet hits an alien
        game.state_manager.bullet_position = {"x": 75, "y": 75}
        # press space bar to shoot bullet
        event = pygame.event.Event(pygame.KEYDOWN, {"key": getattr(pygame, f"K_SPACE")})
        game.run(event=event)

        self.assertEqual(game.state_manager.score, initial_score + 1)

    def test_enemy_movement(self):
        self.test_number = 5

        game = Game()
        initial_alien_positions = game.state_manager.alien_positions.copy()

        # Simulate a few game iterations
        for _ in range(10):
            game.run(event=pygame.event.Event(pygame.NOEVENT))

        # Check if any alien positions have changed
        self.assertNotEqual(
            game.state_manager.alien_positions,
            initial_alien_positions,
            "Enemy positions should change after running the game loop",
        )

    def test_change_direction(self):
        self.test_number = 6

        game = Game()
        initial_directions = [
            alien["direction"] for alien in game.state_manager.alien_positions
        ]

        # Simulate a few game iterations
        for _ in range(10):
            game.run(event=pygame.event.Event(pygame.NOEVENT))

        # Check if any alien directions have changed
        self.assertNotEqual(
            [alien["direction"] for alien in game.state_manager.alien_positions],
            initial_directions,
            "Directions of enemies should change after reaching screen edges",
        )


if __name__ == "__main__":
    unittest.main(testRunner=JsonTestRunner(verbosity=2))
