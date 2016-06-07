import pygame, os, random, time, webbrowser, math
from random import randrange

from paths import *
from highscores import *
from shop_status import *

pygame.init()

fps = 30
clock = pygame.time.Clock()

display_width = 800
display_height = 600

middle_x = display_width / 2
middle_y = display_height / 2

white = (255, 255, 255)
black = (0, 0, 0)
orange = (255, 179, 71)
green = (124, 252, 0)
red = (187, 31, 54)
grey = (96, 96, 96)
light_grey = (128, 128, 128)

global coins
coins = 0

info_screen = 1

player_sprite = 1

sprite_selected = 1

capital_letters = { "a" : "A", "b" : "B", "c" : "C", "d" : "D", "e" : "E",
                    "f" : "F", "g" : "G", "h" : "H", "i" : "I", "j" : "J",
                    "k" : "K", "l" : "L", "m" : "M", "n" : "N", "o" : "O",
                    "p" : "P", "q" : "Q", "r" : "R", "s" : "S", "t" : "T",
                    "u" : "U", "v" : "V", "w" : "W", "x" : "X", "y" : "Y",
                    "z" : "Z"
                  }

letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
           "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

save_game_bool = 0

account_create_count = 0
type_section = 1
shift_count = 0
error_string = 1
username = ""
cursor_count = 0
cursor_status = True

load_game_count = 0

global mode
mode = 0
render_count = 7
frame_count = 0
second_count = 0
minute_count = 0

new = 2
url = "http://wallos901hsc.weebly.com/"

maze_size_count = 1

show_password = False

score_update_count = 0

screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Major Work - Tink")

background = pygame.image.load(imgpath["background"])
bg_scale = pygame.transform.scale(background, (800, 600))

maze_avatar = pygame.sprite.Group()
maze_finish = pygame.sprite.Group()
maze_boarder = pygame.sprite.Group()

def check_fullscreen():
    if screen.get_flags() & pygame.FULLSCREEN:
        screen.blit(background, (0, 0))
    else:    
        screen.blit(bg_scale, (0, 0))

class start_menu_button():
    def __init__(self, button, label_string, x, y):
        self.button = button
        self.label_string = label_string
        self.x = x
        self.y = y
        self.pos = (self.x, self.y)
        self.rect_outer = pygame.Rect(self.pos[0], self.pos[1], 300, 40)
        self.rect_inner = pygame.Rect((self.pos[0] + 5), (self.pos[1] + 5), 290, 30)
        self.selected = False

    def draw(self):
        pygame.draw.rect(screen, red, self.rect_outer)
        pygame.draw.rect(screen, white, self.rect_inner)
        font = pygame.font.SysFont(None, 30)
        label = font.render(str(self.label_string), True, red)
        label_size = font.size(self.label_string)
        screen.blit(label, ((middle_x - (label_size[0]/2)), (self.y + (label_size[1]/2))))


class home_screen_button():
    def __init__(self, button, label_string, x, y):
        self.button = button
        self.label_string = label_string
        self.x = x
        self.y = y
        self.pos = (self.x, self.y)
        self.rect_outer = pygame.Rect(self.pos[0], self.pos[1], 300, 40)
        self.rect_inner = pygame.Rect((self.pos[0] + 5), (self.pos[1] + 5), 290, 30)
        self.selected = False

    def draw(self):
        pygame.draw.rect(screen, red, self.rect_outer)
        pygame.draw.rect(screen, white, self.rect_inner)
        font = pygame.font.SysFont(None, 30)
        label = font.render(str(self.label_string), True, red)
        label_size = font.size(self.label_string)
        screen.blit(label, ((middle_x - (label_size[0]/2 + 125)), (self.y + (label_size[1]/2))))


class account_create_button():
    def __init__(self, button, label_string, x, y):
        self.button = button
        self.label_string = label_string
        self.x = x
        self.y = y
        self.pos = (self.x, self.y)
        self.rect_outer = pygame.Rect(self.pos[0], self.pos[1], 300, 45)
        self.rect_inner = pygame.Rect((self.pos[0] + 5), (self.pos[1] + 5), 290, 35)
        self.selected = False

    def draw(self):
        pygame.draw.rect(screen, red, self.rect_outer)
        pygame.draw.rect(screen, white, self.rect_inner)
        font = pygame.font.SysFont(None, 30)
        label = font.render(str(self.label_string), True, red)
        label_size = font.size(self.label_string)
        screen.blit(label, ((middle_x - (label_size[0]/2)), (self.y + (label_size[1]/2) + 2)))


class back_button_maze():
    def __init__(self, button, label_string, x, y):
        self.button = button
        self.label_string = label_string
        self.x = x
        self.y = y
        self.pos = (self.x, self.y)
        self.rect_outer = pygame.Rect(self.pos[0], self.pos[1], 140, 60)
        self.rect_inner = pygame.Rect((self.pos[0] + 5), (self.pos[1] + 5), 130, 50)
        self.selected = False

    def find_image(self):
        pass

    def draw(self):
        pygame.draw.rect(screen, red, self.rect_outer)
        pygame.draw.rect(screen, white, self.rect_inner)
        font = pygame.font.SysFont(None, 25)
        label = font.render(str(self.label_string), True, red)
        label_size = font.size(self.label_string)
        screen.blit(label, ((self.x + 70 - label_size[0]/2), (self.y + 30 - label_size[1]/2)))


class maze_cell(pygame.sprite.Sprite):
    def __init__(self, x, y, collide_able, colour, size):
        self.x = x
        self.y = y
        self.size = size
        self.collide_able = collide_able
        self.colour = colour
        if self.collide_able == 1:
            pygame.sprite.Sprite.__init__(self, maze_boarder)
        if self.collide_able == 3:
            pygame.sprite.Sprite.__init__(self, maze_finish)
        self.pos = (self.x, self.y)
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size, self.size)

    def draw(self):
        pygame.draw.rect(screen, self.colour, self.rect)
        

class maze_player(pygame.sprite.Sprite):
    def __init__(self, x, y, size, speed):
        pygame.sprite.Sprite.__init__(self, maze_avatar)
        self.x = x
        self.y = y
        self.temp_x = self.x
        self.temp_y = self.y
        self.size = size
        self.speed = speed

    def draw(self):
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        player_image = pygame.image.load(imgpath[("shop_" + str(player_sprite))][0])
        player_image = pygame.transform.smoothscale(player_image, (self.size, self.size))
        screen.blit(player_image, self.rect)

    def handle_keys(self):
        key = pygame.key.get_pressed()
        
        if key[pygame.K_RIGHT]:
            self.temp_x = self.x
            self.x += self.speed
        elif key[pygame.K_LEFT]:
            self.temp_x = self.x
            self.x -= self.speed
            
        elif key[pygame.K_UP]:
            self.temp_y = self.y
            self.y -= self.speed
        elif key[pygame.K_DOWN]:
            self.temp_y = self.y
            self.y += self.speed

    def collision_wall(self):
        self.x = self.temp_x
        self.y = self.temp_y


class setting_arrow():
    def __init__(self, button, x, y):
        self.button = button
        self.image = pygame.image.load(imgpath[self.button][0])
        self.x = x
        self.y = y
        self.pos = (self.x, self.y)
        self.selected = False
        self.size = 35
        self.rect_outer = pygame.Rect(self.pos[0], self.pos[1], self.size, self.size)

    def find_image(self):
        if self.selected == True:
            self.image = pygame.image.load(imgpath[self.button][1])
        else:
            self.image = pygame.image.load(imgpath[self.button][0])

    def draw(self):
        screen.blit(self.image, self.rect_outer)


class check_box():
    def __init__(self, button, x, y):
        self.button = button
        self.x = x
        self.y = y
        self.pos = (self.x, self.y)
        self.rect_outer = pygame.Rect(self.pos[0], self.pos[1], 25, 25)
        self.rect_inner = pygame.Rect((self.pos[0] + 3), (self.pos[1] + 3), 19, 19)
        self.selected = False

    def draw(self):
        pygame.draw.rect(screen, red, self.rect_outer)
        pygame.draw.rect(screen, white, self.rect_inner)

