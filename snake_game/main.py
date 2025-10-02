import pygame
import sys
import random

pygame.init()

pygame.mixer.init()
pygame.mixer.music.load("assets/music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

width, height = 400, 400
CELL = 20
FPS = 7
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake game")

BG_COLOR = (0, 0, 255)
SNAKE_COLOR = (0, 225, 0)
APPLE_COLOR = (255, 0, 0)
TEXT_COLOR = (255, 255, 255)

apple_img = pygame.image.load("assets/apple.png").convert_alpha()
apple_img = pygame.transform.scale(apple_img, (CELL, CELL))

body_straight = pygame.image.load("assets/body_straight.png").convert_alpha()
body_straight = pygame.transform.scale(body_straight, (CELL, CELL))

body_turn = pygame.image.load("assets/body_turn.png").convert_alpha()
body_turn = pygame.transform.scale(body_turn, (CELL, CELL))

head_up = pygame.image.load("assets/head_up.png").convert_alpha()
head_up = pygame.transform.scale(head_up, (CELL, CELL))

head_down = pygame.image.load("assets/head_down.png").convert_alpha()
head_down = pygame.transform.scale(head_down, (CELL, CELL))

head_left = pygame.image.load("assets/head_left.png").convert_alpha()
head_left = pygame.transform.scale(head_left, (CELL, CELL))

head_right = pygame.image.load("assets/head_right.png").convert_alpha()
head_right = pygame.transform.scale(head_right, (CELL, CELL))

tail_down = pygame.image.load("assets/tail_down.png").convert_alpha()
tail_down = pygame.transform.scale(tail_down, (CELL, CELL))

tail_up = pygame.image.load("assets/tail_up.png").convert_alpha()
tail_up = pygame.transform.scale(tail_up, (CELL, CELL))

tail_left = pygame.image.load("assets/tail_left.png").convert_alpha()
tail_left = pygame.transform.scale(tail_left, (CELL, CELL))

tail_right = pygame.image.load("assets/tail_right.png").convert_alpha()
tail_right = pygame.transform.scale(tail_right, (CELL, CELL))

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)


def random_apple(snake_body):
    while True:
        ax = random.randrange(0, width, CELL)
        ay = random.randrange(0, height, CELL)
        if (ax, ay) not in snake_body:
            return (ax, ay)


def get_body_image(prev_seg, seg, next_seg):
    x, y = seg
    v_prev = ((prev_seg[0] - x) // CELL, (prev_seg[1] - y) // CELL)
    v_next = ((next_seg[0] - x) // CELL, (next_seg[1] - y) // CELL)

    if v_prev[1] == v_next[1]:
        return body_straight
    if v_prev[0] == v_next[0]:
        return pygame.transform.rotate(body_straight, 90)

    s = frozenset({v_prev, v_next})

    corner_map = {
        frozenset({(1, 0), (0, -1)}): 0,
        frozenset({(0, -1), (-1, 0)}): 90,
        frozenset({(-1, 0), (0, 1)}): 180,
        frozenset({(0, 1), (1, 0)}): 270,
    }
    angle = corner_map.get(s, 0)
    return pygame.transform.rotate(body_turn, angle)


def reset_game():
    start_x = width // 2 // CELL * CELL
    start_y = height // 2 // CELL * CELL
    snake = [(start_x - CELL, start_y), (start_x, start_y)]
    dx, dy = CELL, 0
    apple = random_apple(snake)
    score = 0
    game_over = False
    return snake, dx, dy, apple, score, game_over


snake, dx, dy, apple, score, game_over = reset_game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if not game_over:
                if event.key == pygame.K_UP and dy == 0:
                    dx, dy = 0, -CELL
                elif event.key == pygame.K_DOWN and dy == 0:
                    dx, dy = 0, CELL
                elif event.key == pygame.K_LEFT and dx == 0:
                    dx, dy = -CELL, 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx, dy = CELL, 0
            else:
                if event.key == pygame.K_r:
                    snake, dx, dy, apple, score, game_over = reset_game()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

    if not game_over and (dx != 0 or dy != 0):
        head_x, head_y = snake[-1]
        new_head = (head_x + dx, head_y + dy)

        if (new_head[0] < 0 or new_head[0] >= width or
                new_head[1] < 0 or new_head[1] >= height):
            game_over = True
        elif new_head in snake:
            game_over = True
        else:
            snake.append(new_head)

            if new_head == apple:
                score += 1
                apple = random_apple(snake)
            else:
                snake.pop(0)

    screen.fill(BG_COLOR)

    screen.blit(apple_img, (apple[0], apple[1]))

    for i, seg in enumerate(snake):  # Голова
        x, y = seg
        if i == len(snake) - 1:
            if dx > 0:
                screen.blit(head_right, (x, y))
            elif dx < 0:
                screen.blit(head_left, (x, y))
            elif dy > 0:
                screen.blit(head_down, (x, y))
            elif dy < 0:
                screen.blit(head_up, (x, y))

        elif i == 0:  # Хвост
            next_seg = snake[1]
            vx = (x - next_seg[0]) // CELL
            vy = (y - next_seg[1]) // CELL
            if vx == 1:
                screen.blit(tail_right, (x, y))
            elif vx == -1:
                screen.blit(tail_left, (x, y))
            elif vy == 1:
                screen.blit(tail_down, (x, y))
            elif vy == -1:
                screen.blit(tail_up, (x, y))

        else:
            prev_seg = snake[i - 1]
            next_seg = snake[i + 1]
            body_img = get_body_image(prev_seg, seg, next_seg)
            screen.blit(body_img, (x, y))

    score_surf = font.render(f"Score: {score}", True, TEXT_COLOR)
    screen.blit(score_surf, (10, 10))

    if game_over:
        go_surf = font.render("GAME OVER R - restart Q - quit", True, TEXT_COLOR)
        go_rect = go_surf.get_rect(center=(width // 2, height // 2))
        screen.blit(go_surf, go_rect)

    pygame.display.flip()
    clock.tick(FPS)
