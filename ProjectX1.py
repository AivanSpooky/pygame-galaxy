import pygame
import random
import pyganim
import sys
import os
pygame.init()
screen = pygame.display.set_mode((500, 600))
fon = pygame.transform.scale(pygame.image.load('data\\night-stars-png.png').convert_alpha(), [3000, 3000])
dollars = pygame.transform.scale(pygame.image.load('data\\dollars.png').convert_alpha(), [3000, 3000])
ship_play = pygame.transform.scale(pygame.image.load('data\\rockets_PNG13283.png').convert_alpha(), [50, 90])
vns_play = pygame.transform.scale(pygame.image.load('data\\VNS.png').convert_alpha(), [50, 90])
ship_play_shut = pygame.transform.scale(pygame.image.load('data\\OurRocketShut.png').convert_alpha(), [50, 90])
levelup = pygame.transform.scale(pygame.image.load('data\\LevelUp.png').convert_alpha(), [300, 300])
gameover = pygame.transform.scale(pygame.image.load('data\\GAMEOVER.png').convert_alpha(), [300, 300])
gamewin = pygame.transform.scale(pygame.image.load('data\\Victory.png').convert_alpha(), [300, 300])
rocket1 = pygame.transform.scale(pygame.image.load('data\\Rocket1.png').convert_alpha(), [150, 150])
rocket2 = pygame.transform.scale(pygame.image.load('data\\Rocket2.png').convert_alpha(), [150, 150])
rocket3 = pygame.transform.scale(pygame.image.load('data\\Rocket3.png').convert_alpha(), [150, 150])
rocket4 = pygame.transform.scale(pygame.image.load('data\\Rocket4.png').convert_alpha(), [150, 150])
rocketboss1 = pygame.transform.scale(pygame.image.load('data\\RocketBoss1.png').convert_alpha(), [300, 300])
our_laser = pygame.transform.scale(pygame.image.load('data\\Green_laser.png').convert_alpha(), [50, 50])
enemy_laser = pygame.transform.scale(pygame.image.load('data\\EnemyLaser.png').convert_alpha(), [50, 50])
nuke_laser = pygame.transform.scale(pygame.image.load('data\\s1200.png').convert_alpha(), [100, 100])
ship_start = pygame.transform.scale(pygame.image.load('data\\missile_PNG20.png').convert_alpha(), [150, 150])
background = pygame.transform.scale(pygame.image.load('data\\maxresdefault.jpg').convert_alpha(), [500, 600])
explode = pyganim.getImagesFromSpriteSheet('data\\explode.png', rows=4, cols=4, rects=[])
explode1 = pyganim.getImagesFromSpriteSheet('data\\nuke.png', rows=7, cols=2, rects=[])
our_laser = pygame.transform.rotate(our_laser, 90)
enemy_laser = pygame.transform.rotate(enemy_laser, 90)

lives = 3
points = 0
se_points = 0
extra_lives = 0
sound = pygame.mixer.Sound('data\\laser_explosion.wav')
sound1 = pygame.mixer.Sound('data\\our_laser_shot.wav')
sound2 = pygame.mixer.Sound('data\\enemy_shot.wav')
sound2.set_volume(0.2)
sound3 = pygame.mixer.Sound('data\\new_level.wav')
sound4 = pygame.mixer.Sound('data\\engine.wav')
gameovermusic = pygame.mixer.Sound('data\\game_over.wav')
gameovermusic.set_volume(0.2)
pygame.init()
pygame.mixer.init()

def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def draw_level_box(level, lives, points):
    pygame.draw.rect(screen, pygame.Color('brown'), (0, 0, 80, 90))
    font = pygame.font.Font(None, 25)
    level_number = 'level '
    level_number += str(level)
    text = font.render(level_number, 1, (100, 255, 100))
    text_x = 5
    text_y = 5
    screen.blit(text, (text_x, text_y))
    lives_number = 'lives: '
    lives_number += str(lives)
    text1 = font.render(lives_number, 1, (100, 255, 100))
    text1_x = 5
    text1_y = 35
    screen.blit(text1, (text1_x, text1_y))
    points_number = 'p: '
    points_number += str(points)
    text1 = font.render(points_number, 1, (100, 255, 100))
    text1_x = 5
    text1_y = 65
    screen.blit(text1, (text1_x, text1_y))    
    pygame.display.flip()