class shop_button():
    def __init__(self, button, number, x, y):
        self.button = button
        self.number = number
        self.x = x
        self.y = y
        self.pos = (self.x, self.y)
        self.rect_outer = pygame.Rect(self.pos[0], self.pos[1], 150, 45)
        self.rect_inner = pygame.Rect((self.pos[0] + 5), (self.pos[1] + 5), 140, 35)
        self.selected = False

    def find_image(self):
        pass

    def draw(self):
        
        if self.number == 1:
            colour_1 = red
            colour_2 = white
        elif self.number == 2:
            if sprite_status[sprite_selected] == True:
                colour_1 = red
                colour_2 = white
            elif sprite_status[sprite_selected] == False:
                colour_1 = light_grey
                colour_2 = grey

        if self.number == 1:
            if sprite_status[sprite_selected] == True:
                label_string = "Purchased"
            elif sprite_status[sprite_selected] == False:
                label_string = "Buy"
        elif self.number == 2:
            if player_sprite == sprite_selected:
                label_string = "Selected"
            else:
                label_string = "Select"
                
        pygame.draw.rect(screen, colour_1, self.rect_outer)
        pygame.draw.rect(screen, colour_2, self.rect_inner)
        font = pygame.font.SysFont(None, 35)
        label = font.render(str(label_string), True, colour_1)
        label_size = font.size(label_string)
        screen.blit(label, ((self.pos[0] + 75 - (label_size[0]/2)), (self.pos[1] + 10)))
        

new_game               = start_menu_button("new_game", "New Game", (middle_x - 150), (middle_y - 90))
load_game              = start_menu_button("load_game", "Load Game", (middle_x - 150), (middle_y - 10))
instructions           = start_menu_button("instructions", "Instructions", (middle_x - 150), (middle_y + 70))
website                = start_menu_button("website", "Website", (middle_x - 150), (middle_y + 150))

maze                   = home_screen_button("maze", "Enter the Maze", (middle_x - 275), (middle_y - 120))
shop                   = home_screen_button("shop", "Shop", (middle_x - 275), (middle_y - 40))
save_game              = home_screen_button("save_game", "Save Game", (middle_x - 275), (middle_y + 40))
settings               = home_screen_button("settings", "Settings", (middle_x - 275), (middle_y + 120))
back_to_home_menu      = back_button_maze("back_to_menu", "Back to Menu", 647, 45)

back_to_menu_maze      = back_button_maze("back_to_menu", "Back to Menu", 630, 520)

size_setting_left      = setting_arrow("size_setting_left", (middle_x + 100), 188)
size_setting_right     = setting_arrow("size_setting_right", (middle_x + 250), 188)
back_to_menu_settings  = back_button_maze("back_to_menu", "Back to Menu", 647, 45)

create_account         = account_create_button("create_account", "Create Account", (middle_x - 150), 515)
password_check_box     = check_box("password_check_box", (middle_x + 100), 399)
back_to_menu_create    = back_button_maze("back_to_menu_create", "Back to Menu", 647, 45)

load_game_button       = account_create_button("load_game", "Load Game", (middle_x - 150), 515)
password_check_box_1   = check_box("password_check_box_1", (middle_x + 100), 399)
back_to_menu_load      = back_button_maze("back_to_menu_load", "Back to Menu", 647, 45)

back_to_menu_end       = back_button_maze("back_to_menu_end", "Back to Menu", 10, 70)
play_again_end         = back_button_maze("play_again_end", "Play Again", (middle_x + 250), 70)

back_to_menu_shop      = back_button_maze("back_to_menu_shop", "Back to Menu", 647, 45)
shop_select_left       = setting_arrow("size_setting_left", (middle_x - 155), (middle_y - 17))
shop_select_right      = setting_arrow("size_setting_right", (middle_x + 120), (middle_y - 17))
purchase_button        = shop_button("purchase_button", 1, (middle_x - 200), (middle_y + 200))
select_button          = shop_button("select_button", 2, (middle_x + 50), (middle_y + 200))

back_to_menu_ins       = back_button_maze("back_to_menu_ins", "Back to Menu", 647, 45)

start_menu_options     = [new_game, load_game, instructions, website]
home_screen_options    = [maze, shop, save_game, settings, back_to_home_menu]
maze_screen_options    = [back_to_menu_maze]
settings_options       = [size_setting_left, size_setting_right, back_to_menu_settings]
account_create_options = [create_account, password_check_box, back_to_menu_create]
load_game_options      = [load_game_button, password_check_box_1, back_to_menu_load]
game_over_options      = [back_to_menu_end, play_again_end]
shop_screen_options    = [back_to_menu_shop, shop_select_left, shop_select_right, purchase_button, select_button]
ins_screen_options     = [back_to_menu_ins]

