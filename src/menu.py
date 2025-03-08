import pygame
import json
import sys
import os

def load_settings():
    if os.path.exists("settings.json"):
        with open("settings.json", "r") as file:
            return json.load(file)
    return {"SCREEN_WIDTH": 800, "SCREEN_HEIGHT": 600, "FULLSCREEN": False}

def main_menu(screen, font, SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN):
    while True:
        screen.fill((169, 169, 169))  # GRAY
        title_text = font.render("Car Scroller Game", True, (0, 0, 0))
        start_text = font.render("Press ENTER to Start", True, (0, 0, 0))
        options_text = font.render("Press O for Options", True, (0, 0, 0))
        quit_text = font.render("Press ESC to Quit", True, (0, 0, 0))
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 80))
        screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2 - 20))
        screen.blit(options_text, (SCREEN_WIDTH // 2 - options_text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))
        screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 60))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN
                elif event.key == pygame.K_o:
                    SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN, screen = options_menu(screen, font, SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN)
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def options_menu(screen, font, SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN):
    resolutions = [(800, 600), (1024, 768), (1280, 720), (1920, 1080)]
    current_resolution_index = resolutions.index((SCREEN_WIDTH, SCREEN_HEIGHT))
    temp_width, temp_height, temp_fullscreen = SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN
    
    while True:
        screen.fill((169, 169, 169))
        title_text = font.render("Options", True, (0, 0, 0))
        resolution_text = font.render(f"Resolution: {temp_width}x{temp_height}", True, (0, 0, 0))
        fullscreen_text = font.render(f"Fullscreen: {'On' if temp_fullscreen else 'Off'}", True, (0, 0, 0))
        instructions_text1 = font.render("Press LEFT/RIGHT to change resolution", True, (0, 0, 0))
        instructions_text2 = font.render("F to toggle fullscreen", True, (0, 0, 0))
        instructions_text3 = font.render("ENTER to apply, ESC to go back", True, (0, 0, 0))
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 80))
        screen.blit(resolution_text, (SCREEN_WIDTH // 2 - resolution_text.get_width() // 2, SCREEN_HEIGHT // 2 - 20))
        screen.blit(fullscreen_text, (SCREEN_WIDTH // 2 - fullscreen_text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))
        screen.blit(instructions_text1, (SCREEN_WIDTH // 2 - instructions_text1.get_width() // 2, SCREEN_HEIGHT // 2 + 60))
        screen.blit(instructions_text2, (SCREEN_WIDTH // 2 - instructions_text2.get_width() // 2, SCREEN_HEIGHT // 2 + 100))
        screen.blit(instructions_text3, (SCREEN_WIDTH // 2 - instructions_text3.get_width() // 2, SCREEN_HEIGHT // 2 + 140))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_resolution_index = (current_resolution_index - 1) % len(resolutions)
                    temp_width, temp_height = resolutions[current_resolution_index]
                elif event.key == pygame.K_RIGHT:
                    current_resolution_index = (current_resolution_index + 1) % len(resolutions)
                    temp_width, temp_height = resolutions[current_resolution_index]
                elif event.key == pygame.K_f:
                    temp_fullscreen = not temp_fullscreen
                elif event.key == pygame.K_RETURN:
                    SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN = temp_width, temp_height, temp_fullscreen
                    if FULLSCREEN:
                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                    save_settings(SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN)
                elif event.key == pygame.K_ESCAPE:
                    return SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN, screen

def save_settings(SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN):
    settings = {
        "SCREEN_WIDTH": SCREEN_WIDTH,
        "SCREEN_HEIGHT": SCREEN_HEIGHT,
        "FULLSCREEN": FULLSCREEN
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

def show_leaderboard(screen, font, SCREEN_WIDTH, SCREEN_HEIGHT, player_name, player_score):
    leaderboard = load_leaderboard("leaderboard.json")
    screen.fill((169, 169, 169))  # GRAY
    title_text = font.render("Leaderboard", True, (0, 0, 0))  # BLACK
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

    # Display the player's score
    player_score_text = font.render(f"Your Score: {player_score}", True, (0, 0, 0))  # BLACK
    screen.blit(player_score_text, (SCREEN_WIDTH // 2 - player_score_text.get_width() // 2, 100))

    # Display the leaderboard
    for i, entry in enumerate(leaderboard[:10]):
        color = (0, 255, 0) if entry['name'] == player_name and entry['score'] == player_score else (0, 0, 0)  # GREEN for player
        entry_text = font.render(f"{i + 1}. {entry['name']} - {entry['score']}", True, color)
        screen.blit(entry_text, (SCREEN_WIDTH // 2 - entry_text.get_width() // 2, 150 + i * 30))

    instructions_text = font.render("Press R to Restart or ESC to Quit", True, (0, 0, 0))  # BLACK
    screen.blit(instructions_text, (SCREEN_WIDTH // 2 - instructions_text.get_width() // 2, SCREEN_HEIGHT - 50))
    
    pygame.display.flip()

    # Wait for player input
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def pause_menu(screen, font, SCREEN_WIDTH, SCREEN_HEIGHT):
    while True:
        screen.fill((169, 169, 169))
        title_text = font.render("Paused", True, (0, 0, 0))
        resume_text = font.render("Press R to Resume", True, (0, 0, 0))
        quit_text = font.render("Press ESC to Quit", True, (0, 0, 0))
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 80))
        screen.blit(resume_text, (SCREEN_WIDTH // 2 - resume_text.get_width() // 2, SCREEN_HEIGHT // 2 - 20))
        screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()