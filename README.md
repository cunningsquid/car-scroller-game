# Car Scroller Game

## Overview
This game is about dodging cars going in the wrong direction while gathering fuel to not break down on the road.

## Project Structure
```
car-scroller-game
├── src
│   ├── main.py           # Entry point of the game
│   └── menu.py           # Menu logic of the game
├── assets
│   ├── EnemySprite.png   # Enemy car sprite
│   └── PlayerSprite.png  # Player car sprite
├── requirements.txt      # Dependencies for the game
├── README.md             # Project documentation
├── leaderboard.json      # Leaderboard
└── setting.json          # Saved settings

```

## What you need
You will need a python environment installed and working on your computer to run this game as without python the game wont run. Pyrhon 3.12 is recommended.

## Installation
1. Clone the repository:
	```
	git clone https://github.com/cunningsquid/car-scroller-game.git
	```
2. Navigate to the project directory:
	```
	cd car-scroller-game
	```
3. Install the required dependencies:
	```
	pip install -r requirements.txt
	```

## Running the Game
To start the game, run the following command:
```
python src/main.py
```

## Controls
- Use the left and right arrow keys or the A and D keys to move the car.
- Avoid oncoming enemy cars to score points.
- Gather fuel so you can keep driving.

## Contributing
Feel free to submit issues or pull requests to improve the game!