import json
import importlib
import unittest
import pygame
import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
target_path = os.path.join(script_dir, "../../../")
sys.path.append(target_path)
from unittest_utils import JsonTestRunner
os.environ["SDL_VIDEODRIVER"] = "dummy"


if len(sys.argv) > 1:
    # Pop the last argument from sys.argv, which is the path to the game implementation
    implementation_path = sys.argv.pop()
    spec = importlib.util.spec_from_file_location("", implementation_path)
    game_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(game_module)

    Game = game_module.Game
else:
    from mdp import Game


class TestMinesweeperGame(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.game = Game()

    def tearDown(self):
        pygame.quit()

    def test_grid_creation(self):
        self.test_number = 1
        # Test if the grid is correctly initialized
        grid = self.game.state_manager.grid
        self.assertEqual(len(grid), self.game.state_manager.grid_width)
        self.assertTrue(
            all(len(row) == self.game.state_manager.grid_height for row in grid)
        )

    def test_mine_placement(self):
        self.test_number = 2
        # Test if mines are placed correctly
        grid = self.game.state_manager.grid
        mine_count = sum(cell["is_mine"] for row in grid for cell in row)
        self.assertEqual(mine_count, self.game.state_manager.num_mines)

        # Ensure that no two cells have mines
        all_mines = [
            (x, y)
            for x in range(self.game.state_manager.grid_width)
            for y in range(self.game.state_manager.grid_height)
            if grid[x][y]["is_mine"]
        ]
        self.assertEqual(
            len(all_mines), len(set(all_mines))
        )  # Check for unique mine locations

    def test_adjacent_mines_calculation(self):
        self.test_number = 3
        # Test if adjacent mines are calculated correctly
        self.game.state_manager.num_mines = 0  # Ensure no mines for this test
        self.game.state_manager.grid = [
            [
                {
                    "is_mine": False,
                    "is_revealed": False,
                    "is_flagged": False,
                    "adjacent_mines": 0,
                }
                for _ in range(self.game.state_manager.grid_height)
            ]
            for _ in range(self.game.state_manager.grid_width)
        ]

        for x in range(self.game.state_manager.grid_width):
            for y in range(self.game.state_manager.grid_height):
                pygame.event.post(
                    pygame.event.Event(
                        pygame.MOUSEBUTTONDOWN,
                        {
                            "button": 1,
                            "pos": (
                                x * self.game.state_manager.grid_size,
                                y * self.game.state_manager.grid_size,
                            ),
                        },
                    )
                )
                self.game.run(
                    pygame.event.Event(
                        pygame.MOUSEBUTTONDOWN,
                        {
                            "button": 1,
                            "pos": (
                                x * self.game.state_manager.grid_size,
                                y * self.game.state_manager.grid_size,
                            ),
                        },
                    )
                )

                # Check if adjacent mines count is updated
                cell = self.game.state_manager.grid[x][y]
                if not cell["is_mine"]:
                    adjacent_count = sum(
                        self.game.state_manager.grid[nx][ny]["is_mine"]
                        for dx in [-1, 0, 1]
                        for dy in [-1, 0, 1]
                        if (dx != 0 or dy != 0)
                        if 0 <= (nx := x + dx) < self.game.state_manager.grid_width
                        if 0 <= (ny := y + dy) < self.game.state_manager.grid_height
                    )
                    self.assertEqual(cell["adjacent_mines"], adjacent_count)

    def test_reveal_cell(self):
        self.test_number = 4
        # Test if cells are revealed correctly
        self.game.state_manager.grid = [
            [
                {
                    "is_mine": False,
                    "is_revealed": False,
                    "is_flagged": False,
                    "adjacent_mines": 0,
                }
                for _ in range(self.game.state_manager.grid_height)
            ]
            for _ in range(self.game.state_manager.grid_width)
        ]
        test_x, test_y = 1, 1
        pygame.event.post(
            pygame.event.Event(
                pygame.MOUSEBUTTONDOWN,
                {
                    "button": 1,
                    "pos": (
                        test_x * self.game.state_manager.grid_size,
                        test_y * self.game.state_manager.grid_size,
                    ),
                },
            )
        )
        self.game.run(
            pygame.event.Event(
                pygame.MOUSEBUTTONDOWN,
                {
                    "button": 1,
                    "pos": (
                        test_x * self.game.state_manager.grid_size,
                        test_y * self.game.state_manager.grid_size,
                    ),
                },
            )
        )
        cell = self.game.state_manager.grid[test_x][test_y]
        self.assertTrue(cell["is_revealed"])

    # def test_flagging_cell(self):
    #     # Test if cells can be flagged correctly
    #     self.game.state_manager.grid = [[{'is_mine': False, 'is_revealed': False, 'is_flagged': False, 'adjacent_mines': 0} for _ in range(self.game.state_manager.grid_height)] for _ in range(self.game.state_manager.grid_width)]
    #     test_x, test_y = 1, 1

    #     # Simulate flagging the cell
    #     pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 3, "pos": (test_x * self.game.state_manager.grid_size, test_y * self.game.state_manager.grid_size)}))
    #     self.game.run(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 3, "pos": (test_x * self.game.state_manager.grid_size, test_y * self.game.state_manager.grid_size)}))
    #     cell = self.game.state_manager.grid[test_x][test_y]
    #     #run a no event to update the game state
    #     self.game.run(pygame.event.Event(pygame.NOEVENT))
    #     self.assertTrue(cell['is_flagged'])

    #     # Simulate unflagging the cell
    #     pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 3, "pos": (test_x * self.game.state_manager.grid_size, test_y * self.game.state_manager.grid_size)}))
    #     self.game.run(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 3, "pos": (test_x * self.game.state_manager.grid_size, test_y * self.game.state_manager.grid_size)}))
    #     self.assertFalse(cell['is_flagged'])

    def test_win_condition(self):
        self.test_number = 8
        # Test win condition logic
        self.game.state_manager.num_mines = 0
        self.game.state_manager.grid = [
            [
                {
                    "is_mine": False,
                    "is_revealed": False,
                    "is_flagged": False,
                    "adjacent_mines": 0,
                }
                for _ in range(self.game.state_manager.grid_height)
            ]
            for _ in range(self.game.state_manager.grid_width)
        ]

        for x in range(self.game.state_manager.grid_width):
            for y in range(self.game.state_manager.grid_height):
                pygame.event.post(
                    pygame.event.Event(
                        pygame.MOUSEBUTTONDOWN,
                        {
                            "button": 1,
                            "pos": (
                                x * self.game.state_manager.grid_size,
                                y * self.game.state_manager.grid_size,
                            ),
                        },
                    )
                )
                self.game.run(
                    pygame.event.Event(
                        pygame.MOUSEBUTTONDOWN,
                        {
                            "button": 1,
                            "pos": (
                                x * self.game.state_manager.grid_size,
                                y * self.game.state_manager.grid_size,
                            ),
                        },
                    )
                )

        self.assertTrue(self.game.state_manager.won)

    def test_restart_game(self):
        self.test_number = 10
        self.game.state_manager.game_over = True

        self.assertTrue(self.game.state_manager.game_over)

        pygame.event.post(
            pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (1, 1)})
        )
        self.game.run(
            pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (1, 1)})
        )

        # self.assertFalse(self.game.state_manager.game_over)
        self.assertEqual(
            len(
                [
                    cell
                    for row in self.game.state_manager.grid
                    for cell in row
                    if cell["is_revealed"]
                ]
            ),
            0,
        )  # Ensure that no cells are revealed


if __name__ == "__main__":
    unittest.main(testRunner=JsonTestRunner(game_name="minesweeper", verbosity=2))
