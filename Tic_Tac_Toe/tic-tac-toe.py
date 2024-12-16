import pygame
import sys
import random

pygame.init()

WIDTH = 600
HEIGHT = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG_COLOR = (230, 230, 230)
GRID_COLOR = (50, 50, 50)
X_COLOR = (220, 20, 60)
O_COLOR = (30, 144, 255)
BUTTON_COLOR = (200, 200, 200)
BUTTON_HOVER_COLOR = (170, 170, 170)
TEXT_COLOR = (50, 50, 50)
WIN_LINE_COLOR = (0, 200, 0) 

CELL_SIZE = 180
LINE_WIDTH = 10
GRID_OFFSET = 30  

END_DELAY = 1000

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Хрестики-Нулики")

font = pygame.font.SysFont("arial", 60, bold=True)
small_font = pygame.font.SysFont("arial", 34, bold=True)

board = [['' for _ in range(3)] for _ in range(3)]

current_player = 'X'
game_over = False
winner = None
play_mode = None
show_main_menu = True

winning_line = None
game_end_time = None
show_end_menu_flag = False

def draw_board():
    screen.fill(BG_COLOR)
    
    border_rect = pygame.Rect(GRID_OFFSET - 10, GRID_OFFSET - 10, CELL_SIZE*3 + 20, CELL_SIZE*3 + 20)
    pygame.draw.rect(screen, GRID_COLOR, border_rect, 5)

    for i in range(1, 3):
        start_x = GRID_OFFSET + CELL_SIZE*i
        pygame.draw.line(screen, GRID_COLOR, (start_x, GRID_OFFSET), (start_x, GRID_OFFSET + CELL_SIZE*3), LINE_WIDTH)

        start_y = GRID_OFFSET + CELL_SIZE*i
        pygame.draw.line(screen, GRID_COLOR, (GRID_OFFSET, start_y), (GRID_OFFSET + CELL_SIZE*3, start_y), LINE_WIDTH)

    for row in range(3):
        for col in range(3):
            mark = board[row][col]
            if mark == 'X':
                draw_x(col, row)
            elif mark == 'O':
                draw_o(col, row)

def draw_x(col, row):
    start_x = GRID_OFFSET + col * CELL_SIZE
    start_y = GRID_OFFSET + row * CELL_SIZE
    end_x = start_x + CELL_SIZE
    end_y = start_y + CELL_SIZE
    pygame.draw.line(screen, X_COLOR, (start_x+20, start_y+20), (end_x-20, end_y-20), LINE_WIDTH)
    pygame.draw.line(screen, X_COLOR, (start_x+20, end_y-20), (end_x-20, start_y+20), LINE_WIDTH)