def button_selection():

    global mode
    global new
    global url
    global maze_count
    global mazeplayer
    global maze_size_count
    global render_count
    global show_password
    global username
    global password
    global confirm_password
    global error_string
    global frame_count
    global points
    global second_count
    global minute_count
    global high_score_small
    global high_score_medium
    global high_score_large
    global save_game_bool
    global account_create_count
    global load_game_count
    global type_section
    global sprite_selected
    global player_sprite
    global coins

    mouse_click = pygame.mouse.get_pressed()[0]

    if mouse_click != 0:

        if new_game.selected and mode == 0:
            account_create_count = 0
            type_section = 1
            error_string = 1
            mode = 8
        elif load_game.selected and mode == 0:
            load_game_count = 0
            type_section = 1
            error_string = 1
            mode = 2
        elif instructions.selected and mode == 0:
            mode = 3
        elif website.selected and mode == 0:
            webbrowser.open(url, new=new)
            website.selected = False
            save_game_bool = 0
            mode = 0
        elif maze.selected and mode == 1:
            mode = 4
            render_count = 0
            frame_count = 0
            second_count = 0
            minute_count = 0
            points = 300
            maze_gen()
            if maze_size_count == 1:
                mazeplayer = maze_player(245, 145, 15, 4)
            elif maze_size_count == 2:
                mazeplayer = maze_player(226, 126, 10, 3)
            elif maze_size_count == 3:
                mazeplayer = maze_player(218, 118, 5, 2)
        elif shop.selected and mode == 1:
            sprite_selected = 1
            error_string = 0
            mode = 5
        elif save_game.selected and mode == 1:
            file = open((os.path.join('data/saves', (username + '.txt'))), 'w')
            file.write(username + "\n")
            file.write(password + "\n")
            file.write(str(coins) + "\n")
            file.write(str(high_scores["small_1"])  + "\n")
            file.write(str(high_scores["small_2"])  + "\n")
            file.write(str(high_scores["small_3"])  + "\n")
            file.write(str(high_scores["medium_1"]) + "\n")
            file.write(str(high_scores["medium_2"]) + "\n")
            file.write(str(high_scores["medium_3"]) + "\n")
            file.write(str(high_scores["large_1"])  + "\n")
            file.write(str(high_scores["large_2"])  + "\n")
            file.write(str(high_scores["large_3"])  + "\n")
            file.write(str(player_sprite) + "\n")
            for i in sprite_status:
                file.write(str(sprite_status[i]) + "\n")
            file.close()

            for i in high_scores:
                if len(str(high_scores[i])) == 1:
                    high_scores[i] = ("00" + str(high_scores[i]))
                elif len(str(high_scores[i])) == 2:
                    high_scores[i] = ("0" + str(high_scores[i]))
                elif len(str(high_scores[i])) == 3:
                    high_scores[i] = str(high_scores[i])

            save_game_bool = 1
        elif settings.selected and mode == 1:
            mode = 7
        elif back_to_home_menu.selected and mode == 1:
            mode = 0
        elif back_to_menu_maze.selected and mode == 4:
            save_game_bool = 0
            mode = 1
        elif size_setting_left.selected and mode == 7:
            if maze_size_count == 1:
                maze_size_count = 1
            else:
                maze_size_count -= 1
        elif size_setting_right.selected and mode == 7:
            if maze_size_count == 3:
                maze_size_count = 3
            else:
                maze_size_count += 1
        elif back_to_menu_settings.selected and mode == 7:
            save_game_bool = 0
            mode = 1
        elif create_account.selected and mode == 8:
            if password == confirm_password:
                if not os.path.exists(os.path.join('data/saves', (username + '.txt'))):
                    file = open((os.path.join('data/saves', (username + '.txt'))), 'w')
                    file.write(username + "\n")
                    file.write(password + "\n")
                    file.write(str(coins) + "\n")
                    file.write(str(high_scores["small_1"])  + "\n")
                    file.write(str(high_scores["small_2"])  + "\n")
                    file.write(str(high_scores["small_3"])  + "\n")
                    file.write(str(high_scores["medium_1"]) + "\n")
                    file.write(str(high_scores["medium_2"]) + "\n")
                    file.write(str(high_scores["medium_3"]) + "\n")
                    file.write(str(high_scores["large_1"])  + "\n")
                    file.write(str(high_scores["large_2"])  + "\n")
                    file.write(str(high_scores["large_3"])  + "\n")
                    file.write(str(player_sprite) + "\n")
                    for i in sprite_status:
                        file.write(str(sprite_status[i]) + "\n")
                    file.close()

                    for i in high_scores:
                        if len(str(high_scores[i])) == 1:
                            high_scores[i] = ("00" + str(high_scores[i]))
                        elif len(str(high_scores[i])) == 2:
                            high_scores[i] = ("0" + str(high_scores[i]))
                        elif len(str(high_scores[i])) == 3:
                            high_scores[i] = str(high_scores[i])

                    save_game_bool = 0
                    mode = 1
                else:
                    error_string = 3
            else:
                error_string = 2
        elif password_check_box.selected and mode == 8:
            if show_password == True:
                show_password = False
            elif show_password == False:
                show_password = True
        elif back_to_menu_end.selected and mode == 9:
            save_game_bool = 0
            mode = 1
        elif play_again_end.selected and mode == 9:
            mode = 4
            render_count = 0
            frame_count = 0
            second_count = 0
            minute_count = 0
            points = 300
            maze_gen()
            if maze_size_count == 1:
                mazeplayer = maze_player(245, 145, 15, 4)
            elif maze_size_count == 2:
                mazeplayer = maze_player(226, 126, 10, 3)
            elif maze_size_count == 3:
                mazeplayer = maze_player(218, 118, 5, 2)
        elif load_game_button.selected and mode == 2:
            if os.path.exists(os.path.join('data/saves', (username + '.txt'))):
                file = open((os.path.join('data/saves', (username + '.txt'))), 'r')
                file_strings = file.readlines()
                if password == file_strings[1].strip():
                    username = file_strings[0].strip()
                    password = file_strings[1].strip()
                    coins = int(file_strings[2].strip())
                    high_scores["small_1"] = file_strings[3].strip()
                    high_scores["small_2"] = file_strings[4].strip()
                    high_scores["small_3"] = file_strings[5].strip()
                    high_scores["medium_1"] = file_strings[6].strip()
                    high_scores["medium_2"] = file_strings[7].strip()
                    high_scores["medium_3"] = file_strings[8].strip()
                    high_scores["large_1"] = file_strings[9].strip()
                    high_scores["large_2"] = file_strings[10].strip()
                    high_scores["large_3"] = file_strings[11].strip()
                    player_sprite = int(file_strings[12].strip())

                    pos = 1
                    for i in range(10):
                        if file_strings[i + 13].strip() == "True":
                            sprite_status[pos] = True
                        elif file_strings[i + 13].strip() == "False":
                            sprite_status[pos] = False
                        pos += 1

                    for i in high_scores:
                        if len(str(high_scores[i])) == 1:
                            high_scores[i] = ("00" + str(high_scores[i]))
                        elif len(str(high_scores[i])) == 2:
                            high_scores[i] = ("0" + str(high_scores[i]))
                        elif len(str(high_scores[i])) == 3:
                            high_scores[i] = str(high_scores[i])

                    save_game_bool = 0
                    mode = 1
                else:
                    error_string = 2
            else:
                error_string = 2
        elif password_check_box_1.selected and mode == 2:
            if show_password == True:
                show_password = False
            elif show_password == False:
                show_password = True
        elif back_to_menu_load.selected and mode == 2:
            mode = 0
        elif back_to_menu_create.selected and mode == 8:
            mode = 0
        elif back_to_menu_shop.selected and mode == 5:
            save_game_bool = 0
            mode = 1
        elif shop_select_left.selected and mode == 5:
            error_string = 0
            if sprite_selected != 1:
                sprite_selected -= 1
            else:
                sprite_selected = 1
        elif shop_select_right.selected and mode == 5:
            error_string = 0
            if sprite_selected != 10:
                sprite_selected += 1
            else:
                sprite_selected = 10
        elif purchase_button.selected and mode == 5:
            error_string = 0
            if sprite_status[sprite_selected] == False:
                if coins >= sprite_costs[sprite_selected]:
                    coins -= sprite_costs[sprite_selected]
                    sprite_status[sprite_selected] = True
                    player_sprite = sprite_selected
                else:
                    error_string = 1
            else:
                error_string = 2
        elif select_button.selected and mode == 5:
            if sprite_status[sprite_selected] == True:
                player_sprite = sprite_selected
        elif back_to_menu_ins.selected and mode == 3:
            mode = 0
            

                
        time.sleep(0.2)



def start_menu():

    check_fullscreen()

    heading_box_outer = pygame.Rect((middle_x - 250), 50, 500, 100)
    pygame.draw.rect(screen, red, heading_box_outer)
    
    heading_box_inner = pygame.Rect((middle_x - 240), 60, 480, 80)
    pygame.draw.rect(screen, white, heading_box_inner)

    heading_string  = "Tink"
    heading_font = pygame.font.SysFont(None, 75)
    heading = heading_font.render(str(heading_string), True, red)
    heading_size = heading_font.size(heading_string)
    screen.blit(heading, ((middle_x - (heading_size[0]/2)), (middle_y - 225)))

    credit_string = "Created by Ben Walton 12SDD     Version 1.10.7"
    credit_font = pygame.font.SysFont(None, 20)
    credit = credit_font.render(str(credit_string), True, red)
    credit_size = credit_font.size(credit_string)
    screen.blit(credit, ((middle_x - (credit_size[0]/2)), (600 - 20)))

    for button in start_menu_options:
        if button.rect_outer.collidepoint(pygame.mouse.get_pos()):
            button.selected = True
        else:
            button.selected = False
        button.draw()

    pygame.display.update()
    button_selection()

    

def home_screen():

    global username

    check_fullscreen()

    heading_box_outer = pygame.Rect((middle_x - 375), 25, 500, 100)
    pygame.draw.rect(screen, red, heading_box_outer)

    heading_box_inner = pygame.Rect((middle_x - 365), 35, 480, 80)
    pygame.draw.rect(screen, white, heading_box_inner)

    hs_box_outer = pygame.Rect((middle_x + 100), (middle_y - 120), 200, 280)
    pygame.draw.rect(screen, red, hs_box_outer)

    hs_box_inner = pygame.Rect((middle_x + 105), (middle_y - 115), 190, 270)
    pygame.draw.rect(screen, white, hs_box_inner)

    heading_string = "Welcome, " + username
    heading_font = pygame.font.SysFont(None, 55)
    heading = heading_font.render(str(heading_string), True, red)
    heading_size = heading_font.size(heading_string)
    screen.blit(heading, ((middle_x - (heading_size[0]/2 + 125)), (middle_y - (heading_size[1]/2 + 225))))

    fact_string = "Random Fact About the Game"
    fact_font = pygame.font.SysFont(None, 25)
    fact = fact_font.render(str(fact_string), True, red)
    fact_size = fact_font.size(fact_string)
    screen.blit(fact, ((middle_x - (fact_size[0]/2 + 125)), (600 - 80)))

    hs_heading_string = "High Scores"
    hs_heading_font = pygame.font.SysFont(None, 35)
    hs_heading = hs_heading_font.render(str(hs_heading_string), True, red)
    hs_heading_size = hs_heading_font.size(hs_heading_string)
    screen.blit(hs_heading, ((middle_x + 130), (195)))

    hs_small_string = "Small         : " + str(high_scores["small_1"])
    hs_medium_string = "Medium      : " + str(high_scores["medium_1"])
    hs_large_string = "Large         : " + str(high_scores["large_1"])
    hs_scores_font = pygame.font.SysFont(None, 30)
    hs_small = hs_scores_font.render(str(hs_small_string), True, red)
    hs_medium = hs_scores_font.render(str(hs_medium_string), True, red)
    hs_large = hs_scores_font.render(str(hs_large_string), True, red)
    screen.blit(hs_small, ((middle_x + 125), (250)))
    screen.blit(hs_medium, ((middle_x + 125), (320)))
    screen.blit(hs_large, ((middle_x + 125), (390)))

    for button in home_screen_options:
        if button.rect_outer.collidepoint(pygame.mouse.get_pos()):
            button.selected = True
        else:
            button.selected = False
        button.draw()

    pygame.display.update()
    button_selection()

