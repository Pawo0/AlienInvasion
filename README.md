# Overview
This project is a classic arcade-style game called "Alien Invasion" built using Python and the Pygame library. The player controls a ship that can move left and right at the bottom of the screen and shoot bullets to destroy incoming aliens. The game tracks the player's score, level, and the number of ships (lives) remaining.  
## Preview
![image](https://github.com/user-attachments/assets/524070b2-a487-43d9-a13e-1c98d76ce2e8)
![image](https://github.com/user-attachments/assets/c4389bbf-4af3-4396-a480-e1578f5badb7)

## Features
- Ship Movement: The player can move the ship left and right.
- Shooting Bullets: The player can shoot bullets to destroy aliens.
- Alien Fleet: Aliens move across the screen and drop down periodically.
- Score Tracking: The game tracks the player's score and high score.
- Levels: The game increases in difficulty as the player progresses through levels.
- Lives: The player has a limited number of ships (lives).
## Installation
Clone the repository:
```bash
git clone https://github.com/Pawo0/AlienInvasion.git
````
Navigate to the project directory:
```bash
cd alien_invasion
```
Install the required dependencies:
```bash
pip install pygame
```

## Usage
- Run the game:
 ```bash
  python main.py
  ```
- Use the arrow keys to move the ship left and right.
- Press the spacebar to shoot bullets.
- Try to destroy all the aliens and progress through the levels.
## Project Structure
- main.py: The main entry point for the game.
- settings.py: Contains all the game settings.
- game_stats.py: Tracks game statistics.
- scoreboard.py: Manages the display of scores and levels.
- ship.py: Manages the player's ship.
- alien.py: Manages the alien fleet.
- bullet.py: Manages the bullets fired by the ship.
- images/: Contains the images used in the game.
- data/: Contains the high score data.
## Dependencies
- Python 3.x
- Pygame
## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgements
This project was inspired by Eric Matthes' book Python Crash Course.
