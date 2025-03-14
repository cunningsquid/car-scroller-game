import pygame
import random
import json
import sys
import os
from menu import *

# Initialize Pygame
pygame.init()

# Load settings from file
settings_file = "settings.json"
if os.path.exists(settings_file):
	with open(settings_file, "r") as file:
		settings = json.load(file)
else:
	settings = {
		"SCREEN_WIDTH": 800,
		"SCREEN_HEIGHT": 600,
		"FULLSCREEN": False,
		"SHOW_FPS": False
	}

# Ensure all keys are present in settings
settings.setdefault("SHOW_FPS", False)

# Screen dimensions and fullscreen setting
SCREEN_WIDTH = settings["SCREEN_WIDTH"]
SCREEN_HEIGHT = settings["SCREEN_HEIGHT"]
FULLSCREEN = settings["FULLSCREEN"]
SHOW_FPS = settings["SHOW_FPS"]

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (169, 169, 169)
GREEN = (0, 255, 0)  # Color for the player's score
YELLOW = (255, 255, 0)  # Color for fuel

# Game constants
LANE_WIDTH = 100
CAR_SPEED = 5
ENEMY_CAR_SPEED = 2  # Starting speed for enemy cars
MAX_ENEMY_CAR_SPEED = 15  # maximum speed for enemy cars
SPEED_INCREMENT = 0.05  # speed increment for enemy cars
SPAWN_ENEMY_EVENT = pygame.USEREVENT + 1
INITIAL_MIN_SPAWN_INTERVAL = 800  # Initial minimum spawn interval in milliseconds
INITIAL_MAX_SPAWN_INTERVAL = 1500  # Initial maximum spawn interval in milliseconds
MIN_SPAWN_INTERVAL = 300  # Minimum spawn interval in milliseconds
MAX_SPAWN_INTERVAL = 2000  # Maximum spawn interval in milliseconds
MAX_ENEMY_CARS_AT_ONCE = 3  # Maximum number of enemy cars to spawn at once
ENEMY_CAR_INCREMENT_INTERVAL = 3000  # Interval to increase the number of enemy cars and decrease spawn interval
FUEL_DECREASE_RATE = 0.04  # Rate at which fuel decreases
FUEL_INCREMENT = 20  # Amount of fuel collected per fuel item
SPAWN_FUEL_EVENT = pygame.USEREVENT + 3
FUEL_SPAWN_INTERVAL = 4999  # Interval to spawn fuel items in milliseconds

# Create the screen
if FULLSCREEN:
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
else:
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Car Scroller Game")

# Font for score display
font = pygame.font.Font(None, 36)

# Load player car images
player_car_images = {
	"Navy": pygame.image.load(os.path.join("assets", "car1.png")),
	"Scarlet": pygame.image.load(os.path.join("assets", "car2.png")),
	"Dust": pygame.image.load(os.path.join("assets", "car3.png"))
}

# Load enemy car image
enemy_car_image = pygame.image.load(os.path.join("assets", "EnemyCar.png"))

# Load highest score, selected car, and score from game data
game_data = load_game_data()
highest_score = game_data.get("highest_score", 0)
selected_car = game_data.get("selected_car", "Navy")
score = game_data.get("score", 0)

# Ensure selected_car matches the keys in player_car_images
if selected_car not in player_car_images:
	selected_car = car_select(screen, font, SCREEN_WIDTH, SCREEN_HEIGHT, highest_score)
	save_game_data({"selected_car": selected_car, "highest_score": highest_score, "score": score})
else:
	save_game_data({"selected_car": selected_car, "highest_score": highest_score, "score": score})