def maze_gen():

    global maze_size
    global maze_size_count
    
    if maze_size_count == 1:
        maze_size = 13
    elif maze_size_count == 2:
        maze_size = 23
    elif maze_size_count == 3:
        maze_size = 39
    
    global tile_size
    tile_size = round((390/maze_size), 1)

    global maze_boarder
    maze_boarder.empty()

    global maze_finish
    maze_finish.empty()

    if maze_size_count == 1:
        spawn_distance = 7
    elif maze_size_count == 2:
        spawn_distance = 17
    elif maze_size_count == 3:
        spawn_distance = 33

    evens = []
    odds = []
    boundaries = [0, (maze_size - 1)]

    maze_cells = []
    maze_walls = []

    cell_stack = []
    visited_cells = []
    unvisited_cells = []

    avaiable_cells = []

    current_cell = (0, 0)

    global grid
    grid = []

    end_cell_count = 0
    end_cell_count2 = 0

    list_placing_count = 0
    temp_count = 0
    while list_placing_count != (maze_size):
        if temp_count == 0:
            evens.append(list_placing_count)
            temp_count = 1
        elif temp_count == 1:
            odds.append(list_placing_count)
            temp_count = 0
        list_placing_count += 1

    for row in range(maze_size):
        grid.append([])
        for column in range(maze_size):
            if row in evens or column in evens:
                grid[row].append("#")
            else:
                grid[row].append(".")
    
    x_pos = 0
    y_pos = 0
    a = 0
    for x in grid:
        for y in x:
            if x_pos in odds and y_pos in odds:
                temp = (x_pos, y_pos)
                maze_cells.append(temp)
            elif x_pos in boundaries or y_pos in boundaries:
                a = a + 1
            else:
                temp = (x_pos, y_pos)
                maze_walls.append(temp)
            y_pos = y_pos + 1
        x_pos = x_pos + 1
        y_pos = 0


    for i in maze_cells:
        unvisited_cells.append(i)

    global start_cell
    start_cell = random.choice(maze_cells)
    visited_cells.append(start_cell)
    unvisited_cells.remove(start_cell)
    current_cell = start_cell
    total_cells = 49
    
    while len(unvisited_cells) != 0:

        available_cells = []

        north = (current_cell[0], (current_cell[1] - 2))
        south = (current_cell[0], (current_cell[1] + 2))
        east  = ((current_cell[0] + 2), current_cell[1])
        west  = ((current_cell[0] - 2), current_cell[1])

        north_break = (current_cell[0], (current_cell[1] - 1))
        south_break = (current_cell[0], (current_cell[1] + 1))
        east_break  = ((current_cell[0] + 1), current_cell[1])
        west_break  = ((current_cell[0] - 1), current_cell[1])

        directions = [north, south, east, west]

        break_paths = {
                            north   :   north_break,
                            south   :   south_break,
                            east    :   east_break,
                            west    :   west_break
                      }

        for i in directions:
            for k in unvisited_cells:
                if i == k:
                    if 0 < i[0] < (maze_size - 1):
                        if 0 < i[1] < (maze_size - 1):
                            available_cells.append(i)

        if len(available_cells) != 0:

            chosen_cell = random.choice(available_cells)
            cell_stack.append(chosen_cell)

            if chosen_cell == north:
                wall_break = north_break
            elif chosen_cell == south:
                wall_break = south_break
            elif chosen_cell == east:
                wall_break = east_break
            elif chosen_cell == west:
                wall_break = west_break

            grid[wall_break[0]][wall_break[1]] = "."

            current_cell = chosen_cell
            visited_cells.append(current_cell)
            unvisited_cells.remove(current_cell)
            end_cell_count += 1

            if end_cell_count2 == 0:
                if end_cell_count >= 10:
                    if current_cell[0] >= spawn_distance:
                        if current_cell[1] >= spawn_distance:
                            end_cell = current_cell
                            grid[current_cell[0]][current_cell[1]] = "*"
                            end_cell_count2 += 1

        else:
            popped_cell = cell_stack.pop()
            current_cell = popped_cell

    count111 = 0
    for row in grid:
        for i in row:
            if i == "*":
                count111 += 1

    if count111 == 0:
        grid[11][11] = "*"
            

def maze_screen():

    global mazeplayer
    global fps
    global grid
    global mode
    global maze_size_count
    global render_count
    global frame_count
    global minute_count
    global second_count
    global points
    global x
    global score_update_count
    
    check_fullscreen()

    gamestats_box_outer = pygame.Rect(20, 100, 160, 400)
    pygame.draw.rect(screen, red, gamestats_box_outer)

    gamestats_box_inner = pygame.Rect(25, 105, 150, 390)
    pygame.draw.rect(screen, white, gamestats_box_inner)

    hs_box_outer = pygame.Rect(620, 100, 160, 400)
    pygame.draw.rect(screen, red, hs_box_outer)

    hs_box_inner = pygame.Rect(625, 105, 150, 390)
    pygame.draw.rect(screen, white, hs_box_inner)

    maze_box_outer = pygame.Rect(200, 100, 400, 400)
    pygame.draw.rect(screen, red, maze_box_outer)

    maze_box_inner = pygame.Rect(205, 105, 390, 390)
    pygame.draw.rect(screen, white, maze_box_inner)

    if maze_size_count == 1:
        point_edit = 12
    elif maze_size_count == 2:
        point_edit = 7
    elif maze_size_count == 3:
        point_edit = 2

    frame_count += 1
    if frame_count == 30:
        second_count += 1
        frame_count = 0
        points -= point_edit
    if second_count == 60:
        minute_count += 1
        second_count = 0

    if len(str(second_count)) == 1:
        second_display = "0" + str(second_count)
    elif len(str(second_count)) == 2:
        second_display = str(second_count)

    if len(str(minute_count)) == 1:
        minute_display = "0" + str(minute_count)
    elif len(str(minute_count)) == 2:
        minute_display = str(minute_count)
    
    if render_count == 0:
        x = (205 - tile_size)
        y = (105 - tile_size)
        count = 0
        for row in grid:
            y = y + tile_size
            for cell in row:
                if count == maze_size:
                    x = 205
                    count = 0
                else:
                    x = x + tile_size
                if cell == "#":
                    colour = red
                    collide_able = 1
                elif cell == ".":
                    colour = white
                    collide_able = 2
                elif cell == "*":
                    colour = green
                    collide_able = 3
                i = maze_cell(x, y, collide_able, colour, tile_size)
                i.draw()
                count = count + 1
        rect = pygame.Rect(205, 105, 390, 390)
        global sub
        sub = pygame.Surface((390, 390))
        sub.blit(screen, (0, 0), (205, 105, 390, 390))
        render_count += 1

    screen.blit(sub, (205, 105))

    time_label_string = "Time Elapsed"
    time_label_font = pygame.font.SysFont(None, 30)
    time_label = time_label_font.render(str(time_label_string), True, red)
    time_label_size = time_label_font.size(time_label_string)
    screen.blit(time_label, ((100 - (time_label_size[0]/2)), 130))

    time_counter_string = minute_display + ":" + second_display + " mins"
    time_counter_font = pygame.font.SysFont(None, 30)
    time_counter = time_counter_font.render(str(time_counter_string), True, red)
    time_counter_size = time_counter_font.size(time_counter_string)
    screen.blit(time_counter, ((100 - (time_counter_size[0]/2)), 220))

    score_label_string = "Score"
    score_label_font = pygame.font.SysFont(None, 30)
    score_label = score_label_font.render(str(score_label_string), True, red)
    score_label_size = score_label_font.size(score_label_string)
    screen.blit(score_label, ((100 - (score_label_size[0]/2)), 310))

    if points < 0:
        points = 0

    if len(str(points)) == 1:
        temp_points = ("00" + str(points))
    elif len(str(points)) == 2:
        temp_points = ("0" + str(points))
    elif len(str(points)) == 3:
        temp_points = str(points)

    score_counter_string = temp_points + " Points"
    score_counter_font = pygame.font.SysFont(None, 30)
    score_counter = score_counter_font.render(str(score_counter_string), True, red)
    score_counter_size = score_counter_font.size(score_counter_string)
    screen.blit(score_counter, ((100 - (score_counter_size[0]/2)), 400))

    hs_label_string = "High Scores"
    hs_label_font = pygame.font.SysFont(None, 30)
    hs_label = hs_label_font.render(str(hs_label_string), True, red)
    hs_label_size = hs_label_font.size(hs_label_string)
    screen.blit(hs_label, ((700 - (hs_label_size[0]/2)), 130))

    if maze_size_count == 1:
        hs_1_string = "1: " + high_scores["small_1"] + " Points"
        hs_2_string = "2: " + high_scores["small_2"] + " Points"
        hs_3_string = "3: " + high_scores["small_3"] + " Points"
    elif maze_size_count == 2:
        hs_1_string = "1: " + high_scores["medium_1"] + " Points"
        hs_2_string = "2: " + high_scores["medium_2"] + " Points"
        hs_3_string = "3: " + high_scores["medium_3"] + " Points"
    elif maze_size_count == 3:
        hs_1_string = "1: " + high_scores["large_1"] + " Points"
        hs_2_string = "2: " + high_scores["large_2"] + " Points"
        hs_3_string = "3: " + high_scores["large_3"] + " Points"
        
    hs_1_font = pygame.font.SysFont(None, 30)
    hs_1 = hs_1_font.render(str(hs_1_string), True, red)
    hs_1_size = hs_1_font.size(hs_1_string)
    screen.blit(hs_1, ((700 - (hs_1_size[0]/2)), 220))

    hs_2_font = pygame.font.SysFont(None, 30)
    hs_2 = hs_2_font.render(str(hs_2_string), True, red)
    hs_2_size = hs_2_font.size(hs_2_string)
    screen.blit(hs_2, ((700 - (hs_2_size[0]/2)), 310))

    hs_3_font = pygame.font.SysFont(None, 30)
    hs_3 = hs_3_font.render(str(hs_3_string), True, red)
    hs_3_size = hs_3_font.size(hs_3_string)
    screen.blit(hs_3, ((700 - (hs_3_size[0]/2)), 400))

    mazeplayer.handle_keys()
    mazeplayer.draw()

    collide_wall = pygame.sprite.spritecollideany(mazeplayer, maze_boarder, False)
    collide_finish = pygame.sprite.spritecollideany(mazeplayer, maze_finish, False)

    key = pygame.key.get_pressed()

    if collide_wall:
        mazeplayer.collision_wall()
    if collide_finish:
        x = 1
        score_update_count = 0
        mode = 9

    for button in maze_screen_options:
        if button.rect_outer.collidepoint(pygame.mouse.get_pos()):
            button.selected = True
        else:
            button.selected = False
        button.draw()

    clock.tick(fps)
    pygame.display.flip()
    button_selection()


