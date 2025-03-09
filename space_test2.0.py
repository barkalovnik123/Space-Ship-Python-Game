import pygame
import math
import configparser
from random import randint, choice
from tkinter.messagebox import showinfo
import tkinter.simpledialog as dialog

#CONSTS
WIDTH = 640
HEIGHT = 480
FPS = 60
CAPTION = "Space"

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(CAPTION)
clock = pygame.time.Clock()

icon = pygame.image.load('star.png')
pygame.display.set_icon(icon)

pygame.mixer.music.load('bg_mus.mp3')
pygame.mixer.music.play()

config = configparser.ConfigParser()
config.read('highscore.ini')
hs_file = config['highscore']

HIGHSCORE = hs_file['hs']
HS_NAME = hs_file['name']
HP = 100
SCORE = 0

def change_score():
    global SCORE, HIGHSCORE
    if SCORE > float(HIGHSCORE):
        new_name = dialog.askstring(CAPTION, "Ваше имя: ")
        config = configparser.ConfigParser()
        config['highscore'] = {'hs' : str(SCORE), 'name' : new_name}
        with open('highscore.ini', 'w') as configfile:
            config.write(configfile)
""""""
def does_collide(my_x, my_y, my_width, my_height, enemy_x, enemy_y, enemy_width, enemy_height): #проверка на столкновение с кораблём. Требуется улучшение.
    #в pygame есть готовый способ проверять столкновения, но переписывать под него проект уже поздно
    dots_to_check_x = list(range(my_x, my_width+1))
    dots_to_check_y = list(range(my_y, my_height+1))

    is_colliding_by_x = False
    is_colliding_by_y = False
    for dot_x in dots_to_check_x:
        is_collide = dot_x < enemy_width and dot_x > enemy_x
        is_colliding_by_x = is_colliding_by_x or is_collide
    for dot_y in dots_to_check_y:
        is_collide = dot_y < enemy_height and dot_y > enemy_y
        is_colliding_by_y = is_colliding_by_y or is_collide
    
    return is_colliding_by_x and is_colliding_by_y
    '''
    тут все точки складываются в массивы и перебираются
    '''

