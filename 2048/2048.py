import pygame
import sys
import random
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=False)
db = client["mygameDB"]
users_collection = db["users"]
scores_collection = db["scores"]

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("./music/calm_music.mp3")
pygame.mixer.music.set_volume(0.15)
pygame.mixer.music.play(-1)

WIDTH = 500
HEIGHT = 600

BACKGROUND_COLOR = (250, 248, 239)
EMPTY_CELL_COLOR = (204, 192, 179)

TILE_COLORS = {
    2:    (238, 228, 218),
    4:    (237, 224, 200),
    8:    (242, 177, 121),
    16:   (245, 149, 99),
    32:   (246, 124, 95),
    64:   (246, 94, 59),
    128:  (237, 207, 114),
    256:  (237, 204, 97),
    512:  (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}

TILE_TEXT_COLORS = {
    2:    (119, 110, 101),
    4:    (119, 110, 101),
    8:    (249, 246, 242),
    16:   (249, 246, 242),
    32:   (249, 246, 242),
    64:   (249, 246, 242),
    128:  (249, 246, 242),
    256:  (249, 246, 242),
    512:  (249, 246, 242),
    1024: (249, 246, 242),
    2048: (249, 246, 242)
}

GRID_SIZE = 4
CELL_SIZE = 100
CELL_PADDING = 10

board_size = 440
HORIZONTAL_OFFSET = (WIDTH - board_size) // 2
VERTICAL_OFFSET = (HEIGHT - board_size) // 2

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")

font = pygame.font.SysFont("arial", 40, bold=True)
small_font = pygame.font.SysFont("arial", 20, bold=True)
menu_font = pygame.font.SysFont("arial", 28, bold=True)

board = [[0]*GRID_SIZE for _ in range(GRID_SIZE)]
score = 0
current_user = None
best_user_score = 0

def add_new_tile():
    empty_cells = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if board[r][c] == 0]
    if not empty_cells:
        return
    r, c = random.choice(empty_cells)
    board[r][c] = 2 if random.random() < 0.9 else 4

def can_move():
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if board[r][c] == 0:
                return True
            if c < GRID_SIZE-1 and board[r][c] == board[r][c+1]:
                return True
            if r < GRID_SIZE-1 and board[r][c] == board[r+1][c]:
                return True
    return False

def move_left():
    global score
    moved = False
    for r in range(GRID_SIZE):
        row = [x for x in board[r] if x != 0]
        merged_row = []
        skip = False
        for i in range(len(row)):
            if skip:
                skip = False
                continue
            if i+1 < len(row) and row[i] == row[i+1]:
                merged_val = row[i]*2
                merged_row.append(merged_val)
                score += merged_val
                skip = True
            else:
                merged_row.append(row[i])
        merged_row += [0]*(GRID_SIZE - len(merged_row))
        if merged_row != board[r]:
            moved = True
        board[r] = merged_row
    return moved

def move_right():
    global score
    moved = False
    for r in range(GRID_SIZE):
        row = [x for x in board[r] if x != 0]
        merged_row = []
        skip = False
        for i in range(len(row)-1, -1, -1):
            if skip:
                skip = False
                continue
            if i-1 >= 0 and row[i] == row[i-1]:
                merged_val = row[i]*2
                merged_row.insert(0, merged_val)
                score += merged_val
                skip = True
            else:
                merged_row.insert(0, row[i])
        merged_row = [0]*(GRID_SIZE - len(merged_row)) + merged_row
        if merged_row != board[r]:
            moved = True
        board[r] = merged_row
    return moved

def move_up():
    global score
    moved = False
    for c in range(GRID_SIZE):
        col = [board[r][c] for r in range(GRID_SIZE) if board[r][c] != 0]
        merged_col = []
        skip = False
        for i in range(len(col)):
            if skip:
                skip = False
                continue
            if i+1 < len(col) and col[i] == col[i+1]:
                merged_val = col[i]*2
                merged_col.append(merged_val)
                score += merged_val
                skip = True
            else:
                merged_col.append(col[i])
        merged_col += [0]*(GRID_SIZE - len(merged_col))
        for r in range(GRID_SIZE):
            if board[r][c] != merged_col[r]:
                moved = True
            board[r][c] = merged_col[r]
    return moved

def move_down():
    global score
    moved = False
    for c in range(GRID_SIZE):
        col = [board[r][c] for r in range(GRID_SIZE) if board[r][c] != 0]
        merged_col = []
        skip = False
        for i in range(len(col)-1, -1, -1):
            if skip:
                skip = False
                continue
            if i-1 >= 0 and col[i] == col[i-1]:
                merged_val = col[i]*2
                merged_col.insert(0, merged_val)
                score += merged_val
                skip = True
            else:
                merged_col.insert(0, col[i])
        merged_col = [0]*(GRID_SIZE - len(merged_col)) + merged_col
        for r in range(GRID_SIZE):
            if board[r][c] != merged_col[r]:
                moved = True
            board[r][c] = merged_col[r]
    return moved