def settings_screen():

    global maze_size_count

    check_fullscreen()

    heading_box_outer = pygame.Rect((middle_x - 235), 25, 470, 100)
    pygame.draw.rect(screen, red, heading_box_outer)
    
    heading_box_inner = pygame.Rect((middle_x - 225), 35, 450, 80)
    pygame.draw.rect(screen, white, heading_box_inner)

    settings_box_outer = pygame.Rect((middle_x - 375), 150, 750, 425)
    pygame.draw.rect(screen, red, settings_box_outer)

    settings_box_inner = pygame.Rect((middle_x - 365), 160, 730, 405)
    pygame.draw.rect(screen, white, settings_box_inner)

    heading_string = "Settings"
    heading_font = pygame.font.SysFont(None, 75)
    heading = heading_font.render(str(heading_string), True, red)
    heading_size = heading_font.size(heading_string)
    screen.blit(heading, ((400 - (heading_size[0]/2)), 48))

    size_setting_string = "Maze Size:"
    size_setting_font = pygame.font.SysFont(None, 35)
    size_setting = size_setting_font.render(str(size_setting_string), True, red)
    size_setting_size = heading_font.size(size_setting_string)
    screen.blit(size_setting, ((middle_x - 300), 195))

    if maze_size_count == 1:
        size_string = "Small"
        size_font = pygame.font.SysFont(None, 30)
        size = size_font.render(str(size_string), True, red)
        size_size = size_font.size(size_string)
        screen.blit(size, ((middle_x + 192.5 - (size_size[0]/2)), 197.5))
    elif maze_size_count == 2:
        size_string = "Medium"
        size_font = pygame.font.SysFont(None, 30)
        size = size_font.render(str(size_string), True, red)
        size_size = size_font.size(size_string)
        screen.blit(size, ((middle_x + 192.5 - (size_size[0]/2)), 197.5))
    elif maze_size_count == 3:
        size_string = "Large"
        size_font = pygame.font.SysFont(None, 30)
        size = size_font.render(str(size_string), True, red)
        size_size = size_font.size(size_string)
        screen.blit(size, ((middle_x + 192.5 - (size_size[0]/2)), 197.5))

    for button in settings_options:
        if button.rect_outer.collidepoint(pygame.mouse.get_pos()):
            button.selected = True
        else:
            button.selected = False
        button.find_image()
        button.draw()

    pygame.display.update()
    button_selection()

def account_create():

    global show_password
    global username
    global password
    global confirm_password
    global temp_password
    global temp_confirm_password
    global account_create_count
    global type_section
    global shift_count
    global error_string
    global frame_count
    global cursor_count
    global cursor_status

    if account_create_count == 0:
        username = ""
        password = ""
        confirm_password = ""
        temp_password = ""
        temp_confirm_password = ""
        account_create_count += 1

    check_fullscreen()

    heading_box_outer = pygame.Rect((middle_x - 235), 25, 470, 100)
    pygame.draw.rect(screen, red, heading_box_outer)
    
    heading_box_inner = pygame.Rect((middle_x - 225), 35, 450, 80)
    pygame.draw.rect(screen, white, heading_box_inner)

    info_box_outer = pygame.Rect((middle_x - 375), 150, 750, 325)
    pygame.draw.rect(screen, red, info_box_outer)

    info_box_inner = pygame.Rect((middle_x - 365), 160, 730, 305)
    pygame.draw.rect(screen, white, info_box_inner)

    heading_string = "Account Creation"
    heading_font = pygame.font.SysFont(None, 75)
    heading = heading_font.render(str(heading_string), True, red)
    heading_size = heading_font.size(heading_string)
    screen.blit(heading, ((400 - (heading_size[0]/2)), 48))

    username_string_string = "Username:"
    username_string_font = pygame.font.SysFont(None, 35)
    username_string = username_string_font.render(str(username_string_string), True, red)
    username_string_size = username_string_font.size(username_string_string)
    screen.blit(username_string, ((middle_x - 300), 195))

    password_string_string = "Password:"
    password_string_font = pygame.font.SysFont(None, 35)
    password_string = password_string_font.render(str(password_string_string), True, red)
    password_string_size = password_string_font.size(password_string_string)
    screen.blit(password_string, ((middle_x - 300), 263))

    confirm_string_string = "Confirm Password:"
    confirm_string_font = pygame.font.SysFont(None, 35)
    confirm_string = confirm_string_font.render(str(confirm_string_string), True, red)
    confirm_string_size = confirm_string_font.size(confirm_string_string)
    screen.blit(confirm_string, ((middle_x - 300), 331))

    show_string = "Hide Password:"
    show_font = pygame.font.SysFont(None, 35)
    show = show_font.render(str(show_string), True, red)
    show_size = show_font.size(show_string)
    screen.blit(show, ((middle_x - 300), 399))

    if error_string == 1:
        pass
    elif error_string == 2:
        error_string_string = "Passwords do not match."
        error_string_font = pygame.font.SysFont(None, 25)
        error_string_1 = error_string_font.render(str(error_string_string), True, red)
        error_string_size = error_string_font.size(error_string_string)
        screen.blit(error_string_1, ((middle_x - (error_string_size[0]/2)), 486))
    elif error_string == 3:
        error_string_string = "That username already exists."
        error_string_font = pygame.font.SysFont(None, 25)
        error_string_1 = error_string_font.render(str(error_string_string), True, red)
        error_string_size = error_string_font.size(error_string_string)
        screen.blit(error_string_1, ((middle_x - (error_string_size[0]/2)), 486))

    for button in account_create_options:
        if button.rect_outer.collidepoint(pygame.mouse.get_pos()):
            button.selected = True
        else:
            button.selected = False
        button.draw()

    if show_password == False:
        check_string = "X"
        check_font = pygame.font.SysFont(None, 39)
        check = check_font.render(str(check_string), True, white)
        check_size = check_font.size(check_string)
        screen.blit(check, ((middle_x + 154), 400))
    elif show_password == True:
        check_string = "X"
        check_font = pygame.font.SysFont(None, 39)
        check = check_font.render(str(check_string), True, red)
        check_size = check_font.size(check_string)
        screen.blit(check, ((middle_x + 104), 400))

    username_text_string = username
    username_text_font = pygame.font.SysFont(None, 35)
    username_text = username_text_font.render(str(username_text_string), True, red)
    username_text_size = username_text_font.size(username_text_string)
    screen.blit(username_text, ((middle_x + 100), 195))

    if show_password == False:
        password_text_string = password
    elif show_password == True:
        password_text_string = temp_password
    password_text_font = pygame.font.SysFont(None, 35)
    password_text = password_text_font.render(str(password_text_string), True, red)
    password_text_size = password_text_font.size(password_text_string)
    screen.blit(password_text, ((middle_x + 100), 263))

    if show_password == False:
        confirm_text_string = confirm_password
    elif show_password == True:
        confirm_text_string = temp_confirm_password
    confirm_text_font = pygame.font.SysFont(None, 35)
    confirm_text = confirm_text_font.render(str(confirm_text_string), True, red)
    confirm_text_size = confirm_text_font.size(confirm_text_string)
    screen.blit(confirm_text, ((middle_x + 100), 331))

    if cursor_count == 15:
        if cursor_status == True:
            cursor_status = False
        elif cursor_status == False:
            cursor_status = True
        cursor_count = 0
    else:
        cursor_count += 1

    if cursor_status == True:
        if type_section == 1:
            cursor = pygame.Rect((username_text_size[0] + middle_x + 103), 195, 1, 25)
            pygame.draw.rect(screen, red, cursor)
        elif type_section == 2:
            cursor = pygame.Rect((password_text_size[0] + middle_x + 103), 263, 1, 25)
            pygame.draw.rect(screen, red, cursor)
        elif type_section == 3:
            cursor = pygame.Rect((confirm_text_size[0] + middle_x + 103), 331, 1, 25)
            pygame.draw.rect(screen, red, cursor)
        
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if type_section == 1:
                    username = username[:-1]
                elif type_section == 2:
                    password = password[:-1]
                    temp_password = temp_password[:-1]
                elif type_section == 3:
                    confirm_password = confirm_password[:-1]
                    temp_confirm_password = temp_confirm_password[:-1]
            elif event.key in [pygame.K_RETURN, pygame.K_TAB]:
                if type_section != 3:
                    type_section += 1
                else:
                    type_section = 1
            else:
                if type_section == 1:
                    username += event.unicode
                elif type_section == 2:
                    password += event.unicode
                    temp_password += "*"
                elif type_section == 3:
                    confirm_password += event.unicode
                    temp_confirm_password += "*"
            username = username[:10]
            password = password[:10]
            confirm_password = confirm_password[:10]
            temp_password = temp_password[:10]
            temp_confirm_password = temp_confirm_password[:10]
        if event.type == pygame.QUIT:
            exit()
            pygame.quit()
        if (event.type is pygame.KEYDOWN and event.key == pygame.K_BACKQUOTE):
            if screen.get_flags() & pygame.FULLSCREEN:
                pygame.display.set_mode((800, 600))
            else:
                pygame.display.set_mode((800, 600), pygame.FULLSCREEN)

    pygame.display.update()
    button_selection()