# Player car class
class PlayerCar(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = player_car_images[selected_car]
		self.rect = self.image.get_rect()
		self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - SCREEN_HEIGHT // 10)
		self.fuel = 100  # Initial fuel level

	def update(self):
		keys = pygame.key.get_pressed()
		if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.rect.left > 0:
			self.rect.x -= CAR_SPEED
		if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.rect.right < SCREEN_WIDTH:
			self.rect.x += CAR_SPEED
		self.fuel -= FUEL_DECREASE_RATE  # Decrease fuel over time
		if self.fuel <= 0:
			self.kill()  # End the game if fuel runs out

	def set_image(self, car_image):
		self.image = car_image
		self.rect = self.image.get_rect(center=self.rect.center)

# Enemy car class
class EnemyCar(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = enemy_car_image
		self.rect = self.image.get_rect()
		self.rect.y = -100
		self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
		while pygame.sprite.spritecollideany(self, enemy_cars):
			self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)

	def update(self):
		self.rect.y += ENEMY_CAR_SPEED
		if self.rect.top > SCREEN_HEIGHT:
			self.kill()

# Fuel item class
class FuelItem(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.Surface((30, 30))
		self.image.fill(YELLOW)
		self.rect = self.image.get_rect()
		self.rect.y = -30
		self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
		while pygame.sprite.spritecollideany(self, enemy_cars) or pygame.sprite.spritecollideany(self, fuel_items):
			self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)

	def update(self):
		self.rect.y += ENEMY_CAR_SPEED
		if self.rect.top > SCREEN_HEIGHT:
			self.kill()

# Create sprite groups
all_sprites = pygame.sprite.Group()
enemy_cars = pygame.sprite.Group()
fuel_items = pygame.sprite.Group()

# Create player car
player_car = PlayerCar()
all_sprites.add(player_car)

# Set up the enemy car spawn event with initial intervals
pygame.time.set_timer(SPAWN_ENEMY_EVENT, random.randint(INITIAL_MIN_SPAWN_INTERVAL, INITIAL_MAX_SPAWN_INTERVAL))

# Set up the enemy car increment event
pygame.time.set_timer(pygame.USEREVENT + 2, ENEMY_CAR_INCREMENT_INTERVAL)

# Set up the fuel item spawn event
pygame.time.set_timer(SPAWN_FUEL_EVENT, FUEL_SPAWN_INTERVAL)

# Load leaderboard
leaderboard_file = "leaderboard.json"
if os.path.exists(leaderboard_file):
	try:
		with open(leaderboard_file, "r") as file:
			leaderboard = json.load(file)
	except json.JSONDecodeError:
		leaderboard = []
else:
	leaderboard = []

def reset_game():
	global all_sprites, enemy_cars, fuel_items, player_car, score, ENEMY_CAR_SPEED, MAX_ENEMY_CARS_AT_ONCE, MIN_SPAWN_INTERVAL, MAX_SPAWN_INTERVAL, running, selected_car
	all_sprites.empty()
	enemy_cars.empty()
	fuel_items.empty()
	player_car = PlayerCar()
	all_sprites.add(player_car)
	score = 0
	ENEMY_CAR_SPEED = 2
	MAX_ENEMY_CARS_AT_ONCE = 3
	MIN_SPAWN_INTERVAL = 200
	MAX_SPAWN_INTERVAL = 2000
	pygame.time.set_timer(SPAWN_ENEMY_EVENT, random.randint(INITIAL_MIN_SPAWN_INTERVAL, INITIAL_MAX_SPAWN_INTERVAL))
	pygame.time.set_timer(pygame.USEREVENT + 2, ENEMY_CAR_INCREMENT_INTERVAL)
	pygame.time.set_timer(SPAWN_FUEL_EVENT, FUEL_SPAWN_INTERVAL)
	running = True

def game_over():
	global running, leaderboard, highest_score, selected_car
	# Save the highest score
	if score > highest_score:
		highest_score = score

	# Save game data
	save_game_data({"selected_car": selected_car, "highest_score": highest_score, "score": score})

	# Game over, show leaderboard and get player name
	player_name = get_player_name(screen, font, SCREEN_WIDTH, SCREEN_HEIGHT)
	leaderboard.append({"name": player_name, "score": score, "car": selected_car})
	leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)
	save_leaderboard(leaderboard, leaderboard_file)
	show_leaderboard(screen, font, SCREEN_WIDTH, SCREEN_HEIGHT, player_name, score, selected_car)

	ask_restart()

