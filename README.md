# Car Scroller Game

## Overview
This game is about dodging cars going in the wrong direction while gathering fuel to not break down on the road.

<!-- Don't change the tabs as it will look bad on the GitHub page. They are like this for a reason and keep them 2 tabs. -->
## Project Structure
```
car-scroller-game
├── assets
│   ├── EnemyCar.png		# Enemy car
│   ├── car1.png		# Navy car
│   ├── car2.png		# Scarlet car
│   └── car3.png		# Dust car
├── src
│   ├── main.py			# Entry point of the game
│   └── menu.py			# Menu logic of the game
├── leaderboard.json		# Leaderboard
├── README.md			# Project documentation
├── requirements.txt		# Dependencies for the game
├── run.bat			# Windows start file
└── run.sh			# Linux start file

```

## What you need
You will need a python environment installed and working on your computer to run this game as without python the game wont run.

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
Or double click run.bat on windows and run.sh on linux.

## Controls
- Use the left and right arrow keys or the A and D keys to move the car.
- Avoid oncoming enemy cars to score points.
- Gather fuel so you can keep driving.

## Contributing
Feel free to submit issues or pull requests to improve the game!

## Credits
Aim studios for the top down car sprites. https://aim-studios.itch.io/top-down-pixel-art-race-cars