def game_over_screen():

    global second_count
    global minute_count
    global points
    global x
    global maze_size_count
    global score_update_count
    global coins
    global coins_earned

    check_fullscreen()

    heading_box_outer = pygame.Rect((middle_x - 240), 50, 480, 100)
    pygame.draw.rect(screen, red, heading_box_outer)

    heading_box_inner = pygame.Rect((middle_x - 235), 55, 470, 90)
    pygame.draw.rect(screen, white, heading_box_inner)
    
    hs_box_outer = pygame.Rect((middle_x + 25), (middle_y - 100), 250, 350)
    pygame.draw.rect(screen, red, hs_box_outer)

    hs_box_inner = pygame.Rect((middle_x + 30), (middle_y - 95), 240, 340)
    pygame.draw.rect(screen, white, hs_box_inner)

    gs_box_outer = pygame.Rect((middle_x - 275), (middle_y - 100), 250, 350)
    pygame.draw.rect(screen, red, gs_box_outer)

    gs_box_inner = pygame.Rect((middle_x - 270), (middle_y - 95), 240, 340)
    pygame.draw.rect(screen, white, gs_box_inner)

    heading_string = "Game Over"
    heading_font = pygame.font.SysFont(None, 65)
    heading = heading_font.render(str(heading_string), True, red)
    heading_size = heading_font.size(heading_string)
    screen.blit(heading, ((middle_x - heading_size[0]/2), (middle_y - 225)))

    game_info_string = "Game Info"
    game_info_font = pygame.font.SysFont(None, 35)
    game_info = game_info_font.render(str(game_info_string), True, red)
    game_info_size = game_info_font.size(game_info_string)
    screen.blit(game_info, ((middle_x - 150 - (game_info_size[0]/2)), (middle_y - 60)))

    if len(str(minute_count)) == 1:
        temp_minute_count = "0" + str(minute_count)
    elif len(str(minute_count)) == 2:
        temp_minute_count = str(minute_count)
        
    if len(str(second_count)) == 1:
        temp_second_count = "0" + str(second_count)
    elif len(str(second_count)) == 2:
        temp_second_count = str(second_count)

    game_time_string = "Time: " + str(temp_minute_count) + ":" + str(temp_second_count) + " Mins"
    game_time_font = pygame.font.SysFont(None, 30)
    game_time = game_time_font.render(str(game_time_string), True, red)
    game_time_size = game_time_font.size(game_time_string)
    screen.blit(game_time, ((middle_x - 150 - (game_time_size[0]/2)), (middle_y + 70)))

    while x == 1:
        
        if maze_size_count == 1:
            point_edit = 2
        elif maze_size_count == 2:
            point_edit = 4
        elif maze_size_count == 3:
            point_edit = 6
            
        seconds_passed = second_count + minute_count*60
        points_taken = seconds_passed/point_edit
        points -= points_taken
        points = round(points)

        if points < 0:
            points = 0

        if maze_size_count == 1:
            coins_earned = round(points/10)
        elif maze_size_count == 2:
            coins_earned = round(points/5)
        elif maze_size_count == 3:
            coins_earned = round(points/2)
        coins += coins_earned
        
        x = 2

    for i in high_scores:
        if len(str(high_scores[i])) == 1:
            high_scores[i] = ("00" + str(high_scores[i]))
        elif len(str(high_scores[i])) == 2:
            high_scores[i] = ("0" + str(high_scores[i]))
        elif len(str(high_scores[i])) == 3:
            high_scores[i] = str(high_scores[i])

    if maze_size_count == 1:
        if (points > int(high_scores["small_1"])) and (score_update_count == 0):
            high_scores["small_3"] = high_scores["small_2"]
            high_scores["small_2"] = high_scores["small_1"]
            high_scores["small_1"] = str(points)
            
            score_update_count += 1
        else:
            if (points > int(high_scores["small_2"])) and (score_update_count == 0):
                high_scores["small_3"] = high_scores["small_2"]
                high_scores["small_2"] = str(points)
                score_update_count += 1
            else:
                if (points > int(high_scores["small_3"])) and (score_update_count == 0):
                    high_scores["small_3"] = str(points)
                    score_update_count += 1
    elif maze_size_count == 2:
        if (points > int(high_scores["medium_1"])) and (score_update_count == 0):
            high_scores["medium_3"] = high_scores["medium_2"]
            high_scores["medium_2"] = high_scores["medium_1"]
            high_scores["medium_1"] = str(points)
            score_update_count += 1
        else:
            if (points > int(high_scores["medium_2"])) and (score_update_count == 0):
                high_scores["medium_3"] = high_scores["medium_2"]
                high_scores["medium_2"] = str(points)
                score_update_count += 1
            else:
                if (points > int(high_scores["medium_3"])) and (score_update_count == 0):
                    high_scores["medium_3"] = str(points)
                    score_update_count += 1
    elif maze_size_count == 3:
        if (points > int(high_scores["large_1"])) and (score_update_count == 0):
            high_scores["large_3"] = high_scores["large_2"]
            high_scores["large_2"] = high_scores["large_1"]
            high_scores["large_1"] = str(points)
            score_update_count += 1
        else:
            if (points > int(high_scores["large_2"])) and (score_update_count == 0):
                high_scores["large_3"] = high_scores["large_2"]
                high_scores["large_2"] = str(points)
                score_update_count += 1
            else:
                if (points > int(high_scores["large_3"])) and (score_update_count == 0):
                    high_scores["large_3"] = str(points)
                    score_update_count += 1

    if maze_size_count == 1:
        hs_1_string = "1: " + high_scores["small_1"] + " Points"
        hs_2_string = "2: " + high_scores["small_2"] + " Points"
        hs_3_string = "3: " + high_scores["small_3"] + " Points"
    elif maze_size_count == 2:
        hs_1_string = "1: " + high_scores["medium_1"] + " Points"
        hs_2_string = "2: " + high_scores["medium_2"] + " Points"
        hs_3_string = "3: " + high_scores["medium_3"] + " Points"
    elif maze_size_count == 3:
        hs_1_string = "1: " + high_scores["large_1"] + " Points"
        hs_2_string = "2: " + high_scores["large_2"] + " Points"
        hs_3_string = "3: " + high_scores["large_3"] + " Points"

    if len(str(points)) == 1:
        temp_points = ("00" + str(points))
    elif len(str(points)) == 2:
        temp_points = ("0" + str(points))
    elif len(str(points)) == 3:
        temp_points = str(points)

    game_score_string = "Score: " + temp_points + " Points"
    game_score_font = pygame.font.SysFont(None, 30)
    game_score = game_score_font.render(str(game_score_string), True, red)
    game_score_size = game_score_font.size(game_score_string)
    screen.blit(game_score, ((middle_x - 150 - (game_score_size[0]/2)), (middle_y)))

    game_coins_string = "Coins Earned: " + str(coins_earned)
    game_coins_font = pygame.font.SysFont(None, 30)
    game_coins = game_coins_font.render(str(game_coins_string), True, red)
    game_coins_size = game_coins_font.size(game_coins_string)
    screen.blit(game_coins, ((middle_x - 150 - (game_coins_size[0]/2)), (middle_y + 140)))

    coins_total_string = "Coins Total: " + str(coins)
    coins_total_font = pygame.font.SysFont(None, 30)
    coins_total = coins_total_font.render(str(coins_total_string), True, red)
    coins_total_size = coins_total_font.size(coins_total_string)
    screen.blit(coins_total, ((middle_x - 150 - (coins_total_size[0]/2)), (middle_y + 210)))

    game_info_string = "High Scores"
    game_info_font = pygame.font.SysFont(None, 35)
    game_info = game_info_font.render(str(game_info_string), True, red)
    game_info_size = game_info_font.size(game_info_string)
    screen.blit(game_info, ((middle_x + 150 - (game_info_size[0]/2)), (middle_y - 60)))

    hs_1_font = pygame.font.SysFont(None, 30)
    hs_1 = hs_1_font.render(str(hs_1_string), True, red)
    hs_1_size = hs_1_font.size(hs_1_string)
    screen.blit(hs_1, ((middle_x + 150 - (hs_1_size[0]/2)), (middle_y)))

    hs_2_font = pygame.font.SysFont(None, 30)
    hs_2 = hs_2_font.render(str(hs_2_string), True, red)
    hs_2_size = hs_2_font.size(hs_2_string)
    screen.blit(hs_2, ((middle_x + 150 - (hs_2_size[0]/2)), (middle_y + 70)))

    hs_3_font = pygame.font.SysFont(None, 30)
    hs_3 = hs_3_font.render(str(hs_3_string), True, red)
    hs_3_size = hs_3_font.size(hs_3_string)
    screen.blit(hs_3, ((middle_x + 150 - (hs_1_size[0]/2)), (middle_y + 140)))

    for button in game_over_options:
        if button.rect_outer.collidepoint(pygame.mouse.get_pos()):
            button.selected = True
        else:
            button.selected = False
        button.draw()

    pygame.display.update()
    button_selection()