def ask_restart():
	screen.fill(GRAY)
	ask_text = font.render("Do you want to restart? (Y/N)", True, BLACK)
	screen.blit(ask_text, (SCREEN_WIDTH // 2 - ask_text.get_width() // 2, SCREEN_HEIGHT // 2))
	pygame.display.flip()

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_y:
					reset_game()
					return
				elif event.key == pygame.K_n or event.key == pygame.K_ESCAPE:
					pygame.quit()
					sys.exit()

def main_game_loop():
	global running, score, score_increment_timer, SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN, ENEMY_CAR_SPEED, MAX_ENEMY_CARS_AT_ONCE, MIN_SPAWN_INTERVAL, MAX_SPAWN_INTERVAL, SHOW_FPS, selected_car
	running = True
	clock = pygame.time.Clock()
	score = 0
	score_increment_timer = 0

	SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN, SHOW_FPS = main_menu(screen, font, SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN, SHOW_FPS)

	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				ask_restart()
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				pause_menu(screen, font, SCREEN_WIDTH, SCREEN_HEIGHT)
			elif event.type == SPAWN_ENEMY_EVENT:
				enemy_car = EnemyCar()
				all_sprites.add(enemy_car)
				enemy_cars.add(enemy_car)
				# Set the next spawn interval to a random value within an increasing range
				next_spawn_interval = random.randint(MIN_SPAWN_INTERVAL, MAX_SPAWN_INTERVAL)
				pygame.time.set_timer(SPAWN_ENEMY_EVENT, next_spawn_interval)
			elif event.type == SPAWN_FUEL_EVENT:
				fuel_item = FuelItem()
				while pygame.sprite.spritecollideany(fuel_item, enemy_cars) or pygame.sprite.spritecollideany(fuel_item, fuel_items):
					fuel_item.rect.x = random.randint(0, SCREEN_WIDTH - fuel_item.rect.width)
				all_sprites.add(fuel_item)
				fuel_items.add(fuel_item)
			elif event.type == pygame.USEREVENT + 2:
				# Increase the number of enemy cars and decrease spawn interval
				MAX_ENEMY_CARS_AT_ONCE += 1
				MIN_SPAWN_INTERVAL = max(100, MIN_SPAWN_INTERVAL - 100)
				MAX_SPAWN_INTERVAL = max(300, MAX_SPAWN_INTERVAL - 200)

		# Update sprites
		all_sprites.update()

		# Check for collisions with enemy cars
		if pygame.sprite.spritecollideany(player_car, enemy_cars):
			running = False

		# Check for collisions with fuel items
		fuel_collisions = pygame.sprite.spritecollide(player_car, fuel_items, True)
		for fuel_item in fuel_collisions:
			player_car.fuel = min(100, player_car.fuel + FUEL_INCREMENT)  # Increase fuel but cap at 100

		# Check if fuel is depleted
		if player_car.fuel <= 0:
			running = False

		# Increment score over time
		score_increment_timer += clock.get_time()
		if score_increment_timer >= 1000:  # Increment score every second
			score += 1
			score_increment_timer = 0

		# Unlock cars based on score
		if score >= 150:
			unlocked_cars = ["Navy", "Scarlet", "Dust"]
		elif score >= 75:
			unlocked_cars = ["Navy", "Scarlet"]
		else:
			unlocked_cars = ["Navy"]

		# Draw everything
		screen.fill(GRAY)
		all_sprites.draw(screen)

		# Draw the score
		score_text = font.render(f"Score: {score}", True, BLACK)
		screen.blit(score_text, (10, 10))

		# Draw the fuel gauge
		fuel_text = font.render(f"Fuel: {int(player_car.fuel)}%", True, BLACK)
		screen.blit(fuel_text, (10, 40))

		 # Draw the FPS counter if enabled
		if SHOW_FPS:
			fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, BLACK)
			screen.blit(fps_text, (SCREEN_WIDTH - 100, 10))

		# Flip the display
		pygame.display.flip()

		# Cap the frame rate
		clock.tick(60)

		# Increase enemy car speed over time, but cap it at MAX_ENEMY_CAR_SPEED
		ENEMY_CAR_SPEED = min(MAX_ENEMY_CAR_SPEED, ENEMY_CAR_SPEED + SPEED_INCREMENT * clock.get_time() / 1000.0)

		# Update player car image if selected car changes
		new_selected_car = load_selected_car()
		if new_selected_car != selected_car:
			selected_car = new_selected_car
			player_car.set_image(player_car_images[selected_car])

while True:
	main_game_loop()
	game_over()