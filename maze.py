import pygame
import random
 
pygame.init()
 
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Maze Game")
 
BG_DARK = (34, 40, 49)
WALL_COLOR = (119, 141, 169)
PLAYER_COLOR = (240, 84, 84)
GOAL_COLOR = (73, 160, 120)
TEXT_LIGHT = (238, 238, 238)
ACCENT_PURPLE = (157, 119, 219)
ACCENT_ORANGE = (242, 153, 74)
SHADOW = (25, 30, 36)
 
PLAYER_SIZE = 20
GOAL_SIZE = 20
 
 
def make_maze(grid_size):
    cols = WINDOW_WIDTH // grid_size
    rows = WINDOW_HEIGHT // grid_size
    grid = [[1 for _ in range(cols)] for _ in range(rows)]
 
    def carve(x, y):
        grid[y][x] = 0
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < cols and 0 <= ny < rows and grid[ny][nx] == 1:
                grid[y + dy // 2][x + dx // 2] = 0
                carve(nx, ny)
 
    carve(1, 1)
    grid[1][1] = 0
    grid[rows - 2][cols - 2] = 0
    return grid
 
 
def draw_maze(grid, grid_size):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, WALL_COLOR, (x * grid_size, y * grid_size, grid_size, grid_size))
 
 
def choose_difficulty():
    font = pygame.font.Font(None, 60)
    small_font = pygame.font.Font(None, 40)
    difficulties = [("Easy", 60), ("Normal", 40), ("Hard", 20)]
 
    while True:
        screen.fill(BG_DARK)
        title = font.render("Choose Difficulty", True, TEXT_LIGHT)
        screen.blit(title, (WINDOW_WIDTH // 2 - 175, 80))
        pygame.draw.line(screen, ACCENT_PURPLE, (150, 160), (650, 160), 2)
 
        for i, (text, size) in enumerate(difficulties):
            rect = pygame.Rect(250, 220 + i * 100, 300, 60)
            pygame.draw.rect(screen, SHADOW, rect.move(5, 5))
            pygame.draw.rect(screen, ACCENT_ORANGE if i != 1 else ACCENT_PURPLE, rect, 0, 10)
            label = small_font.render(text, True, TEXT_LIGHT)
            screen.blit(label, label.get_rect(center=rect.center))
 
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, (_, size) in enumerate(difficulties):
                    if pygame.Rect(250, 220 + i * 100, 300, 60).collidepoint(event.pos):
                        return size
 
 
def game_over_screen(message):
    font = pygame.font.Font(None, 80)
    small_font = pygame.font.Font(None, 50)
 
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(BG_DARK)
    screen.blit(overlay, (0, 0))
 
    text = font.render(message, True, TEXT_LIGHT)
    screen.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, 200))
 
    restart_rect = pygame.Rect(250, 350, 300, 70)
    pygame.draw.rect(screen, SHADOW, restart_rect.move(5, 5))
    pygame.draw.rect(screen, ACCENT_ORANGE, restart_rect, 0, 15)
    restart_text = small_font.render("Restart", True, TEXT_LIGHT)
    screen.blit(restart_text, restart_text.get_rect(center=restart_rect.center))
 
    home_rect = pygame.Rect(250, 450, 300, 70)
    pygame.draw.rect(screen, SHADOW, home_rect.move(5, 5))
    pygame.draw.rect(screen, ACCENT_PURPLE, home_rect, 0, 15)
    home_text = small_font.render("Main Menu", True, TEXT_LIGHT)
    screen.blit(home_text, home_text.get_rect(center=home_rect.center))
 
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rect.collidepoint(event.pos):
                    return "restart"
                if home_rect.collidepoint(event.pos):
                    return "home"
 
 
def play_game(grid_size):
    maze = make_maze(grid_size)
    cols, rows = len(maze[0]), len(maze)
    player_x = player_y = grid_size + PLAYER_SIZE // 2
    goal_x = (cols - 2) * grid_size + grid_size // 2
    goal_y = (rows - 2) * grid_size + grid_size // 2
 
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
 
        keys = pygame.key.get_pressed()
        new_x, new_y = player_x, player_y
        if keys[pygame.K_LEFT]: new_x -= 3
        if keys[pygame.K_RIGHT]: new_x += 3
        if keys[pygame.K_UP]: new_y -= 3
        if keys[pygame.K_DOWN]: new_y += 3
 
        player_rect = pygame.Rect(new_x - PLAYER_SIZE // 2, new_y - PLAYER_SIZE // 2, PLAYER_SIZE, PLAYER_SIZE)
        can_move = True
        grid_x, grid_y = new_x // grid_size, new_y // grid_size
 
        for y in range(max(0, grid_y - 1), min(rows, grid_y + 2)):
            for x in range(max(0, grid_x - 1), min(cols, grid_x + 2)):
                if maze[y][x] and player_rect.colliderect(
                        pygame.Rect(x * grid_size, y * grid_size, grid_size, grid_size)):
                    can_move = False
                    action = game_over_screen("You Lost!")
                    if action == "restart":
                        return play_game(grid_size)
                    elif action == "home":
                        return
 
        if can_move:
            player_x, player_y = new_x, new_y
 
        if player_rect.colliderect(pygame.Rect(goal_x - GOAL_SIZE // 2, goal_y - GOAL_SIZE // 2, GOAL_SIZE, GOAL_SIZE)):
            action = game_over_screen("You Won!")
            if action == "restart":
                return play_game(grid_size)
            elif action == "home":
                return
 
        screen.fill(BG_DARK)
        draw_maze(maze, grid_size)
        pygame.draw.circle(screen, PLAYER_COLOR, (int(player_x), int(player_y)), PLAYER_SIZE // 2)
        pygame.draw.rect(screen, GOAL_COLOR, (goal_x - GOAL_SIZE // 2, goal_y - GOAL_SIZE // 2, GOAL_SIZE, GOAL_SIZE))
        pygame.display.flip()
        clock.tick(60)
 
 
while True:
    grid_size = choose_difficulty()
    play_game(grid_size)
 
pygame.quit()
