import pygame
import random


class StateManager:
    def __init__(self):
        # Initialize game state
        self.width = 400
        self.height = 400
        self.grid_size = 20
        self.grid_width = self.width // self.grid_size
        self.grid_height = self.height // self.grid_size
        self.fps = 60

        # Colors
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.gray = (192, 192, 192)
        self.dark_gray = (128, 128, 128)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)

        # Game Constants
        self.num_mines = 1

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.grid = []
        self.game_over = False
        self.won = False
        self.revealed_non_mine_cells = 0
        self.clock = pygame.time.Clock()


def reset_game(state_manager):
    # Reset game state variables
    state_manager.game_over = False
    state_manager.won = False
    state_manager.revealed_non_mine_cells = 0

    # Create the grid
    state_manager.grid = [
        [
            {
                "is_mine": False,
                "is_revealed": False,
                "is_flagged": False,
                "adjacent_mines": 0,
            }
            for _ in range(state_manager.grid_height)
        ]
        for _ in range(state_manager.grid_width)
    ]

    # Place mines randomly
    mines_placed = 0
    while mines_placed < state_manager.num_mines:
        x, y = random.randint(0, state_manager.grid_width - 1), random.randint(
            0, state_manager.grid_height - 1
        )
        cell = state_manager.grid[x][y]
        if not cell["is_mine"]:
            cell["is_mine"] = True
            mines_placed += 1

    # Calculate adjacent mines
    for x in range(state_manager.grid_width):
        for y in range(state_manager.grid_height):
            cell = state_manager.grid[x][y]
            if not cell["is_mine"]:
                cell["adjacent_mines"] = count_adjacent_mines(state_manager, x, y)


def count_adjacent_mines(state_manager, x, y):
    count = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if (
                0 <= nx < state_manager.grid_width
                and 0 <= ny < state_manager.grid_height
            ):
                if state_manager.grid[nx][ny]["is_mine"]:
                    count += 1
    return count


def reveal_cell(state_manager, x, y):
    if state_manager.game_over or not (
        0 <= x < state_manager.grid_width and 0 <= y < state_manager.grid_height
    ):
        return

    cell = state_manager.grid[x][y]
    if cell["is_flagged"] or cell["is_revealed"]:
        return
    cell["is_revealed"] = True
    if cell["is_mine"]:
        state_manager.game_over = True
    else:
        state_manager.revealed_non_mine_cells += 1
        if (
            state_manager.revealed_non_mine_cells
            == (state_manager.grid_width * state_manager.grid_height)
            - state_manager.num_mines
        ):
            state_manager.won = True

        # Reveal adjacent cells if there are no adjacent mines
        if cell["adjacent_mines"] == 0:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    nx, ny = x + dx, y + dy
                    reveal_cell(state_manager, nx, ny)


def toggle_flag(state_manager, x, y):
    if state_manager.game_over or not (
        0 <= x < state_manager.grid_width and 0 <= y < state_manager.grid_height
    ):
        return

    cell = state_manager.grid[x][y]
    if not cell["is_revealed"]:
        cell["is_flagged"] = not cell["is_flagged"]


def render(state_manager):
    state_manager.screen.fill(state_manager.black)

    # Draw each cell
    for x in range(state_manager.grid_width):
        for y in range(state_manager.grid_height):
            cell = state_manager.grid[x][y]
            rect = pygame.Rect(
                x * state_manager.grid_size,
                y * state_manager.grid_size,
                state_manager.grid_size,
                state_manager.grid_size,
            )

            # Determine color based on cell state
            color = state_manager.gray
            if cell["is_revealed"]:
                color = state_manager.dark_gray
                if cell["is_mine"]:
                    color = state_manager.red
            elif cell["is_flagged"]:
                color = state_manager.green

            pygame.draw.rect(state_manager.screen, color, rect)

            # Render the number of adjacent mines if the cell is revealed
            if (
                cell["is_revealed"]
                and not cell["is_mine"]
                and cell["adjacent_mines"] > 0
            ):
                font = pygame.font.Font(None, 24)
                text = font.render(
                    str(cell["adjacent_mines"]), True, state_manager.white
                )
                text_rect = text.get_rect(
                    center=(
                        x * state_manager.grid_size + state_manager.grid_size // 2,
                        y * state_manager.grid_size + state_manager.grid_size // 2,
                    )
                )
                state_manager.screen.blit(text, text_rect)

    # Draw grid lines
    for x in range(0, state_manager.width, state_manager.grid_size):
        pygame.draw.line(
            state_manager.screen, state_manager.black, (x, 0), (x, state_manager.height)
        )
    for y in range(0, state_manager.height, state_manager.grid_size):
        pygame.draw.line(
            state_manager.screen, state_manager.black, (0, y), (state_manager.width, y)
        )

    # Draw game over or win message
    if state_manager.game_over:
        font = pygame.font.Font(None, 48)
        message = "Game Over"
        text = font.render(message, True, state_manager.white)
        text_rect = text.get_rect(
            center=(state_manager.width // 2, state_manager.height // 2)
        )
        state_manager.screen.blit(text, text_rect)
    elif state_manager.won:
        font = pygame.font.Font(None, 48)
        message = "You Win!"
        text = font.render(message, True, state_manager.white)
        text_rect = text.get_rect(
            center=(state_manager.width // 2, state_manager.height // 2)
        )
        state_manager.screen.blit(text, text_rect)

    pygame.display.flip()
    state_manager.clock.tick(state_manager.fps)


class Game:
    def __init__(self):
        self.state_manager = StateManager()
        reset_game(self.state_manager)  # Initialize game state

    def run(self, event):
        state_manager = self.state_manager
        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            x //= state_manager.grid_size
            y //= state_manager.grid_size
            if event.button == 1:  # Left click
                if not state_manager.game_over:
                    reveal_cell(state_manager, x, y)
            elif event.button == 3:  # Right click
                if not state_manager.game_over:
                    toggle_flag(state_manager, x, y)

        render(state_manager)
        return not state_manager.game_over


if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            running = game.run(event)
    pygame.quit()