def load_game_screen():

    global show_password
    global username
    global password
    global temp_password
    global type_section
    global error_string
    global load_game_count

    if load_game_count == 0:
        username = ""
        password = ""
        temp_password = ""
        load_game_count += 1
    
    check_fullscreen()

    heading_box_outer = pygame.Rect((middle_x - 235), 25, 470, 100)
    pygame.draw.rect(screen, red, heading_box_outer)
    
    heading_box_inner = pygame.Rect((middle_x - 225), 35, 450, 80)
    pygame.draw.rect(screen, white, heading_box_inner)

    info_box_outer = pygame.Rect((middle_x - 375), 150, 750, 325)
    pygame.draw.rect(screen, red, info_box_outer)

    info_box_inner = pygame.Rect((middle_x - 365), 160, 730, 305)
    pygame.draw.rect(screen, white, info_box_inner)

    heading_string = "Load Game"
    heading_font = pygame.font.SysFont(None, 75)
    heading = heading_font.render(str(heading_string), True, red)
    heading_size = heading_font.size(heading_string)
    screen.blit(heading, ((400 - (heading_size[0]/2)), 48))

    username_string_string = "Username:"
    username_string_font = pygame.font.SysFont(None, 35)
    username_string = username_string_font.render(str(username_string_string), True, red)
    username_string_size = username_string_font.size(username_string_string)
    screen.blit(username_string, ((middle_x - 300), 195))

    password_string_string = "Password:"
    password_string_font = pygame.font.SysFont(None, 35)
    password_string = password_string_font.render(str(password_string_string), True, red)
    password_string_size = password_string_font.size(password_string_string)
    screen.blit(password_string, ((middle_x - 300), 297))

    show_string = "Hide Password:"
    show_font = pygame.font.SysFont(None, 35)
    show = show_font.render(str(show_string), True, red)
    show_size = show_font.size(show_string)
    screen.blit(show, ((middle_x - 300), 399))

    if error_string == 1:
        pass
    elif error_string == 2:
        error_string_string = "Username and/or Password is incorrect."
        error_string_font = pygame.font.SysFont(None, 25)
        error_string_1 = error_string_font.render(str(error_string_string), True, red)
        error_string_size = error_string_font.size(error_string_string)
        screen.blit(error_string_1, ((middle_x - (error_string_size[0]/2)), 486))

    for button in load_game_options:
        if button.rect_outer.collidepoint(pygame.mouse.get_pos()):
            button.selected = True
        else:
            button.selected = False
        button.draw()

    if show_password == False:
        check_string = "X"
        check_font = pygame.font.SysFont(None, 39)
        check = check_font.render(str(check_string), True, white)
        check_size = check_font.size(check_string)
        screen.blit(check, ((middle_x + 154), 400))
    elif show_password == True:
        check_string = "X"
        check_font = pygame.font.SysFont(None, 39)
        check = check_font.render(str(check_string), True, red)
        check_size = check_font.size(check_string)
        screen.blit(check, ((middle_x + 104), 400))

    username_text_string = username
    username_text_font = pygame.font.SysFont(None, 35)
    username_text = username_text_font.render(str(username_text_string), True, red)
    username_text_size = username_text_font.size(username_text_string)
    screen.blit(username_text, ((middle_x + 100), 195))

    if show_password == False:
        password_text_string = password
    elif show_password == True:
        password_text_string = temp_password
    password_text_font = pygame.font.SysFont(None, 35)
    password_text = password_text_font.render(str(password_text_string), True, red)
    password_text_size = password_text_font.size(password_text_string)
    screen.blit(password_text, ((middle_x + 100), 297))

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if type_section == 1:
                    username = username[:-1]
                elif type_section == 2:
                    password = password[:-1]
                    temp_password = temp_password[:-1]
            elif event.key in [pygame.K_RETURN, pygame.K_TAB]:
                if type_section != 2:
                    type_section += 1
                else:
                    type_section = 1
            else:
                if type_section == 1:
                    username += event.unicode
                elif type_section == 2:
                    password += event.unicode
                    temp_password += "*"
            username = username[:10]
            password = password[:10]
            temp_password = temp_password[:10]
        if event.type == pygame.QUIT:
            exit()
            pygame.quit()
        if (event.type is pygame.KEYDOWN and event.key == pygame.K_BACKQUOTE):
            if screen.get_flags() & pygame.FULLSCREEN:
                pygame.display.set_mode((800, 600))
            else:
                pygame.display.set_mode((800, 600), pygame.FULLSCREEN)

    pygame.display.update()
    button_selection()


