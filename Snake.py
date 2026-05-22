import pygame, random
from pygame.locals import *
import time
def on_grid_random():
    x = random.randint(0, 59)
    y = random.randint(0, 59)
    return (x * 10, y * 10)


def collision(c1, c2):
    return (c1[0] == c2[0]) and (c1[1] == c2[1])


# controle.
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 4

my_direction_ai = LEFT


pygame.init()
background = pygame.image.load('FUNDO.jpeg')
background = pygame.transform.scale(background, (600, 600))  # Ajusta o tamanho da imagem

background2 = pygame.image.load('FUNDO2.jpg')
background2 = pygame.transform.scale(background2, (600, 600))  # Ajusta o tamanho da imagem


background3 = pygame.image.load('FUNDO3.jpg')
background3 = pygame.transform.scale(background3, (600, 600))  # Ajusta o tamanho da imagem
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Snake')

snake = [(200, 200), (210, 200), (220, 200)]
snake_skin = pygame.Surface((10, 10))
snake_skin.fill((255, 255, 0))

apple_pos = on_grid_random()
apple = pygame.Surface((10, 10))
apple.fill((255, 255, 255))

my_direction = LEFT

clock = pygame.time.Clock()

font = pygame.font.Font('freesansbold.ttf', 18)
score = 0
score2 = 0
fase = 1
vida = 3
snake_ai_color = 1
snake_color = 1

# Criação da Segunda Cobra
snake_ai = [(100, 100), (110, 100), (120, 100)]
snake_ai_skin = pygame.Surface((10, 10))
snake_ai_skin.fill((255, 0, 255))  # Cor da cobra AI

# Movimento da Cobra de IA
def move_snake_ai():
    global my_direction_ai
    if apple_pos[0] > snake_ai[0][0] and my_direction_ai != LEFT:
        my_direction_ai = RIGHT
    if apple_pos[0] < snake_ai[0][0] and my_direction_ai != RIGHT:
        my_direction_ai = LEFT
    if apple_pos[1] > snake_ai[0][1] and my_direction_ai != UP:
        my_direction_ai = DOWN
    if apple_pos[1] < snake_ai[0][1] and my_direction_ai != DOWN:
        my_direction_ai = UP

# Atualizar posição da cobra AI
# Adicione uma variável de controle para rastrear se a cobra deve se mover
deve_mover = True

def update_snake_ai():
    global my_direction_ai
    global deve_mover

    # Se a cobra não deve se mover, retorne imediatamente
    if not deve_mover:
        return

    if my_direction_ai == UP:
        next_position = (snake_ai[0][0], snake_ai[0][1] - 10)
    if my_direction_ai == DOWN:
        next_position = (snake_ai[0][0], snake_ai[0][1] + 10)
    if my_direction_ai == RIGHT:
        next_position = (snake_ai[0][0] + 10, snake_ai[0][1])
    if my_direction_ai == LEFT:
        next_position = (snake_ai[0][0] - 10, snake_ai[0][1])

    # Verifique se a próxima posição é segura
    if next_position in snake_ai or next_position in snake or next_position[0] < 0 or next_position[1] < 0 or next_position[0] > 590 or next_position[1] > 590:
        # Colisão detectada, mova a cobra para uma posição aleatória
        snake_ai[0] = on_grid_random()
    else:
        # Se a próxima posição for segura, atualize a posição da cobra
        snake_ai[0] = next_position
        # Se a cobra se moveu, ela deve continuar se movendo
        deve_mover = True




