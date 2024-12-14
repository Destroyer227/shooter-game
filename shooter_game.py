from pygame import *
from random import randint

font.init()
font1 = font.SysFont('Arial', 56)
font2 = font.SysFont('Arial', 24)
rank_s = font1.render('Perfect! Rank S', True, (140, 140, 255))
rank_a = font1.render('Great! Rank A', True, (140, 255, 140))
rank_b = font1.render('Good! Rank B', True, (255, 255, 100))
rank_c = font1.render('Rank C', True, (255, 160, 60))
rank_d = font1.render('You lose! Rank D', True, (255, 80, 80))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play(loops = -1)
fire_sound = mixer.Sound('fire.ogg')


img_bg = 'galaxy.jpg'
img_bullet = 'bullet.png'
img_player = 'rocket.png'
img_enemy = 'ufo.png'
img_asteroid = 'asteroid.png'

win_width = 900
win_height = 700
display.set_caption('Shooter')
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_bg), (win_width, win_height))

score = 0
freeze = 0
goal = 30
lost = 0
max_lost_s = 0
max_lost_a = 3
max_lost_b = 8
max_lost_c = 15
size = 0




class GameSprite(sprite.Sprite):
    def __init__(self, player_image,player_x ,player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if freeze == 0:
            if keys[K_LEFT] and self.rect.x > 0:
                self.rect.x -= self.speed
            if keys[K_RIGHT] and self.rect.x < win_width - 75:
                self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx - 7, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1
  
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            size = randint(30, 100)
            self.size_x = size
            self.size_y = size
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0

player = sprite.Group
ship = Player(img_player, 5, win_height - 150, 80, 100, 10)
player.add(ship)

monsters = sprite.Group()
for i in range(1, 5):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 3))
    monsters.add(monster)

bullets = sprite.Group()

asteroids = sprite.Group()
for i in range(1, 3):
    size = randint(30, 100)
    asteroid = Asteroid(img_asteroid, randint(80, win_width - 80), -80, size, size, randint(1, 3))
    asteroids.add(asteroid)

finish = 0
run = True
clock = time.Clock()
FPS = 60

def end_game():
    for b in bullets:
        b.kill()
    for m in monsters:
        m.kill()
    for a in asteroids:
        a.kill()
    

while run:

    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()
    if finish == 0:
        window.blit(background, (0, 0))
        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        collides = sprite.groupcollide(asteroids, bullets, False, True)
        
        if lost > max_lost_c:
            end_game()
            finish = 180
            window.blit(rank_d, (win_width / 2 - 225, win_height / 2 - 21))

        if freeze > 0:
            freeze = freeze - 1

        if score >= goal:
            end_game()
            finish = 180
            if lost > max_lost_b:
                window.blit(rank_c, (win_width / 2 - 95, win_height / 2 - 21))
            elif lost > max_lost_a:
                window.blit(rank_b, (win_width / 2 - 183, win_height / 2 - 21))
            elif lost > max_lost_s:
                window.blit(rank_a, (win_width / 2 - 186, win_height / 2 - 21))
            else:
                window.blit(rank_s, (win_width / 2 - 207, win_height / 2 - 21))

        text = font2.render('Score: ' + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 10))

        text_lose = font2.render('Missed: ' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 40))

        display.update()
        clock.tick(FPS)
    else:


        finish = finish - 1
        window.blit(background, (0, 0))
        if freeze > 0:
            freeze = freeze - 1
        ship.update()
        ship.reset()

        text = font2.render('Score: ' + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 10))

        text_lose = font2.render('Missed: ' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 40))

        text_restart = font2.render('Restart in ' + str((finish // 6 + 1) / 10), 1, (255, 255, 255))
        window.blit(text_restart, (10, 70))

        if lost > max_lost_c:
            window.blit(rank_d, (win_width / 2 - 225, win_height / 2 - 21))
        elif lost > max_lost_b:
            window.blit(rank_c, (win_width / 2 - 95, win_height / 2 - 21))
        elif lost > max_lost_a:
            window.blit(rank_b, (win_width / 2 - 183, win_height / 2 - 21))
        elif lost > max_lost_s:
            window.blit(rank_a, (win_width / 2 - 186, win_height / 2 - 21))
        else:
            window.blit(rank_s, (win_width / 2 - 207, win_height / 2 - 21))

        if finish < 1:
            score = 0
            lost = 0
            finish = 0
            for i in range(1, 5):
                monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 3))
                monsters.add(monster)
            asteroids = sprite.Group()
            for i in range(1, 3):
                size = randint(30, 100)
                asteroid = Asteroid(img_asteroid, randint(80, win_width - 80), -80, size, size, randint(1, 3))
                asteroids.add(asteroid)
            for b in bullets:
                b.kill()

        display.update()
        clock.tick(FPS)


time.delay(50)