def draw_board():
    screen.fill(BACKGROUND_COLOR)
    score_text = small_font.render("Score: " + str(score), True, (119,110,101))
    screen.blit(score_text, (20, 20))
    best_score_text = small_font.render(f"Best: {best_user_score}", True, (119,110,101))
    screen.blit(best_score_text, (20, 50))
    user_text = small_font.render(f"User: {current_user}", True, (119,110,101))
    screen.blit(user_text, (WIDTH - 150, 20))
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            val = board[r][c]
            rect_x = c*(CELL_SIZE+CELL_PADDING) + CELL_PADDING + HORIZONTAL_OFFSET
            rect_y = r*(CELL_SIZE+CELL_PADDING) + CELL_PADDING + VERTICAL_OFFSET
            tile_rect = pygame.Rect(rect_x, rect_y, CELL_SIZE, CELL_SIZE)
            if val == 0:
                pygame.draw.rect(screen, EMPTY_CELL_COLOR, tile_rect, border_radius=5)
            else:
                color = TILE_COLORS.get(val, TILE_COLORS[2048])
                pygame.draw.rect(screen, color, tile_rect, border_radius=5)
                text_color = TILE_TEXT_COLORS.get(val, TILE_TEXT_COLORS[2048])
                tile_text = font.render(str(val), True, text_color)
                text_rect = tile_text.get_rect(center=tile_rect.center)
                screen.blit(tile_text, text_rect)

def check_win():
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if board[r][c] == 2048:
                return True
    return False

def game_over_screen(win=False):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(180)
    overlay.fill((0,0,0))
    screen.blit(overlay, (0,0))
    msg = "You Win!" if win else "Game Over!"
    text = font.render(msg, True, (255,255,255))
    rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(text, rect)
    pygame.display.flip()

def save_score(username, score):
    scores_collection.update_one(
        {"username": username},
        {"$max": {"score": score}},
        upsert=True
    )

