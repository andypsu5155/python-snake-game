import pygame
from random import randint
pygame.font.init()

WIDTH = 600
HEIGHT = 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

FPS = 120

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

FONT = pygame.font.SysFont('comicsans', 90)
MENU_FONT = pygame.font.SysFont('comicsans', 70)

GRID_WIDTH = 15
grid_rows = []
grid_columns = []

def draw_grid(rows, columns):
    for row in range(rows):
        grid_rows.append(pygame.Rect(0, HEIGHT/rows*(row+1)-GRID_WIDTH/2, WIDTH, GRID_WIDTH))
    for column in range(columns):
        grid_columns.append(pygame.Rect(WIDTH/columns*(column+1)-GRID_WIDTH/2, 0, GRID_WIDTH, HEIGHT))

def create_box(row, column):
    total_rows = len(grid_rows)
    total_columns = len(grid_columns)
    if row == 1:
        x = 0
        width = WIDTH / total_columns - GRID_WIDTH / 2
    else:
        width = WIDTH / total_columns - GRID_WIDTH
        x = (row-1)*(WIDTH/total_rows)+GRID_WIDTH/2
        height = HEIGHT / total_rows - GRID_WIDTH
    if column == 1:
        y = 0
        height = HEIGHT / total_rows - GRID_WIDTH / 2
    else:
        height = HEIGHT / total_rows - GRID_WIDTH
        y = (column - 1) * (HEIGHT / total_columns) + GRID_WIDTH / 2

    return pygame.Rect(x, y, width, height)

def draw_box(box, color):
    pygame.draw.rect(WIN, color, box)

def place_food(snake):
    x=randint(1, len(grid_columns))
    y=randint(1, len(grid_rows))
    for block in snake:
        if x == block[0] and y == block[1]:
            return place_food(snake)
    return [x, y]

def draw_window(snake, food_x, food_y):
    WIN.fill(WHITE)
    for grid in grid_rows:
        pygame.draw.rect(WIN, BLACK, grid)
    for grid in grid_columns:
        pygame.draw.rect(WIN, BLACK, grid)
    food_box = create_box(food_x, food_y)
    draw_box(food_box, BLUE)

    for block in snake:
        box = create_box(block[0], block[1])
        draw_box(box, GREEN)
    #player_box = create_box(snake[0][0], snake[0][1])
    #draw_box(player_box, GREEN)
    pygame.display.update()

def move_player(direction):
    if direction == "right":
        return [1, 0]
    elif direction == "up":
        return [0, -1]
    elif direction == "left":
        return [-1, 0]
    else:
        return [0, 1]
def move_box(box, dir):
    new_block = []
    if dir=="right":
        new_block = [box[0]+1, box[1]]
    elif dir == "up":
        new_block = [box[0], box[1]-1 ]
    elif dir == "down":
        new_block = [box[0], box[1]+1]
    else:
        new_block = [box[0]-1, box[1]]

    return new_block

def move_snake(snake, direction):
    new_snake = []
    i=0
    for block in snake:
        if i == 0:
            new_snake.append(move_box(block, direction))
        else:
            new_snake.append(snake[i-1])
        i+=1

    return new_snake

def add_to_snake(snake):
    length = len(snake)
    last_x = snake[length-1][0]
    second_last_x = snake[length-2][0]
    last_y = snake[length - 1][1]
    second_last_y = snake[length - 2][1]

    if last_x-second_last_x == -1:
        snake.append([last_x - 1, last_y])
    elif last_x-second_last_y == 1:
        snake.append([last_x + 1, last_y])
    elif last_y-second_last_y == -1:
        snake.append([last_x, last_y-1])
    else:
        snake.append([last_x, last_y+1])

def check_game_over(snake, rows, columns):
    i=0
    for block in snake:
        if i == 0:
            if block[0] < 1:
                return True
            elif block[0] > columns:
                return True
            elif block[1] < 1:
                return True
            elif block[1] > rows:
                return True
        elif snake[0] == block and i > 0:
            return True
        i+=1
