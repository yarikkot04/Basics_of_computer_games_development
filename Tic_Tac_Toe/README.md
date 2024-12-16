# Tic-Tac-Toe

Tic-Tac-Toe is a classic two-player game where each player takes turns placing their mark (X or O) on a 3x3 grid. The first player to line up three of their marks in a row, column, or diagonal wins! This version also offers a single-player mode against the computer.

## Features

- Classic Tic-Tac-Toe gameplay.
- Two modes:
  - Player vs. Player (PVP)
  - Player vs. Computer (AI)
- Intuitive graphical interface built with Pygame.
- Visual indication of the winning line.

## How to Start

Follow these steps to set up a virtual environment, install dependencies, and run the Tic-Tac-Toe game:

1. **Create a virtual environment** (adjust the Python version to match what is installed on your system):  
   ```bash
   python<version_on_your_pc> -m venv venv
   ```
  > *Example*:
  ```bash
  python3.11 -m venv venv
  ```

2. **Activate the virtual environment:**
  ```bash
  source venv/bin/activate
  ```

3. **Install the dependencies:**
  ```bash
  pip install -r requirements.txt
  ```
4. **Run the game:**
  ```bash
  python tic-tac-toe.py
  ```

After running the last command, the game window should appear, and you will see the main menu.

## How to Play
**Main Menu:**

- Choose to play against the computer or play a 1 vs. 1 match on the same device.
- After selecting the mode, the game board will appear.

**Player vs. Player:**

- Click on any empty cell to place your mark.
- The first player to get three marks in a line (horizontally, vertically, or diagonally) wins.
- If all cells are filled and no one wins, the game results in a draw.
- After a win or draw, you can choose to play again or return to the main menu.

**Player vs. Computer:**

- You start as 'X'.
- Click on any empty cell to make your move.
- The computer will then place its 'O' mark.
- Same winning conditions apply.
- If you win, lose, or draw, you can restart or return to the main menu.

**Controls:**

- Use your mouse to select cells and to interact with buttons.
- After the game ends, select “Play Again” to start a new match or “Main Menu” to change the mode.

Have fun testing your skills against friends or challenging the computer!