def show_leaderboard_screen():
    screen.fill(BACKGROUND_COLOR)
    leaderboard_text = font.render("Leaderboard", True, (119,110,101))
    screen.blit(leaderboard_text, leaderboard_text.get_rect(center=(WIDTH//2, 50)))
    top_scores = scores_collection.find().sort("score", -1).limit(10)
    y_offset = 120
    rank = 1
    for s in top_scores:
        line = f"{rank}. {s['username']} - {s['score']}"
        line_surface = small_font.render(line, True, (119,110,101))
        screen.blit(line_surface, (60, y_offset))
        y_offset += 40
        rank += 1
    back_rect = draw_button("Back to the menu", WIDTH//2, HEIGHT - 50, width=250, height=60)
    pygame.display.flip()
    return back_rect

def draw_button(text, center_x, center_y, width=250, height=60):
    mouse_pos = pygame.mouse.get_pos()
    rect = pygame.Rect(0, 0, width, height)
    rect.center = (center_x, center_y)
    color = (200,200,200)
    if rect.collidepoint(mouse_pos):
        color = (170,170,170)
    pygame.draw.rect(screen, color, rect, border_radius=5)
    btn_text = menu_font.render(text, True, (50,50,50))
    btn_rect = btn_text.get_rect(center=rect.center)
    screen.blit(btn_text, btn_rect)
    return rect

def login_screen():
    username = ""
    password = ""
    user_label_y = HEIGHT//2 - 120
    user_input_y = user_label_y + 40
    pass_label_y = user_input_y + 60
    pass_input_y = pass_label_y + 40
    button_y = pass_input_y + 80
    input_box_user = pygame.Rect(WIDTH//2 - 100, user_input_y, 200, 40)
    input_box_pass = pygame.Rect(WIDTH//2 - 100, pass_input_y, 200, 40)
    active_user = False
    active_pass = False
    info_text = ""
    while True:
        screen.fill(BACKGROUND_COLOR)
        title_text = font.render("Login / Register", True, (119,110,101))
        screen.blit(title_text, title_text.get_rect(center=(WIDTH//2, 100)))
        user_surface = menu_font.render("Username:", True, (119,110,101))
        screen.blit(user_surface, (WIDTH//2 - 100, user_label_y))
        pass_surface = menu_font.render("Password:", True, (119,110,101))
        screen.blit(pass_surface, (WIDTH//2 - 100, pass_label_y))
        pygame.draw.rect(screen, (255,255,255), input_box_user, border_radius=5)
        pygame.draw.rect(screen, (255,255,255), input_box_pass, border_radius=5)
        text_user = menu_font.render(username, True, (0,0,0))
        text_pass = menu_font.render("*"*len(password), True, (0,0,0))
        screen.blit(text_user, (input_box_user.x+5, input_box_user.y+5))
        screen.blit(text_pass, (input_box_pass.x+5, input_box_pass.y+5))
        login_rect = draw_button("Login", WIDTH//2 - 80, button_y, width=150, height=50)
        register_rect = draw_button("Register", WIDTH//2 + 80, button_y, width=150, height=50)
        if info_text:
            info_surf = small_font.render(info_text, True, (255,0,0))
            screen.blit(info_surf, info_surf.get_rect(center=(WIDTH//2, button_y + 70)))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box_user.collidepoint(event.pos):
                    active_user = True
                    active_pass = False
                elif input_box_pass.collidepoint(event.pos):
                    active_pass = True
                    active_user = False
                else:
                    active_user = False
                    active_pass = False
                if login_rect.collidepoint(event.pos):
                    user = users_collection.find_one({"username": username})
                    if user and user["password"] == password:
                        return username
                    else:
                        info_text = "Invalid username or password"
                elif register_rect.collidepoint(event.pos):
                    if users_collection.find_one({"username": username}):
                        info_text = "Username already exists"
                    else:
                        if username and password:
                            users_collection.insert_one({"username": username, "password": password})
                            info_text = "User registered. Now login."
                        else:
                            info_text = "Enter username and password"
            elif event.type == pygame.KEYDOWN:
                if active_user:
                    if event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    elif event.key == pygame.K_RETURN:
                        active_user = False
                    else:
                        username += event.unicode
                elif active_pass:
                    if event.key == pygame.K_BACKSPACE:
                        password = password[:-1]
                    elif event.key == pygame.K_RETURN:
                        active_pass = False
                    else:
                        password += event.unicode

def main_menu_screen():
    while True:
        screen.fill(BACKGROUND_COLOR)
        title_text = font.render("Main Menu", True, (119,110,101))
        screen.blit(title_text, title_text.get_rect(center=(WIDTH//2, 100)))
        play_rect = draw_button("Start the game", WIDTH//2, HEIGHT//2)
        leader_rect = draw_button("Leaderboard", WIDTH//2, HEIGHT//2+80)
        exit_rect = draw_button("Exit", WIDTH//2, HEIGHT//2+160)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    return "play"
                elif leader_rect.collidepoint(event.pos):
                    return "leaderboard"
                elif exit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

def play_game():
    global score, board, best_user_score
    score = 0
    board = [[0]*GRID_SIZE for _ in range(GRID_SIZE)]
    add_new_tile()
    add_new_tile()
    running = True
    game_over_flag = False
    win_flag = False
    while running:
        draw_board()
        exit_rect = draw_button("Exit", WIDTH//2, HEIGHT - 30, width=100, height=40)
        pygame.display.flip()
        if check_win() and not win_flag:
            win_flag = True
            game_over_screen(win=True)
            pygame.time.wait(2000)
            save_score(current_user, score)
            user_score_doc = scores_collection.find_one({"username": current_user})
            if user_score_doc and user_score_doc["score"] > best_user_score:
                best_user_score = user_score_doc["score"]
            running = False
        if not can_move() and not game_over_flag and not win_flag:
            game_over_flag = True
            game_over_screen(win=False)
            pygame.time.wait(2000)
            save_score(current_user, score)
            user_score_doc = scores_collection.find_one({"username": current_user})
            if user_score_doc and user_score_doc["score"] > best_user_score:
                best_user_score = user_score_doc["score"]
            running = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_score(current_user, score)
                user_score_doc = scores_collection.find_one({"username": current_user})
                if user_score_doc and user_score_doc["score"] > best_user_score:
                    best_user_score = user_score_doc["score"]
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if exit_rect.collidepoint(event.pos):
                    save_score(current_user, score)
                    user_score_doc = scores_collection.find_one({"username": current_user})
                    if user_score_doc and user_score_doc["score"] > best_user_score:
                        best_user_score = user_score_doc["score"]
                    running = False
                    break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    save_score(current_user, score)
                    user_score_doc = scores_collection.find_one({"username": current_user})
                    if user_score_doc and user_score_doc["score"] > best_user_score:
                        best_user_score = user_score_doc["score"]
                    running = False
                    break
                moved = False
                if event.key == pygame.K_LEFT:
                    moved = move_left()
                elif event.key == pygame.K_RIGHT:
                    moved = move_right()
                elif event.key == pygame.K_UP:
                    moved = move_up()
                elif event.key == pygame.K_DOWN:
                    moved = move_down()
                if moved:
                    add_new_tile()

def main():
    global current_user, best_user_score
    current_user = login_screen()
    user_score_doc = scores_collection.find_one({"username": current_user})
    if user_score_doc:
        best_user_score = user_score_doc["score"]
    else:
        best_user_score = 0
    while True:
        action = main_menu_screen()
        if action == "play":
            play_game()
            user_score_doc = scores_collection.find_one({"username": current_user})
            if user_score_doc and user_score_doc["score"] > best_user_score:
                best_user_score = user_score_doc["score"]
        elif action == "leaderboard":
            while True:
                back_rect = show_leaderboard_screen()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if back_rect.collidepoint(event.pos):
                            break
                else:
                    continue
                break

if __name__ == "__main__":
    main()
