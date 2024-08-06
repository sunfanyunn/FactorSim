iterative_prompts = """
Create a Minesweeper grid represented as a matrix of cells, covering the entire screen.
Randomly place a predetermined number of mines throughout the grid, ensuring each mine is in a unique cell.
For each non-mine cell, calculate the number of adjacent mines and display this number on the cell.
Allow the player to reveal a cell by left-clicking on it.
If the cell is a mine, trigger a game-over state and display a "Game Over" message on the screen.
If the cell is empty (i.e., no adjacent mines), automatically reveal all connected non-mine cells.
Enable the player to flag a cell as a suspected mine by right-clicking it.
Check for a win condition by verifying that all non-mine cells have been revealed.
Display a "You Win!" message when the win condition is achieved.
Provide an option for the player to restart the game by clicking the screen after a win or game-over.
"""