def draw_winner(game_over_text, score_text):
    draw_text = FONT.render(game_over_text, 1, BLUE)
    score_text = FONT.render(score_text, 1, BLUE)
    WIN.blit(draw_text, (WIDTH / 2 - draw_text.get_width() / 2, HEIGHT / 2 - draw_text.get_height() / 2))
    WIN.blit(score_text, (WIDTH / 2 - score_text.get_width() / 2, HEIGHT / 2 - draw_text.get_height() / 2 + score_text.get_height()))
    pygame.display.update()
    pygame.time.delay(5000)
def draw_menu(menu_selection):
    WIN.fill(BLUE)
    if menu_selection == 0:
        menu_item1_text = MENU_FONT.render("Play Game", 1, GREEN)
    else:
        menu_item1_text = MENU_FONT.render("Play Game", 1, WHITE)

    if menu_selection == 1:
        menu_item2_text = MENU_FONT.render("View High Scores", 1, GREEN)
    else:
        menu_item2_text = MENU_FONT.render("View High Scores", 1, WHITE)

    if menu_selection == 2:
        menu_item3_text = MENU_FONT.render("Quit Game", 1, GREEN)
    else:
        menu_item3_text = MENU_FONT.render("Quit Game", 1, WHITE)
    WIN.blit(menu_item1_text, (WIDTH/2-menu_item1_text.get_width()/2, 0, menu_item1_text.get_width(), menu_item1_text.get_height()))
    WIN.blit(menu_item2_text, (WIDTH/2-menu_item2_text.get_width()/2, menu_item1_text.get_height(), menu_item2_text.get_width(), menu_item2_text.get_height()))
    WIN.blit(menu_item3_text, (WIDTH/2-menu_item3_text.get_width()/2, menu_item1_text.get_height()+menu_item2_text.get_height(), menu_item3_text.get_width(), menu_item3_text.get_height()))
    # WIN.blit(menu_item2_text, menu_item2_rect)
    # WIN.blit(menu_item3_text, menu_item3_rect)
    pygame.display.update()



def mainMenu():
    clock = pygame.time.Clock()
    run = True

    menu_selection = 0
    menu_choices = 3

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s and menu_selection < 2:
                    menu_selection+=1
                if event.key == pygame.K_w and menu_selection > 0:
                    menu_selection-=1
                if event.key == pygame.K_RETURN:
                    if menu_selection == 0:
                        mainGame()
                        run = False
                    if menu_selection == 2:
                        run = False
                        pygame.quit()

        draw_menu(menu_selection)

    pygame.quit()


def mainGame():
    clock = pygame.time.Clock()
    run = True
    snake = []
    player_x = 4
    player_y = 4
    snake += [[player_x, player_y]]

    score = 0

    rows = 8
    columns = 8
    draw_grid(rows,columns)

    direction = "right"

    frame_counter = 0
    speed = 30

    food_coord = place_food(snake)
    food_x = food_coord[0]
    food_y = food_coord[1]

    while run:
        clock.tick(FPS)
        frame_counter += 1

        if frame_counter >= speed:
            frame_counter = 0
            snake = move_snake(snake, direction)

            if snake[0][0] == food_x and snake[0][1] == food_y:
                food_coord = place_food(snake)
                food_x = food_coord[0]
                food_y = food_coord[1]
                speed-=1
                score+=1
                add_to_snake(snake)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    direction = "up"
                if event.key == pygame.K_a:
                    direction = "left"
                if event.key == pygame.K_s:
                    direction = "down"
                if event.key == pygame.K_d:
                    direction = "right"

        winner_text = ""
        if check_game_over(snake, rows, columns) == True:
            winner_text = "GAME OVER!"
            score_text = "Score: " + str(score)
            print(score)
            draw_winner(winner_text, score_text)
            grid_rows.clear()
            grid_columns.clear()
            mainMenu()




        draw_window(snake, food_x, food_y)

    pygame.quit()


# Calling the main function as long as the file name is main.py
if __name__ == '__main__':
    mainMenu()