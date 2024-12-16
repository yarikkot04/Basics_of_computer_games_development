# Math Quiz
Math Quiz is an engaging single-player game that challenges your arithmetic skills under time pressure. Answer as many math questions as you can before the timer runs out, level up as you progress, and aim for the highest score!

## Features
- **Dynamic Math Questions**: Addition, subtraction, multiplication, and division problems.
- **Multiple Levels**: Increase the difficulty as you advance through levels.
- **Timer-Based Gameplay**: Race against the clock to maximize your score.
- **Score Tracking**: Keep track of your current score and best score.
- **Persistent Best Score**: Your best score is saved and loaded automatically.
- **Intuitive Graphical Interface**: Built with Pygame for a smooth user experience.
- **Responsive Controls**: Use keyboard inputs to select your answers and navigate menus.

## How to Start
Follow these steps to set up a virtual environment, install dependencies, and run the Math Quiz game:

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
    python math_quiz.py
    ```

## How to Play
### Main Menu:
- **Start Game:** Press `ENTER` to begin a new math quiz.
- **Exit Game:** Press `ESC` to exit the application.
- **Best Score:** Your highest score is displayed on the main menu.

### Gameplay:
- Question Display: 
  - A math question appears at the top of the screen.
  - Four possible answers are listed below the question, labeled `1` to `4`.

### Selecting an Answer:

- Press the number key (`1`, `2`, `3`, or `4`) corresponding to your chosen answer.
- Correct answers add points and extend the timer.
- Incorrect answers deduct time from the timer.

### Timer:

- You start with a set amount of time (e.g., 60 seconds).
- Correct answers can add time, while incorrect answers reduce it.
- The game ends when the timer reaches zero.

### Scoring:

- Earn points for each correct answer.
- Accumulate points to increase your score and level up.
- Each level increases the difficulty by introducing larger numbers.

### Levels:

- Advance to higher levels by reaching score milestones.
- Higher levels feature more challenging math problems.

### Game Over:
- **Game Over Screen**:
  - Displays your final score and the best score achieved.
  - Options to:
    - **Restart Game:** Press `ENTER` to play again.
    - **Return to Main Menu:** Press `Q` to go back to the main menu.

### Controls:
- **Answer Selection:** Press `1`, `2`, `3`, or `4 `to select an answer.
- **Start Game:** Press `ENTER` from the main menu.
- **Exit Game:** Press `ESC` from the main menu or `Q` from the game over screen.
- **Restart Game:** Press `ENTER` from the game over screen.