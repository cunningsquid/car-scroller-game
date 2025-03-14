import pygame
import json
import sys
import os

def load_settings():
	try:
		with open("settings.json", "r") as file:
			return json.load(file)
	except FileNotFoundError:
		return {"SCREEN_WIDTH": 800, "SCREEN_HEIGHT": 600, "FULLSCREEN": False, "SHOW_FPS": False}

def main_menu(screen, font, SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN, SHOW_FPS):
	options = ["Start Game", "Options", "Select Car", "Quit"]
	selected_option = 0

	while True:
		screen.fill((169, 169, 169))  # GRAY
		title_text = font.render("Car Scroller Game", True, (0, 0, 0))  
		screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))

		for i, option in enumerate(options):
			color = (0, 0, 0) if i != selected_option else (255, 0, 0)
			option_text = font.render(option, True, color)
			screen.blit(option_text, (SCREEN_WIDTH // 2 - option_text.get_width() // 2, SCREEN_HEIGHT // 2 - 40 + i * 40))

		pygame.display.flip()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					if selected_option == 0:
						return SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN, SHOW_FPS
					elif selected_option == 1:
						SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN, SHOW_FPS, screen = options_menu(screen, font, SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN, SHOW_FPS)
					elif selected_option == 2:
						selected_car = car_select(screen, font, SCREEN_WIDTH, SCREEN_HEIGHT, load_highest_score())
						print(f"Selected Car: {selected_car}")  # You can handle the selected car as needed
					elif selected_option == 3:
						pygame.quit()
						sys.exit()
				elif event.key == pygame.K_UP:
					selected_option = (selected_option - 1) % len(options)
				elif event.key == pygame.K_DOWN:
					selected_option = (selected_option + 1) % len(options)

def options_menu(screen, font, SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN, SHOW_FPS):
	options = ["Resolution", "Fullscreen", "Show FPS", "Back"]
	resolutions = [(800, 600), (1024, 768), (1280, 720), (1366, 768), (1920, 1080), (2560, 1440), (3840, 2160)]
	current_resolution_index = resolutions.index((SCREEN_WIDTH, SCREEN_HEIGHT))
	selected_option = 0
	temp_width, temp_height, temp_fullscreen, temp_show_fps = SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN, SHOW_FPS
	
	while True:
		screen.fill((169, 169, 169))
		title_text = font.render("Options", True, (0, 0, 0))
		screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))

		for i, option in enumerate(options):
			if option == "Resolution":
				option_text = f"Resolution: {temp_width}x{temp_height}"
			elif option == "Fullscreen":
				option_text = f"Fullscreen: {'On' if temp_fullscreen else 'Off'}"
			elif option == "Show FPS":
				option_text = f"Show FPS: {'On' if temp_show_fps else 'Off'}"
			else:
				option_text = option

			color = (0, 0, 0) if i != selected_option else (255, 0, 0)
			option_text_rendered = font.render(option_text, True, color)
			screen.blit(option_text_rendered, (SCREEN_WIDTH // 2 - option_text_rendered.get_width() // 2, SCREEN_HEIGHT // 2 - 60 + i * 40))

		pygame.display.flip()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					if selected_option == 0:
						current_resolution_index = (current_resolution_index + 1) % len(resolutions)
						temp_width, temp_height = resolutions[current_resolution_index]
					elif selected_option == 1:
						temp_fullscreen = not temp_fullscreen
					elif selected_option == 2:
						temp_show_fps = not temp_show_fps
					elif selected_option == 3:
						SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN, SHOW_FPS = temp_width, temp_height, temp_fullscreen, temp_show_fps
						if FULLSCREEN:
							screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
						else:
							screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
						save_settings(SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN, SHOW_FPS)
						return SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN, SHOW_FPS, screen
				elif event.key == pygame.K_UP:
					selected_option = (selected_option - 1) % len(options)
				elif event.key == pygame.K_DOWN:
					selected_option = (selected_option + 1) % len(options)

def save_settings(SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN, SHOW_FPS):
	settings = {
		"SCREEN_WIDTH": SCREEN_WIDTH,
		"SCREEN_HEIGHT": SCREEN_HEIGHT,
		"FULLSCREEN": FULLSCREEN,
		"SHOW_FPS": SHOW_FPS
	}
	with open("settings.json", "w") as file:
		json.dump(settings, file)

def get_player_name(screen, font, SCREEN_WIDTH, SCREEN_HEIGHT):
	player_name = ""
	while True:
		screen.fill((169, 169, 169))
		title_text = font.render("Enter Your Name", True, (0, 0, 0))
		name_text = font.render(player_name, True, (0, 0, 0))
		instructions_text = font.render("Press ENTER to Submit", True, (0, 0, 0))
		screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 80))
		screen.blit(name_text, (SCREEN_WIDTH // 2 - name_text.get_width() // 2, SCREEN_HEIGHT // 2 - 20))
		screen.blit(instructions_text, (SCREEN_WIDTH // 2 - instructions_text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))
		pygame.display.flip()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					return player_name.strip()[:15]  # Limit name to 15 characters
				elif event.key == pygame.K_BACKSPACE:
					player_name = player_name[:-1]
				else:
					if len(player_name) < 15:
						player_name += event.unicode

def load_leaderboard(leaderboard_file):
	if os.path.exists(leaderboard_file):
		with open(leaderboard_file, "r") as file:
			return json.load(file)
	return []

def save_leaderboard(leaderboard, leaderboard_file):
	with open(leaderboard_file, "w") as file:
		json.dump(leaderboard, file, indent=4)

def show_leaderboard(screen, font, SCREEN_WIDTH, SCREEN_HEIGHT, player_name, player_score, selected_car):
	leaderboard = load_leaderboard("leaderboard.json")
	options = ["Restart", "Quit"]
	selected_option = 0

	while True:
		screen.fill((169, 169, 169))  # GRAY
		title_text = font.render("Leaderboard", True, (0, 0, 0))  # BLACK
		screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

		# Display the player's score
		player_score_text = font.render(f"Your Score: {player_score}", True, (0, 0, 0))  # BLACK
		screen.blit(player_score_text, (SCREEN_WIDTH // 2 - player_score_text.get_width() // 2, 100))

		# Display the leaderboard
		for i, entry in enumerate(leaderboard[:10]):
			color = (0, 255, 0) if entry['name'] == player_name and entry['score'] == player_score and entry['car'] == selected_car else (0, 0, 0)  # GREEN for player
			entry_text = font.render(f"{i + 1}. {entry['name']} - {entry['score']} - {entry['car']}", True, color)
			screen.blit(entry_text, (SCREEN_WIDTH // 2 - entry_text.get_width() // 2, 150 + i * 30))

		# Display options
		for i, option in enumerate(options):
			color = (0, 0, 0) if i != selected_option else (255, 0, 0)
			option_text = font.render(option, True, color)
			screen.blit(option_text, (SCREEN_WIDTH // 2 - option_text.get_width() // 2, SCREEN_HEIGHT - 100 + i * 30))
		
		pygame.display.flip()

		# Wait for player input
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					if selected_option == 0:
						return True
					elif selected_option == 1:
						pygame.quit()
						sys.exit()
				elif event.key == pygame.K_UP:
					selected_option = (selected_option - 1) % len(options)
				elif event.key == pygame.K_DOWN:
					selected_option = (selected_option + 1) % len(options)

def pause_menu(screen, font, SCREEN_WIDTH, SCREEN_HEIGHT):
	options = ["Resume", "Quit"]
	selected_option = 0

	while True:
		screen.fill((169, 169, 169))
		title_text = font.render("Paused", True, (0, 0, 0))
		screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 80))

		for i, option in enumerate(options):
			color = (0, 0, 0) if i != selected_option else (255, 0, 0)
			option_text = font.render(f"{option}", True, color)
			screen.blit(option_text, (SCREEN_WIDTH // 2 - option_text.get_width() // 2, SCREEN_HEIGHT // 2 - 20 + i * 40))

		pygame.display.flip()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					if selected_option == 0:
						return
					elif selected_option == 1:
						pygame.quit()
						sys.exit()
				elif event.key == pygame.K_UP:
					selected_option = (selected_option - 1) % len(options)
				elif event.key == pygame.K_DOWN:
					selected_option = (selected_option + 1) % len(options)

def save_selected_car(selected_car):
	game_data = load_game_data()
	game_data["selected_car"] = selected_car
	save_game_data(game_data)

def load_selected_car():
	game_data = load_game_data()
	return game_data.get("selected_car", "Navy")

def save_highest_score(highest_score):
	game_data = load_game_data()
	game_data["highest_score"] = highest_score
	save_game_data(game_data)

def load_highest_score():
	game_data = load_game_data()
	return game_data.get("highest_score", 0)

def car_select(screen, font, SCREEN_WIDTH, SCREEN_HEIGHT, highest_score):
	car_images = {
		"Navy": pygame.image.load(os.path.join("assets", "car1.png")),
		"Scarlet": pygame.image.load(os.path.join("assets", "car2.png")),
		"Dust": pygame.image.load(os.path.join("assets", "car3.png"))
	}
	selected_car = load_selected_car()
	unlocked_cars = ["Navy"]
	if highest_score >= 75:
		unlocked_cars.append("Scarlet")
	if highest_score >= 150:
		unlocked_cars.append("Dust")
	car_options = ["Navy", "Scarlet", "Dust"]
	selected_option = car_options.index(selected_car)

	while True:
		screen.fill((169, 169, 169))
		title_text = font.render("Select Your Car", True, (0, 0, 0))
		screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 80))

		for i, car in enumerate(car_options):
			if car == "Scarlet" and "Scarlet" not in unlocked_cars:
				car_text = "Scarlet (Locked) 75+ Score Required"
			elif car == "Dust" and "Dust" not in unlocked_cars:
				car_text = "Dust (Locked) 150+ Score Required"
			else:
				car_text = car

			color = (0, 0, 0) if i != selected_option else (255, 0, 0)
			car_text_rendered = font.render(car_text, True, color)
			screen.blit(car_text_rendered, (SCREEN_WIDTH // 2 - car_text_rendered.get_width() // 2, SCREEN_HEIGHT // 2 - 20 + i * 40))

		confirm_text = font.render("Press ENTER to Confirm", True, (0, 0, 0))
		screen.blit(confirm_text, (SCREEN_WIDTH // 2 - confirm_text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))
		
		# Display the selected car image
		car_image = car_images[car_options[selected_option]]
		car_image_rect = car_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200))
		screen.blit(car_image, car_image_rect)
		
		pygame.display.flip()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					if (selected_option == 1 and "Scarlet" not in unlocked_cars) or (selected_option == 2 and "Dust" not in unlocked_cars):
						continue
					selected_car = car_options[selected_option]
					save_selected_car(selected_car)
					return selected_car
				elif event.key == pygame.K_UP:
					selected_option = (selected_option - 1) % len(car_options)
				elif event.key == pygame.K_DOWN:
					selected_option = (selected_option + 1) % len(car_options)

def save_game_data(data):
	with open("game_data.json", "w") as file:
		json.dump(data, file)

def load_game_data():
	if os.path.exists("game_data.json"):
		with open("game_data.json", "r") as file:
			return json.load(file)
	return {}