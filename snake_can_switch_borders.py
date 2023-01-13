import pygame
from random import randrange

pygame.init()

WINDOW = 1000
TILE_SIZE = 50
RANGE = (TILE_SIZE // 2, WINDOW - TILE_SIZE // 2, TILE_SIZE)


get_random_position = lambda: [randrange(*RANGE), randrange(*RANGE)]
snake = pygame.rect.Rect([0, 0, TILE_SIZE, TILE_SIZE])
snake.center = get_random_position()


font = pygame.font.Font(None, 24)
length = 1
segments = [snake.copy()]


snake_direction = (0, 0)
possible_directions = {

    pygame.K_w: 1, pygame.K_s: 1,
    pygame.K_a: 1, pygame.K_d: 1
    
    }


time, time_step = 0, 80
food = snake.copy()
food.center = get_random_position()


screen = pygame.display.set_mode([WINDOW] * 2)
clock = pygame.time.Clock()


# Main Game Loop
score = 0
running = True
while running:
    # Set the score box text:
    score_text = ('SCORE: ' + str(score))
    score_text_color = (0, 255, 0)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and possible_directions[pygame.K_w]:
                snake_direction = (0, -TILE_SIZE)
                possible_directions = {pygame.K_w: 1, pygame.K_s: 0, pygame.K_a: 1, pygame.K_d: 1}
            if event.key == pygame.K_s and possible_directions[pygame.K_s]:
                snake_direction = (0, TILE_SIZE)
                possible_directions = {pygame.K_w: 0, pygame.K_s: 1, pygame.K_a: 1, pygame.K_d: 1}
            if event.key == pygame.K_a and possible_directions[pygame.K_a]:
                snake_direction = (-TILE_SIZE, 0)
                possible_directions = {pygame.K_w: 1, pygame.K_s: 1, pygame.K_a: 1, pygame.K_d: 0}
            if event.key == pygame.K_d and possible_directions[pygame.K_d]:
                snake_direction = (TILE_SIZE, 0)
                possible_directions = {pygame.K_w: 1, pygame.K_s: 1, pygame.K_a: 0, pygame.K_d: 1}
    

    screen.fill((0, 0, 0))


    def draw_score():
        score_text_surface = font.render(score_text, True, (0, 255, 0))
        screen.blit(score_text_surface, (900, 40))


    # Check Borders
    if snake.right > WINDOW:
        snake.left = 0
    if snake.top > WINDOW - TILE_SIZE:
        snake.top = 0
    if snake.right < 0:
        snake.right = WINDOW
    if snake.top < 0:
        snake.top = WINDOW - TILE_SIZE


    # Check selfeating
    self_eating = pygame.Rect.collidelist(snake, segments[:-1]) != -1
    if self_eating:
        snake.center = get_random_position()
        food.center = get_random_position()
        length = 1
        snake_direction = (0, 0)
        segments = [snake.copy()]
        score = 0


    # Draw Snake
    [pygame.draw.rect(screen, (255, 255, 255), segment) for segment in segments]
   

    # Draw Food
    pygame.draw.rect(screen, (0, 0, 255), food)


    # Check Food Position
    if snake.center == food.center:
        food.center = get_random_position()
        length += 1
        score += 1
        draw_score()


    # Move snake
    time_now = pygame.time.get_ticks()
    if time_now - time > time_step:
        time = time_now
        snake.move_ip(snake_direction)
        segments.append(snake.copy())
        segments = segments[-length:]


    draw_score()
    pygame.display.flip()
    clock.tick(144)