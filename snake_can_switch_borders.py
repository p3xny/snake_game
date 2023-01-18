import pygame
import random
from random import randrange

pygame.init()


def snake_game():
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
    possible_directions_wsad = {
        pygame.K_w: 1, pygame.K_s: 1,
        pygame.K_a: 1, pygame.K_d: 1,
        }
    possible_directions_arrows = {
        pygame.K_UP: 1, pygame.K_DOWN: 1,
        pygame.K_LEFT: 1, pygame.K_RIGHT: 1
    }


    time, time_step = 0, 100
    food = snake.copy()
    food.center = get_random_position()
    food_visible = True


    screen = pygame.display.set_mode([WINDOW] * 2)
    clock = pygame.time.Clock()


    colors = [(255, 0, 0), (255, 255, 0), (255, 0, 255), (0, 255, 255),
     (0, 255, 0)]
    food_color = (0, 0, 255)


    # Main Game Loop
    current_score = 0
    best_score = 0
    running = True
    while running:
        # Set the score text:
        current_score_text = ('CURRENT SCORE: ' + str(current_score))
        current_score_text_color = (0, 255, 0)
    
        best_score_text = ('BEST SCORE: ' + str(best_score))
        best_score_text_color = (255, 255, 255)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and possible_directions_wsad[pygame.K_w]:
                    snake_direction = (0, -TILE_SIZE)
                    possible_directions_wsad = {pygame.K_w: 1, pygame.K_s: 0, pygame.K_a: 1, pygame.K_d: 1}
                if event.key == pygame.K_s and possible_directions_wsad[pygame.K_s]:
                    snake_direction = (0, TILE_SIZE)
                    possible_directions_wsad = {pygame.K_w: 0, pygame.K_s: 1, pygame.K_a: 1, pygame.K_d: 1}
                if event.key == pygame.K_a and possible_directions_wsad[pygame.K_a]:
                    snake_direction = (-TILE_SIZE, 0)
                    possible_directions_wsad = {pygame.K_w: 1, pygame.K_s: 1, pygame.K_a: 1, pygame.K_d: 0}
                if event.key == pygame.K_d and possible_directions_wsad[pygame.K_d]:
                    snake_direction = (TILE_SIZE, 0)
                    possible_directions_wsad = {pygame.K_w: 1, pygame.K_s: 1, pygame.K_a: 0, pygame.K_d: 1}
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and possible_directions_arrows[pygame.K_UP]:
                    snake_direction = (0, -TILE_SIZE)
                    possible_directions_arrows = {pygame.K_UP: 1, pygame.K_DOWN: 0, pygame.K_LEFT: 1, pygame.K_RIGHT: 1}
                if event.key == pygame.K_DOWN and possible_directions_arrows[pygame.K_DOWN]:
                    snake_direction = (0, TILE_SIZE)
                    possible_directions_arrows = {pygame.K_UP: 0, pygame.K_DOWN: 1, pygame.K_LEFT: 1, pygame.K_RIGHT: 1}
                if event.key == pygame.K_LEFT and possible_directions_arrows[pygame.K_LEFT]:
                    snake_direction = (-TILE_SIZE, 0)
                    possible_directions_arrows = {pygame.K_UP: 1, pygame.K_DOWN: 1, pygame.K_LEFT: 1, pygame.K_RIGHT: 0}
                if event.key == pygame.K_RIGHT and possible_directions_arrows[pygame.K_RIGHT]:
                    snake_direction = (TILE_SIZE, 0)
                    possible_directions_arrows = {pygame.K_UP: 1, pygame.K_DOWN: 1, pygame.K_LEFT: 0, pygame.K_RIGHT: 1}
            
        

        screen.fill((0, 0, 0))


        def draw_score():
            current_score_text_surface = font.render(current_score_text, True, (255, 255, 255))
            screen.blit(current_score_text_surface, (815, 50))

            best_score_text_surface = font.render(best_score_text, True, (0, 255, 0))
            screen.blit(best_score_text_surface, (852, 20))


        # Check Borders
        if snake.right > WINDOW:
            snake.left = 0
        if snake.top > WINDOW - TILE_SIZE:
            snake.top = 0
        if snake.right < TILE_SIZE:
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
            
            if current_score > best_score:
                best_score = current_score
            current_score = 0
            time_step = 100


        # Draw Snake
        [pygame.draw.rect(screen, (255, 255, 255), segment) for segment in segments]
    

        # Draw Food
        # if food_visible:
        pygame.draw.rect(screen, food_color, food)


        # Check Food Position
        if snake.center == food.center:
            food.center = get_random_position()
            length += 1
            current_score += 1
            draw_score()
            time_step -= 2
            food_color = random.choice(colors)


        # Move snake
        time_now = pygame.time.get_ticks()
        if time_now - time > time_step:
            time = time_now
            snake.move_ip(snake_direction)
            segments.append(snake.copy())
            segments = segments[-length:]


        draw_score()
        pygame.display.flip()
        clock.tick(60)
        # food_visible = not food_visible

        
snake_game()