def draw_o(col, row):
    center_x = GRID_OFFSET + col * CELL_SIZE + CELL_SIZE//2
    center_y = GRID_OFFSET + row * CELL_SIZE + CELL_SIZE//2
    pygame.draw.circle(screen, O_COLOR, (center_x, center_y), CELL_SIZE//2 - 20, LINE_WIDTH)

def check_winner():
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != '':
            start_pos = (GRID_OFFSET, GRID_OFFSET + i*CELL_SIZE + CELL_SIZE//2)
            end_pos = (GRID_OFFSET + CELL_SIZE*3, GRID_OFFSET + i*CELL_SIZE + CELL_SIZE//2)
            return board[i][0], start_pos, end_pos

    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] != '':
            start_pos = (GRID_OFFSET + j*CELL_SIZE + CELL_SIZE//2, GRID_OFFSET)
            end_pos = (GRID_OFFSET + j*CELL_SIZE + CELL_SIZE//2, GRID_OFFSET + CELL_SIZE*3)
            return board[0][j], start_pos, end_pos

    if board[0][0] == board[1][1] == board[2][2] != '':
        start_pos = (GRID_OFFSET, GRID_OFFSET)
        end_pos = (GRID_OFFSET + CELL_SIZE*3, GRID_OFFSET + CELL_SIZE*3)
        return board[0][0], start_pos, end_pos

    if board[0][2] == board[1][1] == board[2][0] != '':
        start_pos = (GRID_OFFSET + CELL_SIZE*3, GRID_OFFSET)
        end_pos = (GRID_OFFSET, GRID_OFFSET + CELL_SIZE*3)
        return board[0][2], start_pos, end_pos

    return None, None, None

def is_board_full():
    for row in board:
        for cell in row:
            if cell == '':
                return False
    return True

def reset_game():
    global board, current_player, game_over, winner, winning_line, game_end_time, show_end_menu_flag
    board = [['' for _ in range(3)] for _ in range(3)]
    current_player = 'X'
    game_over = False
    winner = None
    winning_line = None
    game_end_time = None
    show_end_menu_flag = False

def draw_message(message, y_offset=0):
    text = font.render(message, True, TEXT_COLOR)
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 + y_offset))
    screen.blit(text, text_rect)

def find_best_move_for(computer_symbol):
    for (r, c) in get_empty_cells():
        board[r][c] = computer_symbol
        w, _, _ = check_winner()
        if w == computer_symbol:
            board[r][c] = ''
            return (r, c)
        board[r][c] = ''

    opponent_symbol = 'X' if computer_symbol == 'O' else 'O'
    for (r, c) in get_empty_cells():
        board[r][c] = opponent_symbol
        w, _, _ = check_winner()
        if w == opponent_symbol:
            board[r][c] = ''
            return (r, c)
        board[r][c] = ''

    empty_cells = get_empty_cells()
    if empty_cells:
        return random.choice(empty_cells)
    return None

def get_empty_cells():
    return [(r, c) for r in range(3) for c in range(3) if board[r][c] == '']

def computer_move():
    move = find_best_move_for('O')
    if move:
        r, c = move
        board[r][c] = 'O'

def draw_button(text, center_x, center_y, width=360, height=60):
    mouse_pos = pygame.mouse.get_pos()
    rect = pygame.Rect(0, 0, width, height)
    rect.center = (center_x, center_y)
    color = BUTTON_COLOR
    if rect.collidepoint(mouse_pos):
        color = BUTTON_HOVER_COLOR
    pygame.draw.rect(screen, color, rect, border_radius=10)
    btn_text = small_font.render(text, True, TEXT_COLOR)
    btn_rect = btn_text.get_rect(center=rect.center)
    screen.blit(btn_text, btn_rect)
    return rect

def draw_main_menu():
    screen.fill(BG_COLOR)
    title = font.render("Хрестики-Нулики", True, TEXT_COLOR)
    title_rect = title.get_rect(center=(WIDTH//2, HEIGHT//4))
    screen.blit(title, title_rect)

    computer_rect = draw_button("Грати з комп’ютером", WIDTH//2, HEIGHT//2)
    pvp_rect = draw_button("Грати 1 на 1", WIDTH//2, HEIGHT//2 + 100)

    return computer_rect, pvp_rect

def draw_end_menu():
    screen.fill(BG_COLOR)
    if winner:
        msg = f"Переміг гравець: {winner}"
    else:
        msg = "Нічия!"

    draw_message(msg, y_offset=-50)

    replay_rect = draw_button("Зіграти знову", WIDTH//2, HEIGHT//2 + 50)
    main_menu_rect = draw_button("Головне меню", WIDTH//2, HEIGHT//2 + 130)

    return replay_rect, main_menu_rect

def draw_winning_line(start_pos, end_pos):
    pygame.draw.line(screen, WIN_LINE_COLOR, start_pos, end_pos, LINE_WIDTH)

clock = pygame.time.Clock()

while True:
    clock.tick(30)

    if show_main_menu:
        computer_rect, pvp_rect = draw_main_menu()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if computer_rect.collidepoint(event.pos):
                    play_mode = 'computer'
                    show_main_menu = False
                    reset_game()
                elif pvp_rect.collidepoint(event.pos):
                    play_mode = 'pvp'
                    show_main_menu = False
                    reset_game()
    else:
        if game_over:
            if winner and winning_line and not show_end_menu_flag:
                draw_board()
                draw_winning_line(winning_line[0], winning_line[1])
                pygame.display.flip()
                if pygame.time.get_ticks() - game_end_time >= END_DELAY:
                    show_end_menu_flag = True
            else:
                replay_rect, main_menu_rect = draw_end_menu()
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if replay_rect.collidepoint(event.pos):
                            reset_game()
                        elif main_menu_rect.collidepoint(event.pos):
                            show_main_menu = True
                            play_mode = None
        else:
            draw_board()
            if winner and winning_line:
                draw_winning_line(winning_line[0], winning_line[1])
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if GRID_OFFSET <= x <= GRID_OFFSET + CELL_SIZE*3 and GRID_OFFSET <= y <= GRID_OFFSET + CELL_SIZE*3:
                        col = (x - GRID_OFFSET) // CELL_SIZE
                        row = (y - GRID_OFFSET) // CELL_SIZE
                        if board[row][col] == '':
                            if play_mode == 'pvp':
                                board[row][col] = current_player
                                w, start_pos, end_pos = check_winner()
                                if w or is_board_full():
                                    winner = w
                                    if winner:
                                        winning_line = (start_pos, end_pos)
                                    game_over = True
                                    game_end_time = pygame.time.get_ticks()
                                else:
                                    current_player = 'O' if current_player == 'X' else 'X'

                            elif play_mode == 'computer':
                                board[row][col] = 'X'
                                w, start_pos, end_pos = check_winner()
                                if w or is_board_full():
                                    winner = w
                                    if winner:
                                        winning_line = (start_pos, end_pos)
                                    game_over = True
                                    game_end_time = pygame.time.get_ticks()
                                else:
                                    computer_move()
                                    w, start_pos, end_pos = check_winner()
                                    if w or is_board_full():
                                        winner = w
                                        if winner:
                                            winning_line = (start_pos, end_pos)
                                        game_over = True
                                        game_end_time = pygame.time.get_ticks()
