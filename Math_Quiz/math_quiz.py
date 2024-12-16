import pygame
import random
import sys
import os

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BG_COLOR = (240, 240, 255)          
PANEL_COLOR = (220, 230, 250)       
TEXT_COLOR = (50, 50, 100)          
HIGHLIGHT_COLOR = (255, 230, 150)   
BUTTON_COLOR = (200, 200, 255)     
BUTTON_HOVER_COLOR = (180, 180, 240)
RED_OVERLAY = (200, 100, 100, 180)  

TITLE_FONT = pygame.font.Font("freesansbold.ttf", 80)
FONT = pygame.font.Font("freesansbold.ttf", 40)
SMALL_FONT = pygame.font.Font("freesansbold.ttf", 24)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Math Quiz")

clock = pygame.time.Clock()

timer = 60
score = 0
level = 1
best_score = 0

STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"
state = STATE_MENU

BEST_SCORE_FILE = "best_score.txt"


def load_best_score():
    global best_score
    if os.path.exists(BEST_SCORE_FILE):
        with open(BEST_SCORE_FILE, "r") as file:
            try:
                best_score = int(file.read().strip())
            except ValueError:
                best_score = 0


def save_best_score():
    global best_score
    with open(BEST_SCORE_FILE, "w") as file:
        file.write(str(best_score))


def generate_question():
    global level
    max_value = 20 + (level - 1) * 10
    operation = random.choice(["+", "-", "*", "/"])

    if operation == "/":
        b = random.randint(1, max_value // 2)
        a = b * random.randint(1, max_value // b)
    else:
        a = random.randint(1, max_value)
        b = random.randint(1, max_value)

    if operation == "+":
        answer = a + b
    elif operation == "-":
        answer = a - b
    elif operation == "*":
        answer = a * b
    else:
        answer = a // b

    answers = {answer}
    while len(answers) < 4:
        offset = random.choice([-5, -4, -3, 3, 4, 5])
        wrong_answer = answer + offset
        if wrong_answer not in answers and (wrong_answer > 0 or answer < 0):
            answers.add(wrong_answer)

    if answer < 0:
        while len([x for x in answers if x < 0]) < 2:
            answers.add(-random.randint(1, max_value))
    else:
        while len([x for x in answers if x > 0]) < 2:
            answers.add(random.randint(1, max_value))

    answers = list(answers)[:4]
    random.shuffle(answers)
    question = f"{a} {operation} {b}"
    return question, answers, answer


def draw_text(text, x, y, color=TEXT_COLOR, font=FONT):
    rendered_text = font.render(text, True, color)
    screen.blit(rendered_text, (x, y))


def menu():
    screen.fill(BG_COLOR)
    title_surf = TITLE_FONT.render("Math Quiz", True, TEXT_COLOR)
    title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
    screen.blit(title_surf, title_rect)

    best_surf = FONT.render(f"Best Score: {best_score}", True, TEXT_COLOR)
    best_rect = best_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(best_surf, best_rect)

    start_surf = SMALL_FONT.render("Press ENTER to Start", True, TEXT_COLOR)
    start_rect = start_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(start_surf, start_rect)

    exit_surf = SMALL_FONT.render("Press ESC to Exit", True, TEXT_COLOR)
    exit_rect = exit_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 90))
    screen.blit(exit_surf, exit_rect)

    pygame.display.flip()


def game_over():
    global score, best_score
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill(RED_OVERLAY)
    screen.blit(overlay, (0, 0))

    if score > best_score:
        best_score = score
        save_best_score()

    go_surf = TITLE_FONT.render("Game Over", True, (255, 255, 255))
    go_rect = go_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
    screen.blit(go_surf, go_rect)

    score_surf = FONT.render(f"Your Score: {score}", True, (255, 255, 255))
    score_rect = score_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
    screen.blit(score_surf, score_rect)

    best_surf = FONT.render(f"Best Score: {best_score}", True, (255, 255, 255))
    best_rect = best_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
    screen.blit(best_surf, best_rect)

    exit_surf = SMALL_FONT.render("Press Q to Exit", True, (255, 255, 255))
    exit_rect = exit_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 90))
    screen.blit(exit_surf, exit_rect)

    restart_surf = SMALL_FONT.render("Press ENTER to Restart", True, (255, 255, 255))
    restart_rect = restart_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 130))
    screen.blit(restart_surf, restart_rect)

    pygame.display.flip()


def game():
    global timer, score, level, state, best_score

    question, answers, correct_answer = generate_question()
    selected = -1

    timer_highlight_color = None
    timer_highlight_end_time = 0

    while state == STATE_PLAYING:
        current_time = pygame.time.get_ticks()
        screen.fill(BG_COLOR)

        pygame.draw.rect(screen, PANEL_COLOR, (50, 50, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100), border_radius=20)

        pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH // 2 - 200, 100, 400, 70), border_radius=15)
        draw_text(question, SCREEN_WIDTH // 2 - 180, 120, TEXT_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if score > best_score:
                    best_score = score
                    save_best_score()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    if score > best_score:
                        best_score = score
                        save_best_score()
                    state = STATE_MENU
                    return
                elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                    selected = int(event.key - pygame.K_1)

        timer -= clock.get_time() / 1000
        if timer <= 0:
            state = STATE_GAME_OVER
            return

        if selected != -1:
            if answers[selected] == correct_answer:
                timer += 5
                score += 10
                timer_highlight_color = (0, 255, 0)
                timer_highlight_end_time = current_time + 1000  

                if score % 50 == 0:
                    level += 1
            else:
                timer -= 20
                timer_highlight_color = (255, 0, 0)
                timer_highlight_end_time = current_time + 1000  

            question, answers, correct_answer = generate_question()
            selected = -1

        if timer_highlight_color and current_time < timer_highlight_end_time:
            time_color = timer_highlight_color
        else:
            time_color = TEXT_COLOR

        draw_text(f"Time: {max(0, int(timer))} sec", 60, 60, time_color, SMALL_FONT)
        draw_text(f"Score: {score}", SCREEN_WIDTH - 200, 60, TEXT_COLOR, SMALL_FONT)
        draw_text(f"Level: {level}", SCREEN_WIDTH - 200, 100, TEXT_COLOR, SMALL_FONT)
        draw_text("Press Q to Exit", SCREEN_WIDTH - 300, 500, TEXT_COLOR, SMALL_FONT)

        for i, answer in enumerate(answers):
            ans_x = SCREEN_WIDTH // 2 - 180
            ans_y = 250 + i * 50
            ans_str = f"{i + 1}. {answer}"
            if i == selected:
                pygame.draw.rect(screen, HIGHLIGHT_COLOR, (ans_x - 10, ans_y - 5, 300, 45), border_radius=8)
            draw_text(ans_str, ans_x, ans_y, TEXT_COLOR, SMALL_FONT)

        pygame.display.flip()
        clock.tick(30)


load_best_score()

while True:
    if state == STATE_MENU:
        menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    timer = 60
                    score = 0
                    level = 1
                    state = STATE_PLAYING
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    elif state == STATE_PLAYING:
        game()
    elif state == STATE_GAME_OVER:
        game_over()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    timer = 60
                    score = 0
                    level = 1
                    state = STATE_PLAYING
                elif event.key == pygame.K_q:
                    state = STATE_MENU

    clock.tick(30)