def shop_screen():

    check_fullscreen()

    heading_box_outer = pygame.Rect((middle_x - 235), 25, 470, 100)
    pygame.draw.rect(screen, red, heading_box_outer)
    
    heading_box_inner = pygame.Rect((middle_x - 225), 35, 450, 80)
    pygame.draw.rect(screen, white, heading_box_inner)

    sprite_box_outer = pygame.Rect((middle_x - 100), (middle_y - 100), 200, 200)
    pygame.draw.rect(screen, red, sprite_box_outer)

    sprite_box_inner = pygame.Rect((middle_x - 95), (middle_y - 95), 190, 190)
    pygame.draw.rect(screen, white, sprite_box_inner)

    player_coin_box_outer = pygame.Rect((middle_x - 150), 140, 300, 45)
    pygame.draw.rect(screen, red, player_coin_box_outer)

    player_coin_box_inner = pygame.Rect((middle_x - 145), 145, 290, 35)
    pygame.draw.rect(screen, white, player_coin_box_inner)

    sprite_cost_box_outer = pygame.Rect((middle_x - 150), (middle_y + 115), 300, 45)
    pygame.draw.rect(screen, red, sprite_cost_box_outer)

    sprite_cost_box_inner = pygame.Rect((middle_x - 145), (middle_y + 120), 290, 35)
    pygame.draw.rect(screen, white, sprite_cost_box_inner)

    heading_string = "Shop"
    heading_font = pygame.font.SysFont(None, 75)
    heading = heading_font.render(str(heading_string), True, red)
    heading_size = heading_font.size(heading_string)
    screen.blit(heading, ((400 - (heading_size[0]/2)), 48))

    player_coin_string = "Coins: " + str(coins)
    player_coin_font = pygame.font.SysFont(None, 35)
    player_coin = player_coin_font.render(str(player_coin_string), True, red)
    player_coin_size = player_coin_font.size(player_coin_string)
    screen.blit(player_coin, ((middle_x - (player_coin_size[0]/2)), 150))

    if sprite_status[sprite_selected] == True:
        sprite_cost_string = "Purchased"
    elif sprite_status[sprite_selected] == False:
        sprite_cost_string = "Cost: " + str(sprite_costs[sprite_selected])

    sprite_cost_font = pygame.font.SysFont(None, 35)
    sprite_cost = sprite_cost_font.render(str(sprite_cost_string), True, red)
    sprite_cost_size = sprite_cost_font.size(sprite_cost_string)
    screen.blit(sprite_cost, ((middle_x - (sprite_cost_size[0]/2)), (middle_y + 125)))

    if error_string == 1:
        error_string_string = "You don't have enough coins."
        error_string_font = pygame.font.SysFont(None, 25)
        error_string_1 = error_string_font.render(str(error_string_string), True, red)
        error_string_size = error_string_font.size(error_string_string)
        screen.blit(error_string_1, ((middle_x - (error_string_size[0]/2)), 470))
    elif error_string == 2:
        error_string_string = "You already own this."
        error_string_font = pygame.font.SysFont(None, 25)
        error_string_1 = error_string_font.render(str(error_string_string), True, red)
        error_string_size = error_string_font.size(error_string_string)
        screen.blit(error_string_1, ((middle_x - (error_string_size[0]/2)), 470))
        
    if sprite_status[sprite_selected] == True:
        display_image = pygame.image.load(imgpath[("shop_" + str(sprite_selected))][0])
    elif sprite_status[sprite_selected] == False:
        display_image = pygame.image.load(imgpath[("shop_" + str(sprite_selected))][1])

    display_image = pygame.transform.scale(display_image, (100, 100))
    screen.blit(display_image, (350, 250))


    for button in shop_screen_options:
        if button.rect_outer.collidepoint(pygame.mouse.get_pos()):
            button.selected = True
        else:
            button.selected = False
        button.find_image()
        button.draw()

    pygame.display.update()
    button_selection()


def ins_screen():

    check_fullscreen()

    heading_box_outer = pygame.Rect((middle_x - 235), 25, 470, 100)
    pygame.draw.rect(screen, red, heading_box_outer)
    
    heading_box_inner = pygame.Rect((middle_x - 225), 35, 450, 80)
    pygame.draw.rect(screen, white, heading_box_inner)

    info_box_outer = pygame.Rect((middle_x - 375), 150, 750, 425)
    pygame.draw.rect(screen, red, info_box_outer)

    info_box_inner = pygame.Rect((middle_x - 365), 160, 730, 405)
    pygame.draw.rect(screen, white, info_box_inner)

    heading_string = "Instructions"
    heading_font = pygame.font.SysFont(None, 75)
    heading = heading_font.render(str(heading_string), True, red)
    heading_size = heading_font.size(heading_string)
    screen.blit(heading, ((400 - (heading_size[0]/2)), 48))

    text_string = "Typing"
    text_font = pygame.font.SysFont(None, 35)
    text = text_font.render(str(text_string), True, red)
    text_size = text_font.size(text_string)
    screen.blit(text, ((middle_x - 350), 175))

    text_string = "~   Enter text using keyboard."
    text_font = pygame.font.SysFont(None, 25)
    text = text_font.render(str(text_string), True, red)
    text_size = text_font.size(text_string)
    screen.blit(text, ((middle_x - 330), 215))

    text_string = "~   Change the typing area using the TAB or ENTER keys."
    text_font = pygame.font.SysFont(None, 25)
    text = text_font.render(str(text_string), True, red)
    text_size = text_font.size(text_string)
    screen.blit(text, ((middle_x - 330), 235))

    text_string = "~   Delete entered text using the BACKSPACE key."
    text_font = pygame.font.SysFont(None, 25)
    text = text_font.render(str(text_string), True, red)
    text_size = text_font.size(text_string)
    screen.blit(text, ((middle_x - 330), 255))

    text_string = "Navigation"
    text_font = pygame.font.SysFont(None, 35)
    text = text_font.render(str(text_string), True, red)
    text_size = text_font.size(text_string)
    screen.blit(text, ((middle_x - 350), 305))

    text_string = "~   To navigate about the game, click relevant buttons with the left mouse button."
    text_font = pygame.font.SysFont(None, 25)
    text = text_font.render(str(text_string), True, red)
    text_size = text_font.size(text_string)
    screen.blit(text, ((middle_x - 330), 345))

    text_string = "Gameplay"
    text_font = pygame.font.SysFont(None, 35)
    text = text_font.render(str(text_string), True, red)
    text_size = text_font.size(text_string)
    screen.blit(text, ((middle_x - 350), 395))

    text_string = "~   Move throughout the maze using the arrow keys."
    text_font = pygame.font.SysFont(None, 25)
    text = text_font.render(str(text_string), True, red)
    text_size = text_font.size(text_string)
    screen.blit(text, ((middle_x - 330), 435))

    text_string = "~   Move to the green square to complete the maze."
    text_font = pygame.font.SysFont(None, 25)
    text = text_font.render(str(text_string), True, red)
    text_size = text_font.size(text_string)
    screen.blit(text, ((middle_x - 330), 455))

    text_string = "~   Change the maze difficulty in the settings menu."
    text_font = pygame.font.SysFont(None, 25)
    text = text_font.render(str(text_string), True, red)
    text_size = text_font.size(text_string)
    screen.blit(text, ((middle_x - 330), 475))

    for button in ins_screen_options:
        if button.rect_outer.collidepoint(pygame.mouse.get_pos()):
            button.selected = True
        else:
            button.selected = False
        button.find_image()
        button.draw()

    pygame.display.update()
    button_selection()


while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            exit()
            pygame.quit()

        if (event.type is pygame.KEYDOWN and event.key == pygame.K_BACKQUOTE):

            if screen.get_flags() & pygame.FULLSCREEN:
                pygame.display.set_mode((800, 600))

            else:
                pygame.display.set_mode((800, 600), pygame.FULLSCREEN)

    if mode == 0:
        start_menu()
    elif mode == 1:
        home_screen()
    elif mode == 2:
        load_game_screen()
    elif mode == 3:
        ins_screen()
    elif mode == 4:
        maze_screen()
    elif mode == 5:
        shop_screen()
    elif mode == 7:
        settings_screen()
    elif mode == 8:
        account_create()
    elif mode == 9:
        game_over_screen()