def lost_live():
    global lives
    lives -= 1
    ship.change_col()

class Explosion():
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.current_sprite = 0
        self.sprites = explode
    
    def update(self, screen):
        self.current_sprite = (self.current_sprite + 1) % 33
        if self.current_sprite == 32:
            explodes.remove(self)
            return
        screen.blit(self.sprites[self.current_sprite // 2], [self.x, self.y])

class Ship(pygame.sprite.Sprite):
    ship_play = pygame.transform.scale(pygame.image.load('data\\rockets_PNG13283.png').convert_alpha(), [50, 90])
    ship_play_shut = pygame.transform.scale(pygame.image.load('data\\OurRocketShut.png').convert_alpha(), [50, 90])
    
    def __init__(self, sprite, x, y):
        self.x = x
        self.y = y
        self.image = ship_play
        self.sprite = sprite
        self.invisibility = 0
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)        
        super().__init__()

    def update(self):
        if self.invisibility == 0:
            screen.blit(self.sprite, [self.x, self.y])
        else:
            self.invisibility -= 1
    
    def check_if_down(self, shipR):
        offset = (int(shipR.x - self.x), int(shipR.y - self.y))
        if ship.mask.overlap(shipR.mask, offset):
            return True
        else:
            return False
    
    def change_col(self):
        self.invisibility = 5
    
    def rotate(self, rotate_angle):
        self.sprite = pygame.transform.rotate(vns_play, rotate_angle)

class Laser(pygame.sprite.Sprite):
    def __init__(self, sprite, x, y):
        self.x = x
        self.y = y
        self.image = our_laser
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        #self.rect = pygame.Rect(self.x, self.y, our_laser.get_rect().width, our_laser.get_rect().height)
        self.sprite = sprite
        super().__init__()

    def update(self):
        screen.blit(self.sprite, [self.x, self.y])

class EnemyLaser(pygame.sprite.Sprite):
    def __init__(self, sprite, x, y):
        self.x = x
        self.y = y
        self.image = enemy_laser
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        #self.rect = pygame.Rect(self.x, self.y, our_laser.get_rect().width, our_laser.get_rect().height)
        self.sprite = sprite
        super().__init__()

    def update(self):
        offset = (int(ship.x - self.x), int(ship.y - self.y))
        if self.mask.overlap(ship.mask, offset):
            lost_live()
            self.y = 800
        else:
            self.y += 10
            screen.blit(self.sprite, [self.x, self.y])
        return self.y

class EnemyLaserTracking(pygame.sprite.Sprite):
    def __init__(self, sprite, x, y):
        self.x = x
        self.y = y
        self.image = enemy_laser
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        #self.rect = pygame.Rect(self.x, self.y, our_laser.get_rect().width, our_laser.get_rect().height)
        self.sprite = sprite
        super().__init__()

    def update(self):
        offset = (int(ship.x - self.x), int(ship.y - self.y))
        if ship.x - 30 > self.x:
            self.x += random.randint(0, 5)
        elif ship.x - 30 < self.x:
            self.x -= random.randint(0, 5)
        if self.mask.overlap(ship.mask, offset):
            lost_live()
            self.y = 800
        else:
            self.y += 10
            screen.blit(self.sprite, [self.x, self.y])
        return self.y

class Stars_fon(pygame.sprite.Sprite):
    def __init__(self, sprite, x, y, y_board, y_start):
        self.x = x
        self.y = y
        self.y_board = y_board
        self.y_start = y_start
        self.sprite = sprite
        super().__init__()

    def update(self):
        if self.y < self.y_board:
            if not gameovering and not gamewinning:
                self.y += 5
            screen.blit(self.sprite, [self.x, self.y])
        else:
            self.y = self.y_start

class Level_Up(pygame.sprite.Sprite):
    def __init__(self, sprite, x, y):
        self.x = x
        self.y = y
        self.sprite = sprite
        super().__init__()

    def update(self):
        if self.x < 800:
            self.x += 10
            screen.blit(self.sprite, [self.x, self.y])
        else:
            levelingup = False

class Game_Over(pygame.sprite.Sprite):
    def __init__(self, sprite, x, y):
        self.x = x
        self.y = y
        self.sprite = sprite
        super().__init__()

    def update(self):
        if self.x < 100:
            self.x += 3
            screen.blit(self.sprite, [self.x, self.y])
        else:
            screen.blit(self.sprite, [self.x, self.y])
            gameovering = False
            lives = -1
            runing = False

class Game_Win(pygame.sprite.Sprite):
    def __init__(self, sprite, x, y):
        self.x = x
        self.y = y
        self.sprite = sprite
        super().__init__()

    def update(self):
        if self.x < 100:
            self.x += 3
            screen.blit(self.sprite, [self.x, self.y])
        else:
            screen.blit(self.sprite, [self.x, self.y])
            gamewinning = False
            runing = False

class Rocket1(pygame.sprite.Sprite):
    def __init__(self, sprite, x, y):
        self.x = x
        self.y = y
        self.hitpoints = 1
        self.points = 1
        self.shag = random.randint(1, 5)
        self.image = rocket1
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        #self.rect = pygame.Rect(self.x, self.y, rocket1.get_rect().width, rocket1.get_rect().height)
        self.sprite = sprite
        super().__init__()

    def update(self):
        if self.y < 700:
            self.y += self.shag
            screen.blit(self.sprite, [self.x, self.y])
        else:
            self.x = random.randint(-30, 400)
            self.y = random.randint(yr11, yr12)
            pass
    
    def explode(self):
        offset = (int(self.x - laser.x), int(self.y - laser.y))
        if laser.mask.overlap(self.mask, offset):
            self.hitpoints -= 1
            return (self.hitpoints, self.points)
        return (-1, -1)

class Rocket2(pygame.sprite.Sprite):
    def __init__(self, sprite, x, y):
        self.x = x
        self.y = y
        self.hitpoints = 3
        self.points = 5
        self.enem_fired = False
        self.shag = random.randint(1, 5)
        self.image = rocket1
        self.shoot_time = 0
        self.laser = None
        self.set_shoot_time = 80
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        #self.rect = pygame.Rect(self.x, self.y, rocket1.get_rect().width, rocket1.get_rect().height)
        self.sprite = sprite
        super().__init__()

    def update(self):
        if self.y < 700:
            self.y += self.shag
            if self.y > 0:
                if ship.x - 50 > self.x:
                    self.x += random.randint(0, 2)
                elif ship.x - 50 < self.x:
                    self.x -= random.randint(0, 2)
                if abs(ship.x - 50 - self.x) < 50 and self.shoot_time <= 0 and not self.laser:
                    self.shoot_time = self.set_shoot_time
                    self.laser = EnemyLaser(enemy_laser, self.x + 50, self.y + 100)
                elif self.shoot_time > 0:
                    self.shoot_time -= 1
            if self.laser:
                sound2.play()
                pos = self.laser.update()
                if pos >= 700:
                    self.laser = None
            screen.blit(self.sprite, [self.x, self.y])
        else:
            self.x = random.randint(-30, 400)
            self.y = random.randint(yr21, yr22)
            pass
    
    def explode(self):
        offset = (int(self.x - laser.x), int(self.y - laser.y))
        if laser.mask.overlap(self.mask, offset):
            self.hitpoints -= 1
            return (self.hitpoints, self.points)
        return (-1, -1)

class Rocket3(pygame.sprite.Sprite):
    def __init__(self, sprite, x, y):
        self.x = x
        self.y = y
        self.hitpoints = 1
        self.points = 3
        self.shag = 3
        self.image = rocket3
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        #self.rect = pygame.Rect(self.x, self.y, rocket1.get_rect().width, rocket1.get_rect().height)
        self.sprite = sprite
        super().__init__()

    def update(self):
        if self.y < 700:
            if self.y > -200:
                sound4.play()
            if self.y > 0:
                self.shag = 50
            self.y += self.shag
            screen.blit(self.sprite, [self.x, self.y])
        else:
            self.x = random.randint(-30, 400)
            self.y = random.randint(yr31, yr32)
            self.shag = 3
            pass
    
    def explode(self):
        offset = (int(self.x - laser.x), int(self.y - laser.y))
        if laser.mask.overlap(self.mask, offset):
            self.hitpoints -= 1
            return (self.hitpoints, self.points)
        return (-1, -1)

class Rocket4(pygame.sprite.Sprite):
    def __init__(self, sprite, x, y):
        self.x = x
        self.y = y
        self.hitpoints = 3
        self.points = 10
        self.enem_fired = False
        self.shag = random.randint(1, 5)
        self.image = rocket1
        self.shoot_time = 0
        self.laser = None
        self.set_shoot_time = 100
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        #self.rect = pygame.Rect(self.x, self.y, rocket1.get_rect().width, rocket1.get_rect().height)
        self.sprite = sprite
        super().__init__()

    def update(self):
        if self.y < 700:
            self.y += self.shag
            if self.y > -20:
                if ship.x - 50 > self.x and not fired:
                    self.x += random.randint(0, 2)
                elif ship.x - 50 < self.x and not fired:
                    self.x -= random.randint(0, 2)
                if abs(ship.x - 50 - self.x) < 100 and self.shoot_time <= 0 and not self.laser:
                    self.shoot_time = self.set_shoot_time
                    self.laser = EnemyLaser(enemy_laser, self.x + 50, self.y + 100)
                elif self.shoot_time > 0:
                    self.shoot_time -= 1
                if fired:
                    if laser.x >= self.x + 20:
                        if self.x - 3 > -30:
                            self.x -= 3
                        else:
                            self.x += 5
                    if laser.x <= self.x + 20:
                        if self.x + 3 < 400:
                            self.x += 3
                        else:
                            self.x -= 5                        
            if self.laser:
                sound2.play()
                pos = self.laser.update()
                if pos >= 700:
                    self.laser = None
            screen.blit(self.sprite, [self.x, self.y])
        else:
            self.x = random.randint(-30, 400)
            self.y = random.randint(yr41, yr42)
            pass
    
    def explode(self):
        offset = (int(self.x - laser.x), int(self.y - laser.y))
        if laser.mask.overlap(self.mask, offset):
            self.hitpoints -= 1
            return (self.hitpoints, self.points)
        return (-1, -1)

class RocketBoss1(pygame.sprite.Sprite):
    def __init__(self, sprite, x, y):
        self.x = x
        self.y = y
        self.hitpoints = 40
        self.points = 50
        self.enem_fired = False
        self.shag = random.randint(1, 5)
        self.image = rocketboss1
        self.shoot_time = 0
        self.laser = None
        self.laser1 = None
        self.set_shoot_time = 180
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        #self.rect = pygame.Rect(self.x, self.y, rocket1.get_rect().width, rocket1.get_rect().height)
        self.sprite = sprite
        super().__init__()

    def update(self):
        if self.y < 10:
            self.y += self.shag
            screen.blit(self.sprite, [self.x, self.y])
        if self.y > 0:
            if ship.x - 120 > self.x and not fired:
                self.x += 1
            elif ship.x - 120 < self.x and not fired:
                self.x -= 1            
            if self.shoot_time <= 0 and not self.laser and not self.laser1:
                p = random.randint(1, 2)
                self.shoot_time = self.set_shoot_time
                self.laser = EnemyLaserTracking(enemy_laser, self.x + 50, self.y + 120)
                self.laser1 = EnemyLaserTracking(enemy_laser, self.x + 200, self.y + 120)
            elif self.shoot_time > 0:
                self.shoot_time -= 1
        if self.laser and self.laser1:
            sound2.play()
            pos = self.laser.update()
            pos1 = self.laser1.update()
            if pos >= 700 or pos1 >= 700:
                self.laser = None
                self.laser1 = None
        screen.blit(self.sprite, [self.x, self.y])
    
    def explode(self):
        offset = (int(self.x - laser.x), int(self.y - laser.y))
        if laser.mask.overlap(self.mask, offset):
            self.hitpoints -= 1
            if self.hitpoints == 0:
                self.hitpoints = -2
            return (self.hitpoints, self.points)
        return (-1, -1)

runing = True
loading = True
FPS = 60
level = 1
motion = 'STOP'
fired = False
rockets = []
explodes = []
danger_objects = []
rotate = 0
ship = Ship(ship_play, 150, 500)
laser = Laser(our_laser, 150, 400)
danger_objects.append(laser)
moving_fon = Stars_fon(fon, 0, -2400, 0, -2400)
moving_dollar = Stars_fon(dollars, -200, -3000, 700, -3000)
moving_level = Level_Up(levelup, -300, 150)
moving_gameover = Game_Over(gameover, -400, 150)
moving_victory = Game_Win(gamewin, -400, 150)
r1 = True
levelingup = False
gameovering = False
gamewinning = False
dollar_move = False
vns = False
clock = pygame.time.Clock()
while runing:
    while loading:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runing = False
                loading = False
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:              
                loading = False
        screen.blit(background, [0, 0])
        screen.blit(ship_start, [250, 25])
        intro_text = ["GALAXY",
                      "by Aivan", "",
                      "Rules:",
                      "1) Control your ship",
                      "2) Shoot your enemies",
                      "3) Win the game!",
                      "Warning! The game is very hard!(but possible)"]
        font = pygame.font.Font(None, 30)
        text_coord = 50
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('red'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        pygame.display.flip()
        screen.fill((0, 0, 0))
        
    pygame.display.flip()
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            runing = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                motion = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                motion = 'RIGHT'
            elif event.key == pygame.K_UP:
                if not fired and not gameovering and not gamewinning:
                    laser.x = ship.x
                    laser.y = ship.y - 20                
                    fired = True
                    sound1.play()
            elif keys[pygame.K_s] and keys[pygame.K_p] and keys[pygame.K_o] and keys[pygame.K_k] and keys[pygame.K_y]:
                pygame.mixer.music.load('data\\Space_Galaxy.mp3')
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play()
            elif keys[pygame.K_v] and keys[pygame.K_n] and keys[pygame.K_s]:
                if not vns:
                    vns = True
                    ship.sprite = vns_play
                    rotate = 0
                else:
                    vns = False
                    ship.sprite = ship_play
                    rotate = 0
                print(vns)
            elif event.key == pygame.K_4:
                if not dollar_move:
                    dollar_move = True
                else:
                    dollar_move = False
        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                motion = 'STOP'
    
    if level == 1 and r1:
        yr11 = -1000
        yr12 = -300
        for i in range(5):
            rocket_1 = Rocket1(rocket1, random.randint(-30, 400), random.randint(yr11, yr12))
            rockets.append(rocket_1)        
        r1 = False
    elif level == 2 and r1:
        yr11 = -1200
        yr12 = -300
        yr21 = -2000
        yr22 = -700
        for i in range(5):
            rocket_1 = Rocket1(rocket1, random.randint(-30, 400), random.randint(yr11, yr12))
            rockets.append(rocket_1)
        for i in range(2):
            rocket_2 = Rocket2(rocket2, random.randint(-30, 400), random.randint(yr21, yr22))
            rockets.append(rocket_2)
        r1 = False
    elif level == 3 and r1:
        yr11 = -1200
        yr12 = -300
        yr21 = -2000
        yr22 = -700
        yr31 = -2500
        yr32 = -1500
        for i in range(7):
            rocket_1 = Rocket1(rocket1, random.randint(-30, 400), random.randint(yr11, yr12))
            rockets.append(rocket_1)
        for i in range(2):
            rocket_2 = Rocket2(rocket2, random.randint(-30, 400), random.randint(yr21, yr22))
            rockets.append(rocket_2)
        for i in range(2):
            rocket_3 = Rocket3(rocket3, random.randint(-30, 400), random.randint(yr31, yr32))
            rockets.append(rocket_3)
        r1 = False
    elif level == 4 and r1:
        yr21 = -2000
        yr22 = -300
        for i in range(6):
            rocket_2 = Rocket2(rocket2, random.randint(-30, 400), random.randint(yr21, yr22))
            rockets.append(rocket_2)
        r1 = False
    elif level == 5 and r1:
        yr41 = -1200
        yr42 = -500
        for i in range(1):
            rocket_4 = Rocket4(rocket4, random.randint(-30, 400), random.randint(yr41, yr42))
            rockets.append(rocket_4)    
        r1 = False
    elif level == 6 and r1:
        yr11 = -1200
        yr12 = -300
        yr21 = -2000
        yr22 = -1000        
        yr41 = -1200
        yr42 = -500
        for i in range(10):
            rocket_1 = Rocket1(rocket1, random.randint(-30, 400), random.randint(yr11, yr12))
            rockets.append(rocket_1)
        for i in range(3):
            rocket_2 = Rocket2(rocket2, random.randint(-30, 400), random.randint(yr21, yr22))
            rockets.append(rocket_2)        
        for i in range(1):
            rocket_4 = Rocket4(rocket4, random.randint(-30, 400), random.randint(yr41, yr42))
            rockets.append(rocket_4)    
        r1 = False
    elif level == 7 and r1:
        yr11 = -1500
        yr12 = -400       
        yr41 = -3200
        yr42 = -1500
        for i in range(20):
            rocket_1 = Rocket1(rocket1, random.randint(-30, 400), random.randint(yr11, yr12))
            rockets.append(rocket_1)       
        for i in range(4):
            rocket_4 = Rocket4(rocket4, random.randint(-30, 400), random.randint(yr41, yr42))
            rockets.append(rocket_4)    
        r1 = False
    elif level == 8 and r1:
        yr31 = -2500
        yr32 = -1500        
        for i in range(6):
            rocket_3 = Rocket3(rocket3, random.randint(-30, 400), random.randint(yr31, yr32))
            rockets.append(rocket_3)          
        r1 = False
    elif level == 9 and r1:
        yr11 = -2500
        yr12 = -1000
        yr21 = -3000
        yr22 = -400               
        yr31 = -2500
        yr32 = -1500
        yr41 = -3000
        yr42 = -2000
        for i in range(15):
            rocket_1 = Rocket1(rocket1, random.randint(-30, 400), random.randint(yr11, yr12))
            rockets.append(rocket_1)
        for i in range(5):
            rocket_2 = Rocket2(rocket2, random.randint(-30, 400), random.randint(yr21, yr22))
            rockets.append(rocket_2)                   
        for i in range(4):
            rocket_3 = Rocket3(rocket3, random.randint(-30, 400), random.randint(yr31, yr32))
            rockets.append(rocket_3) 
        for i in range(3):
            rocket_4 = Rocket4(rocket4, random.randint(-30, 400), random.randint(yr41, yr42))
            rockets.append(rocket_4) 
        r1 = False 
    elif level == 10 and r1:
        yrb11 = -400
        yrb12 = -300
        yr11 = -5000
        yr12 = -3000
        yr21 = -7000
        yr22 = -500        
        for i in range(1):
            rocket_boss_1 = RocketBoss1(rocketboss1, 100, random.randint(yrb11, yrb12))
            rockets.append(rocket_boss_1)
        for i in range(10):
            rocket_1 = Rocket1(rocket1, random.randint(-30, 400), random.randint(yr11, yr12))
            rockets.append(rocket_1)
        for i in range(3):
            rocket_2 = Rocket2(rocket2, random.randint(-30, 400), random.randint(yr21, yr22))
            rockets.append(rocket_2)
        yr11 = -2500
        yr12 = -1000
        yr21 = -3000
        yr22 = -400
        r1 = False           
    if motion == 'LEFT':
        if ship.x > 0:
            ship.x -= 10
    elif motion == 'RIGHT':
        if ship.x < 450:
            ship.x += 10
    screen.fill((0, 0, 0))
    moving_fon.update()
    if dollar_move:
        moving_dollar.update()
    if not gameovering and not gamewinning:
        if vns:
            rotate += 2
            ship.rotate(rotate)
        ship.update()
    else:
        gameovermusic.play()
        moving_gameover.update()
    if levelingup:
        moving_level.update()    
    #if r1:
        #r1 = False
    if gamewinning:
        moving_victory.update()
    for i in rockets:
        if ship.check_if_down(i):
            lost_live()
            i.y = 800
        if not gameovering and not gamewinning:
            i.update()
    if fired:
        if laser.y < 0:
            fired = False
        else:
            laser.y -= 10
            laser.update()
        for j in rockets:
            checking = j.explode()
            if checking[0] > 0:
                sound.play()                
                fired = False
            elif checking[0] == 0 or checking[0] == -2:
                points += checking[1]
                #explosion = AnimatedSprite(explode, 4, 4, j.x, j.y)
                sound.play()                
                explodes.append(Explosion(j.x, j.y))
                #pygame.event.wait()                
                rockets.remove(j)
                fired = False
                if checking[0] == -2:
                    rockets = []
            else:
                pass
    for i in explodes:
        i.update(screen)
    if rockets == []:
        if level == 10:
            pygame.mixer.music.stop()
            gamewinning = True
        if not gamewinning:
            level += 1
            explodes = []
            moving_level.x = -300
            sound3.play()
            levelingup = True
            r1 = True
    se_points = points - 50 * extra_lives
    if se_points >= 50:
        extra_lives += 1
        lives += 1
    draw_level_box(level, lives, points)
    if lives == 0 and not gameovering:
        pygame.mixer.music.stop()
        gameovering = True
    clock.tick(FPS)