class Asteroid(): #астероиды
    def __init__(self):
        self.y = 0-256
        self.x = randint(0, WIDTH+2)
        self.x_speed = randint(-5, 5)
        self.y_speed = randint(1, 13)
        self.rotate_angle = choice((0, 180))
    def animate(self):
        global HP
        self.x += self.x_speed
        self.y += self.y_speed
        
        asteroid_img = pygame.image.load("asteroid_0.png")
        asteroid_img = asteroid_img.convert()
        asteroid_img.set_colorkey((0, 0, 0))
        scale_i = 2
        #print(player.scale_i) - хорошие новости, объект может получать свойства другого по названию. Интерпритация (?)
        #print(player.image_for_asteroid.get_width()) - ещё более хорошая новость!
        asteroid_img = pygame.transform.rotate(asteroid_img, self.rotate_angle)
        asteroid_img = pygame.transform.scale(asteroid_img, (asteroid_img.get_width()//scale_i, asteroid_img.get_height()//scale_i))
        asteroid_img = {'image': asteroid_img,
                    'x_start': self.x,
                    'y_start': self.y}
        screen.blit(asteroid_img['image'], [asteroid_img['x_start'], asteroid_img['y_start']])

        hit_box = 20
        if does_collide(self.x+hit_box, self.y+hit_box, self.x+asteroid_img['image'].get_width()-hit_box, self.y+asteroid_img['image'].get_height()-hit_box, \
              player.x, player.y, player.x+player.image_for_asteroid.get_width(), player.y+player.image_for_asteroid.get_height()):
            HP -= 5 #уменьшить жизни
        

class Player(): #игрок - корабль
    def __init__(self): 
        self.y = HEIGHT - 64 #нач. позиции
        self.x = WIDTH / 2
    def controls(self): #управление
        self.speed = 15
        mouse_x = pygame.mouse.get_pos()
        mouse_x = mouse_x[0]
        if mouse_x < WIDTH:
            self.x = mouse_x - (self.image_for_asteroid.get_width()//2)
    def animate(self):
        player_img = pygame.image.load('playerstar.png')
        player_img = player_img.convert()
        player_img.set_colorkey((0, 0, 0))
        self.scale_i = 10
        player_img = pygame.transform.scale(player_img, (player_img.get_width()//self.scale_i, player_img.get_height()//self.scale_i))
        player_img = {'image': player_img,
                    'x_start': self.x,
                    'y_start': self.y}
        screen.blit(player_img['image'], [player_img['x_start'], player_img['y_start']])
        self.image_for_asteroid = player_img['image']

class Star():
    def __init__(self):
        self.x = randint(0, WIDTH)
        self.y = -128
        max_speed = 5
        self.speed = randint(1, max_speed)
    def animate(self):   
        self.y += self.speed

        star = pygame.image.load('star.png')
        star = star.convert()
        star.set_colorkey((0,0,0))
        scale_k = self.speed*2
        star = pygame.transform.scale(star, (scale_k, scale_k))
        screen.blit(star, [self.x, self.y])
sin_k = 0 
class UI(): #юзер-интерфейс
    def render(self):
        global sin_k, HP
        
        BGCOLOR = (30,33,61)
        screen.fill(BGCOLOR)

        BGSATURN = pygame.image.load('saturn.png')
        BGSATURN = BGSATURN.convert()
        BGSATURN.set_colorkey((0, 0, 0))
        scale_i = WIDTH / 213
        BGSATURN = pygame.transform.scale(BGSATURN, (BGSATURN.get_width()//scale_i, BGSATURN.get_height()//scale_i))
        BGSATURN = {'image': BGSATURN,
                    'x_start': WIDTH/6*2,
                    'y_start': HEIGHT/4}
        sin_k += 0.037 #сатурн плавно качается, тут скорость
        screen.blit(BGSATURN['image'], [BGSATURN['x_start'], BGSATURN['y_start']+(math.sin(sin_k)*6)])

    def controls(self):
        global HP, SCORE, FPS
        def end_game():
            running = False
            pygame.quit()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_game()
        
        if HP <= 0:
            
            showinfo(CAPTION, "Игра окончена!")

            change_score()
            
            end_game()
        
        SCORE += 1/FPS
        pygame.display.set_caption(CAPTION+' | Здоровье: '+str(HP)+" | Очки: "+str(int(SCORE))+' с | Высший рекорд: '+HS_NAME+" с "+str(int(float(HIGHSCORE)))+' с')
        

#настройки звёздочек
star_creating_limiter_timer = 2 #как часто появляются звездчоки. Измеряется в Попугаях, потому что помоту.
max_star_amount = int(WIDTH / 106) #как много звёздочек. Считается автоматически и кратно шести по стандарту.
stars = [] #тут мы храним экземпляры звёзд чтобы иметь возможность их удалять и не нагружать цпу
star_creating_timer = star_creating_limiter_timer #таймер их создания. Так они будут создаваться каждый раз когда таймер достигает в размере лимитёра

ui = UI()
player = Player()

#астероиды. принцип создания тот же что у звёздочек
asteroid_creating_limiter_timer = 2
max_asteroid_amount = int(WIDTH / 53)
asteroid_lst = []
asteroid_creating_timer = asteroid_creating_limiter_timer
running = True
while running:
    #до step
    ui.controls() #вызов меню, закрытие программки и т.д.

    #step
    
    
    #post-step рендер
    
    ui.render()
    player.animate()
    player.controls()
    
    '''
    они работают на совершенно одинаковом принципе таймеров, но если обернуть их в функцию появляется проблема: создаваемые внутри функции объекты почему-то
    перестают вести себя уникально: все локальные переменные определяются одинаково. Возможно стоило попробовать обернуть их в класс. Или
    просто обновлять сид для рандома. Но пока так...
    '''
    asteroid_creating_timer += 0.1
    if asteroid_creating_timer - asteroid_creating_limiter_timer >= 0:
        for i in range(randint(0, max_asteroid_amount)):
            some_aster = Asteroid()
            asteroid_lst.append(some_aster)
        asteroid_creating_timer = 0
    for the_aster in asteroid_lst:
        if the_aster.y > HEIGHT + 128:
            asteroid_lst.remove(the_aster)
        else:
            the_aster.animate()

    
    star_creating_timer += 0.05
    if star_creating_timer - star_creating_limiter_timer >= 0:
        for i in range(randint(0, max_star_amount)):
            some_star = Star()
            stars.append(some_star)
        star_creating_timer = 0
    for the_star in stars:
        if the_star.y > HEIGHT + 64:
            stars.remove(the_star)
        else:
            the_star.animate()
    pygame.display.update()
    '''странное дело: все работает как надо только если расположить их в таком порядке... Какая разница
        в корне не ясно, но пока работает трогать не буду XD'''
    

pygame.quit()