game_over = False
while not game_over:
    clock.tick(10)


    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_w and my_direction != DOWN:
                my_direction = UP
            if event.key == K_s and my_direction != UP:
                my_direction = DOWN
            if event.key == K_a and my_direction != RIGHT:
                my_direction = LEFT
            if event.key == K_d and my_direction != LEFT:
                my_direction = RIGHT


    if score < 30:
        fase = 1

    if score >= 30:
        fase = 2
    if score ==40:
        vida = vida+1

    if score >= 50:
        fase = 3
    if score ==50:
         vida = vida+1

    if score == 65:
        fase = 4

    if fase == 1:
        if collision(snake[0], apple_pos):
            apple_pos = on_grid_random()
            snake.append((0, 0))
            score = score + 1

        for i in range(len(snake) - 1, 0, -1):
            snake[i] = (snake[i - 1][0], snake[i - 1][1])


        # Atualizar posição.
        if my_direction == UP:
            snake[0] = (snake[0][0], snake[0][1] - 10)
        if my_direction == DOWN:
            snake[0] = (snake[0][0], snake[0][1] + 10)
        if my_direction == RIGHT:
            snake[0] = (snake[0][0] + 10, snake[0][1])
        if my_direction == LEFT:
            snake[0] = (snake[0][0] - 10, snake[0][1])
        screen.blit(background, (0, 0))
        screen.blit(apple, apple_pos)
    #CRIAR GRADE
        for x in range(0, 600, 10):  # Draw vertical lines
            pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, 600))
        for y in range(0, 600, 10):  # Draw vertical lines
            pygame.draw.line(screen, (40, 40, 40), (0, y), (600, y))

        #pontos
        score_font = font.render('Score: %s' % (score), True, (0, 0, 100))
        score_rect = score_font.get_rect()
        score_rect.topleft = (600 - 120, 10)
        screen.blit(score_font, score_rect)

        #fases
        fase_font = font.render('Fase: %s' % (fase), True, (0, 100, 0))
        fase_rect = fase_font.get_rect()
        fase_rect.topleft = (600 - 200, 10)
        screen.blit(fase_font, fase_rect)

        #vida
        vida_font = font.render('Vida: %s' % (vida), True, (200, 50, 100))
        vida_rect = vida_font.get_rect()
        vida_rect.topleft = (600 - 600, 10)
        screen.blit(vida_font, vida_rect)


        move_snake_ai()
        update_snake_ai()


        for pos in snake:
            screen.blit(snake_skin, pos)
        for pos in snake_ai:
            screen.blit(snake_ai_skin, pos)
        for i in range(len(snake_ai) - 1, 0, -1):
            snake_ai[i] = (snake_ai[i - 1][0], snake_ai[i - 1][1])
        if collision(snake_ai[0], apple_pos):
            apple_pos = on_grid_random()
            snake_ai.append((0, 0))
            score2 = score2 +  1
        # Alterne a cor da cobra controlada por IA entre preto e branco
        if snake_ai_color == 0:
            snake_ai_skin.fill((0, 45, 150))  # Branco
            snake_ai_color = 1
        else:
            snake_ai_skin.fill((100, 0, 0))  # Preto
            snake_ai_color = 0

        # ...
         # colisão
        if snake[0][0] == 600 or snake[0][1] == 600 or snake[0][0] < 0 or snake[0][1] < 0:
            vida = -1

        if vida < 0:
            break
        #colisão entre as cobras
        for i in range(1, len(snake_ai) - 1):
            if snake[0][0] == snake_ai[i][0] and snake[0][1] == snake_ai[i][1]:
                vida = vida - 1

        #colisão com proprio corpo
        for i in range(1, len(snake)):
            if snake[0][0] == snake[i][0] and snake[0][1] == snake[i][1]:
                vida = vida - 1
        if game_over:
            break

        pygame.display.update()
    if fase == 2:

        pygame.display.update()
        if collision(snake[0], apple_pos):
            apple_pos = on_grid_random()
            snake.append((0, 0))
            score = score + 1



        for i in range(len(snake) - 1, 0, -1):
            snake[i] = (snake[i - 1][0], snake[i - 1][1])
        # Atualizar posição.
        if my_direction == UP:
            snake[0] = (snake[0][0], snake[0][1] - 10)
        if my_direction == DOWN:
            snake[0] = (snake[0][0], snake[0][1] + 10)
        if my_direction == RIGHT:
            snake[0] = (snake[0][0] + 10, snake[0][1])
        if my_direction == LEFT:
            snake[0] = (snake[0][0] - 10, snake[0][1])
        screen.blit(background2, (0, 0))
        screen.blit(apple, apple_pos)
    #CRIAR GRADE
        #for x in range(0, 600, 10):  # Draw vertical lines
            #pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, 600))
        #for y in range(0, 600, 10):  # Draw vertical lines
            #pygame.draw.line(screen, (40, 40, 40), (0, y), (600, y))

        #pontos
        score_font = font.render('Score: %s' % (score), True, (0, 0, 100))
        score_rect = score_font.get_rect()
        score_rect.topleft = (600 - 120, 10)
        screen.blit(score_font, score_rect)

        #fases
        fase_font = font.render('Fase: %s' % (fase), True, (0, 100, 0))
        fase_rect = fase_font.get_rect()
        fase_rect.topleft = (600 - 200, 10)
        screen.blit(fase_font, fase_rect)

        #vida
        vida_font = font.render('Vida: %s' % (vida), True, (200, 55, 100))
        vida_rect = vida_font.get_rect()
        vida_rect.topleft = (600 - 600, 10)
        screen.blit(vida_font, vida_rect)


        move_snake_ai()
        update_snake_ai()


        for pos in snake:
            screen.blit(snake_skin, pos)
        for pos in snake_ai:
            screen.blit(snake_ai_skin, pos)
        for i in range(len(snake_ai) - 1, 0, -1):
            snake_ai[i] = (snake_ai[i - 1][0], snake_ai[i - 1][1])
        if collision(snake_ai[0], apple_pos):
            apple_pos = on_grid_random()
            snake_ai.append((0, 0))
            score2 = score2 +  1
        # Alterne a cor da cobra controlada por IA entre preto e branco
        if snake_ai_color == 0:
            snake_ai_skin.fill((0, 45, 150))  # Branco
            snake_ai_color = 1
        else:
            snake_ai_skin.fill((100, 0, 0))  # Preto
            snake_ai_color = 0

        # ...
         # colisão
        if snake[0][0] == 600 or snake[0][1] == 600 or snake[0][0] < 0 or snake[0][1] < 0:
            vida = -1

        if vida < 0:
            break
        #colisão entre as cobras
        for i in range(1, len(snake_ai) - 1):
            if snake[0][0] == snake_ai[i][0] and snake[0][1] == snake_ai[i][1]:
                vida = vida - 1

        #colisão com proprio corpo
        for i in range(1, len(snake)):
            if snake[0][0] == snake[i][0] and snake[0][1] == snake[i][1]:
                vida = vida - 1
        if game_over:
            break

        pygame.display.update()

    if fase == 3:

        pygame.display.update()
        if collision(snake[0], apple_pos):
            apple_pos = on_grid_random()
            snake.append((0, 0))
            score = score + 1



        for i in range(len(snake) - 1, 0, -1):
            snake[i] = (snake[i - 1][0], snake[i - 1][1])
        # Atualizar posição.
        if my_direction == UP:
            snake[0] = (snake[0][0], snake[0][1] - 10)
        if my_direction == DOWN:
            snake[0] = (snake[0][0], snake[0][1] + 10)
        if my_direction == RIGHT:
            snake[0] = (snake[0][0] + 10, snake[0][1])
        if my_direction == LEFT:
            snake[0] = (snake[0][0] - 10, snake[0][1])
        screen.blit(background3, (0, 0))
        screen.blit(apple, apple_pos)
    #CRIAR GRADE
        #for x in range(0, 600, 10):  # Draw vertical lines
            #pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, 600))
        #for y in range(0, 600, 10):  # Draw vertical lines
            #pygame.draw.line(screen, (40, 40, 40), (0, y), (600, y))

        #pontos
        score_font = font.render('Score: %s' % (score), True, (0, 0, 100))
        score_rect = score_font.get_rect()
        score_rect.topleft = (600 - 120, 10)
        screen.blit(score_font, score_rect)

        #fases
        fase_font = font.render('Fase: %s' % (fase), True, (100, 0, 0))
        fase_rect = fase_font.get_rect()
        fase_rect.topleft = (600 - 200, 10)
        screen.blit(fase_font, fase_rect)

        #vida
        vida_font = font.render('Vida: %s' % (vida), True, (200, 55, 100))
        vida_rect = vida_font.get_rect()
        vida_rect.topleft = (600 - 600, 10)
        screen.blit(vida_font, vida_rect)

        #pontos DO INIMIGO
        score2_font = font.render('Chefão: %s' % (score2), True, (158, 0, 0))
        score2_rect = score2_font.get_rect()
        score2_rect.topleft = (600 - 350, 10)
        screen.blit(score2_font, score2_rect)

        move_snake_ai()
        update_snake_ai()


        for pos in snake:
            screen.blit(snake_skin, pos)
        for pos in snake_ai:
            screen.blit(snake_ai_skin, pos)
        for i in range(len(snake_ai) - 1, 0, -1):
            snake_ai[i] = (snake_ai[i - 1][0], snake_ai[i - 1][1])
        if collision(snake_ai[0], apple_pos):
            apple_pos = on_grid_random()
            snake_ai.append((0, 0))
            score = score - 1
        # Alterne a cor da cobra controlada por IA entre preto e branco
        if snake_color == 0:
            snake_skin.fill((0, 150, 200))
            snake_color = 1
        else:
            snake_ai_skin.fill((200, 5, 200))
            snake_ai_color = 0

        # ...
         # colisão
        if snake[0][0] == 600 or snake[0][1] == 600 or snake[0][0] < 0 or snake[0][1] < 0:
            vida = -1

        if vida < 0:
            break
        #colisão entre as cobras
        for i in range(1, len(snake_ai) - 1):
            if snake[0][0] == snake_ai[i][0] and snake[0][1] == snake_ai[i][1]:
                vida = vida + 1
                score2 = score2 - 1

        #colisão com proprio corpo
        for i in range(1, len(snake)):
            if snake[0][0] == snake[i][0] and snake[0][1] == snake[i][1]:
                vida = vida - 1
        if game_over:
            break

        pygame.display.update()


    if fase == 4:

        game_over_font = pygame.font.Font('freesansbold.ttf', 50)
        game_over_screen = game_over_font.render('Você Venceu!!!', True, (55, 55, 55))
        game_over_rect = game_over_screen.get_rect()
        game_over_rect.midtop = (600 /2, 10)
        screen.blit(game_over_screen, game_over_rect)
        pygame.display.update()
        time.sleep(7)
        break


while True:
    game_over_font = pygame.font.Font('freesansbold.ttf', 75)
    game_over_screen = game_over_font.render('Game Over', True, (0, 0, 0))
    game_over_rect = game_over_screen.get_rect()
    game_over_rect.midtop = (600 / 2, 10)
    screen.blit(game_over_screen, game_over_rect)
    pygame.display.update()
    pygame.time.wait(500)
    while True:
        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                exit()
