import pygame

import sys

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 400

FPS = 30

WHITE = (255, 255, 255)

BLUE = (0, 0, 255)

RED = (255, 0, 0)

GREEN = (0, 255, 0)

BLACK = (0, 0, 0)

BUTTON_COLOR = (200, 200, 200)

BUTTON_HOVER_COLOR = (170, 170, 170)

CHARACTER_WIDTH = 30

CHARACTER_HEIGHT = 50

CHARACTER_SPACING = 10

missionary_image = pygame.image.load('missionary.png')

cannibal_image = pygame.image.load('cannibal.png')

boat_image = pygame.image.load('boat.png')

background_image = pygame.image.load('background_full.png')

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Missionaries and Cannibals Game")

clock = pygame.time.Clock()

missionaries_left = 3

cannibals_left = 3

missionaries_right = 0

cannibals_right = 0

boat_side = 'left'

boat_capacity = 2

boat_load = []

game_over = False

win = False

font = pygame.font.SysFont(None, 36)

go_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 30, 10, 60, 30)

reset_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 30, 50, 60, 30)

def draw_game_state():

    screen.fill(WHITE)

    screen.blit(background_image, (0, 0))

    draw_buttons()

    draw_characters_and_boat()

    if game_over:

        display_message("Game Over! Press Reset to restart", RED)

    if win:

        display_message("Congratulations! You Win!", GREEN)

        

def draw_buttons():

    draw_button(go_button_rect, "Go")

    draw_button(reset_button_rect, "Reset")

    

def draw_button(rect, text):

    mouse_x, mouse_y = pygame.mouse.get_pos()

    if rect.collidepoint((mouse_x, mouse_y)):

        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, rect)

    else:

        pygame.draw.rect(screen, BUTTON_COLOR, rect)

    text_surf = font.render(text, True, BLACK)

    text_rect = text_surf.get_rect(center=rect.center)

    screen.blit(text_surf, text_rect)

    

def draw_characters_and_boat():

    draw_side(50, missionaries_left, missionary_image, 50)  # Draw missionaries on the left

    draw_side(50, cannibals_left, cannibal_image, 100 + CHARACTER_HEIGHT + CHARACTER_SPACING)  # Draw cannibals on the left

    draw_side(SCREEN_WIDTH - 50, missionaries_right, missionary_image, 50, right=True)

    draw_side(SCREEN_WIDTH - 50, cannibals_right, cannibal_image, 100 + CHARACTER_HEIGHT + CHARACTER_SPACING, right=True)  # Draw cannibals on the right

    draw_boat()

    

def draw_side(x_offset, characters_count, character_img, start_y, right=False):

    for i in range(characters_count):

        x_position = x_offset - i * (CHARACTER_WIDTH + CHARACTER_SPACING) if right else x_offset + i * (CHARACTER_WIDTH + CHARACTER_SPACING)

        screen.blit(character_img, (x_position, start_y))

        

def draw_boat():

    boat_x = 150 if boat_side == 'left' else SCREEN_WIDTH - 150 - boat_image.get_width()

    boat_y = 230

    screen.blit(boat_image, (boat_x, boat_y))

    for idx, (m, c) in enumerate(boat_load):

        img = missionary_image if m else cannibal_image

        screen.blit(img, (boat_x + 20 + idx * 30, boat_y - 30))


def display_message(message, color):

    text_surf = font.render(message, True, color)

    text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    screen.blit(text_surf, text_rect)


def handle_click(pos):

    x, y = pos

    if go_button_rect.collidepoint(x, y):

        move_boat()

    elif reset_button_rect.collidepoint(x, y):

        reset_game()

    else:

        load_unload_people(x, y)

        

