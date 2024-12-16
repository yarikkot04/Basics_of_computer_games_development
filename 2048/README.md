# 2048

2048 is a popular puzzle game where you merge numbered tiles to reach the elusive 2048 tile. This version is implemented in Python with Pygame and integrates with a MongoDB database to save scores.

## Features

- Classic 2048 gameplay.
- Score saving and leaderboards via MongoDB.
- Background music.
- User login/registration system.
- Leaderboard screen.

## How to start

Follow these steps to set up a virtual environment, install dependencies, and run the 2048 game:

1. **Create a virtual environment** (adjust the Python version to match what is installed on your system):  
   ```bash
   python<version_on_your_pc> -m venv venv
   ```
    > *Example*: 
    ```bash
    python3.11 -m venv venv
    ```
2. **Activate the virtual environment**
    ```bash
    source venv/bin/activate
    ```
3. **Install the dependencies**
    ```bash
    pip install -r requirements.txt
    ```
4. **Run the game**
    ```bash
    python 2048.py
    ```

## How to play

**Registration**:
When you start the game for the first time, you will be prompted to enter a username and password. If you don’t have an account, choose the registration option. After registration, you can log in with your new credentials.

**Login**:
Enter your registered username and password. If the credentials are correct, you will be taken to the main menu. If not, you will be prompted to try again or register if you don’t have an account.

**View the Leaderboard**:
From the main menu, select the leaderboard option. This will display the top scores and the players who achieved them. Use this as motivation to improve your own skills!

**Playing the Game**:

- Once you select "Play," the 2048 grid will appear.
- Use the arrow keys on your keyboard to move the tiles.
- When two tiles with the same number touch, they merge into a tile with the sum of those two numbers.
- Keep merging tiles until you create a tile with the number 2048.
- Your score increases with every merge.
- If no more moves are possible and no empty spaces remain, the game is over.

You can return to the main menu or exit the game at any time.

Good luck, and have fun challenging yourself to reach the 2048 tile!

