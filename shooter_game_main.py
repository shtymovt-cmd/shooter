import pygame as pg
from random import randint
from time import *
pg.init()  

FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
clock = pg.time.Clock()

HP = 3

W, H = 700, 500

background = pg.transform.scale(pg.image.load('galaxy.jpg'), (W, H))

#создай окно игры
window = pg.display.set_mode((W, H))


#задай фон сцены
window.blit(background, (0, 0))

game = True

class Area():
    def __init__(self, x=0, y=0, width=10, height=10, color = None):
        self.rect = pg.Rect(x, y, width, height)                      
        self.fill_color = color
        self.spisok = []
    

class Lable(Area):
    def __init__(self, text, x=0, y=0, width=10, height=10, bg_color = None, text_color = BLACK, fsize = 25):
        super().__init__(x, y, width, height, bg_color)
        self.bg_color = bg_color
        self.set_text(text, text_color = text_color, fsize = fsize)
        self.fsize = fsize
        self.text_color = text_color

    def draw(self, shift_x=0, shift_y=0):
        if not self.bg_color is None:
            draw.rect(window, self.fill_color, self.rect)
        window.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))

    def set_text(self, text, fsize=None, text_color=None):
        if fsize is None:
            fsize = self.fsize
        if text_color is None:
            text_color = self.text_color
        self.text = text
        self.image = pg.font.Font(None, fsize).render(text, True, text_color)

class Game():
    run = True
    finish = False
    win = False
    lose = False
    sound_played = False
    objs = []
    shooting_rate = 0.5

    
    def update(self):
        for i in pg.event.get():
            if i.type == pg.QUIT:
                self.run = False
            for obj, f_type in self.objs:
                if f_type == 'on_click' and obj.rect.collidepoint(x, y):
                    obj.on_click(x,y)
    
        if self.finish == False:
            player.update()
            enemies.update()
            asteroids.update()
            bullets.update()

            window.blit(background, (0, 0))
            
            player.reset()
            enemies.draw(window)
            asteroids.draw(window)
            bullets.draw(window)
            
        score_label.draw()
        missed_label.draw()
        score.draw()
        missed.draw()

        if player.sc >= 10 and player.ms < 10:
            self.win = True
            self.finish = True

        if player.sc < 10 and player.ms >= 10:
            self.lose = True
            self.finish = True
        

        if self.finish == True and self.lose == True:
            lose_text.draw()            

        if self.finish == True and self.win == True:
            win_text.draw()


    def start(self):
        while game.run == True:
            self.update()
            btn_start.draw()

            display.update()
            clock.tick(FPS)

    def add_handler(self, obj):
        if obj in self.objs:
            self.objs.remove(obj)
        self.objs.append(obj)
            
        

class GameSprite(pg.sprite.Sprite):
    def __init__(self, image_name, x, y, w, h, speed):
        super().__init__()
        self.image = pg.transform.scale(pg.image.load(image_name), (w, h))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= H:
            self.rect.x = randint(0, 650)
            self.rect.y = -50
            player.ms += 1
            missed.set_text(str(player.ms))

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0 - self.rect.height:
            self.kill()
        sprites_list = pg.sprite.groupcollide(bullets, enemies, True, True)
        sprites_num = len(sprites_list)
        if sprites_num != 0:
            player.sc += sprites_num
            score.set_text(str(player.sc))
            for i in range(sprites_num):
                enemies.add(Enemy('ufo.png', randint(0, 650), -50, 50, 50, randint(1, 3)))
            


class Player(GameSprite):
    sc = 0
    ms = 0
    hp = HP
    last_bullet = time()

    def fire(self):
        cur_time = time()
        if cur_time - self.last_bullet > game.shooting_rate:
            bullets.add(Bullet('bullet.png', self.rect.centerx - 7, self.rect.y, 15, 30, 3))
            self.last_bullet = cur_time
        

    def update(self):
        keys_pressed = pg.key.get_pressed()
        if keys_pressed[pg.K_LEFT] and self.rect.x >= 0:
            self.rect.x -= self.speed
        if keys_pressed[pg.K_RIGHT] and self.rect.x <= W - self.rect.width: 
            self.rect.x += self.speed
        if keys_pressed[pg.K_SPACE]:
            self.fire()
        monsters_list = pg.sprite.spritecollide(player, enemies, True)
        asteroids_list = pg.sprite.spritecollide(player, asteroids, True)
        if len(asteroids_list) != 0:
            game.lose = True
            game.finish = True

        if len(monsters_list) != 0:
            game.lose = True
            game.finish = True

player = Player('rocket.png', 400, 425, 50, 70, 5)

enemies = pg.sprite.Group()
asteroids = pg.sprite.Group()
bullets = pg.sprite.Group()

for i in range(5):
    enemies.add(Enemy('ufo.png', randint(0, 650), -50, 50, 50, randint(1, 3)))

for i in range(5):
    asteroids.add(Asteroid('asteroid.png', randint(0, 650), -50, 50, 50, randint(1, 3)))

game = Game()

score_label = Lable('счет:', 10, 10, 100, 30, text_color=WHITE, fsize=30)
missed_label = Lable('пропущено:', 10, 50, 150, 30, text_color=WHITE, fsize=30)
score = Lable(str(player.sc), 120, 10, 100, 30, text_color=WHITE, fsize=30)
missed = Lable(str(player.ms), 170, 50, 150, 30, text_color=WHITE, fsize=30)
lose_text = Lable('YOU LOSE', 170, 200, 100, 30, text_color=RED, fsize=100)
win_text = Lable('YOU WON', 170, 200, 100, 30, text_color=GREEN, fsize=100)

while game.run == True:

    game.update()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            game = False

    pg.display.update()
    clock.tick(FPS)