def load_unload_people(x, y):

    global missionaries_left, cannibals_left, missionaries_right, cannibals_right, boat_load, boat_side

    boat_x = 150 if boat_side == 'left' else SCREEN_WIDTH - 150 - boat_image.get_width()

    boat_y = 200

    if boat_x <= x <= boat_x + boat_image.get_width() and boat_y <= y <= boat_y + boat_image.get_height():

        unload_from_boat(x, y)

        return

    check_character_click(x, y, 50, 50, missionaries_left, missionary_image, 'left', (1, 0))

    check_character_click(x, y, 50, 100 + CHARACTER_HEIGHT + CHARACTER_SPACING, cannibals_left, cannibal_image, 'left', (0, 1))

    check_character_click(x, y, SCREEN_WIDTH - 50, 50, missionaries_right, missionary_image, 'right', (1, 0))

    check_character_click(x, y, SCREEN_WIDTH - 50, 100 + CHARACTER_HEIGHT + CHARACTER_SPACING, cannibals_right, cannibal_image, 'right', (0, 1))

    

def check_character_click(x, y, start_x, start_y, count, image, side, type):

    global boat_load, boat_side

    if len(boat_load) < 2:  # Make sure the boat does not exceed its capacity of 2

        if (side == 'left' and boat_side == 'left') or (side == 'right' and boat_side == 'right'):

            for i in range(count):

                img_x = start_x + i * (CHARACTER_WIDTH + CHARACTER_SPACING) if side == 'left' else start_x - i * (CHARACTER_WIDTH + CHARACTER_SPACING)

                if img_x <= x <= img_x + CHARACTER_WIDTH and start_y <= y <= start_y + CHARACTER_HEIGHT:

                    update_character_count(side, type)

                    break

def update_character_count(side, type):

  global missionaries_left, cannibals_left, missionaries_right, cannibals_right, boat_load

  if side == 'left':

    if type == (1, 0):

      missionaries_left -= 1

    else:

      cannibals_left -= 1

  else:

    if type == (1, 0):

        missionaries_right -= 1

    else:

        cannibals_right -= 1

  boat_load.append(type)

  
 
def unload_from_boat(x, y):

  global missionaries_left, cannibals_left, missionaries_right, cannibals_right, boat_load, boat_side

  boat_x = 150 if boat_side == 'left' else SCREEN_WIDTH - 150 - boat_image.get_width()

  for idx, (m, c) in enumerate(boat_load):

      person_x = boat_x + 20 + idx * 30

      if person_x <= x <= person_x + CHARACTER_WIDTH and 200 <= y <= 200 + CHARACTER_HEIGHT:

        if boat_side == 'left':

            if m:

                missionaries_left += 1

        else:

                cannibals_left += 1

      else:

          if m:

              missionaries_right += 1

          else:

              cannibals_right += 1

      boat_load.pop(idx)

      break

      
     
def reset_game():

    global missionaries_left, cannibals_left, missionaries_right, cannibals_right, boat_load, game_over, win, boat_side

    missionaries_left = 3

    cannibals_left = 3

    missionaries_right = 0

    cannibals_right = 0

    boat_side = 'left'

    boat_load = []

    game_over = False

    win = False

    

def check_game_state():

    global game_over, win

    if (missionaries_left < cannibals_left and missionaries_left > 0) or \
       (missionaries_right < cannibals_right and missionaries_right > 0):

        game_over = True

    elif missionaries_right == 3 and cannibals_right == 3 and len(boat_load) == 0:

        win = True

        

def move_boat():

    global boat_side, boat_load, game_over, win

    if not boat_load:

        return  # Cannot move an empty boat

    boat_side = 'left' if boat_side == 'right' else 'right'

    check_game_state()

    if game_over:

        print("Lost: Invalid move leads to a losing condition.")

    if win:

        print("Congratulations! You Win!")

        
       
running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

           running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:

             handle_click(pygame.mouse.get_pos())

      

    check_game_state()

    draw_game_state()

    pygame.display.flip()

    clock.tick(FPS)

    

pygame.quit()

sys.exit()