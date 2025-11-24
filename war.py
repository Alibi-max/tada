# pip install pyinstaller
# pyinstaller -- onefile <название файла>
import pygame 
import random
pygame.init()
width = 800
heigth =600
window = pygame.display.set_mode((width, heigth))
pygame.display.set_caption('Cosmo-Shooter')
background = pygame.transform.scale(pygame.image.load('cosmos.png'), (width, heigth))

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, sprite_image, widht, heigth, x, y, speed_x, speed_y ):
        pygame.sprite.Sprite.__init__(self)
        self.width = widht
        self.height = heigth
        self.image =  pygame.transform.scale(pygame.image.load(sprite_image), (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y 

    def draw_image(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, sprite_image, widht, height, x, y, speed_x, speed_y, hp ):
        super().__init__( sprite_image, widht, height, x, y, speed_x, speed_y )
        self.hp = hp

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def fire(self):
        bullet = Bullet('laser beam.png', 20, 20, self.rect.centerx, self.rect.top, 0, 5)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed_y
        if self.rect.y > 600:
            self.rect.y = -40
            self.rect.x = random.randint(0, 700)

class Asteroid(GameSprite):
    def update(self):
        self.rect.y +=self.speed_y
        self.rect.x +=self.speed_x
        if self.rect.y >600 or self.rect.x < 0:
            self.rect.y = random.randint(-40,40)
            self.rect.x = random.randint(700,800)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed_y
        if self.rect.y < 0:
            self.kill()

score = 0

pygame.mixer.init()
pygame.mixer.music.load('8d82b5_Star_Wars_Main_Theme_Song.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.7)
fire_sound =pygame.mixer.Sound('lasergun-35817.ogg')
boom_sound =pygame.mixer.Sound('vine-boom-392646.mp3')

RED = (255, 0, 0)
WHITE = (255, 255, 255)

font_win = pygame.font.SysFont('Georgia', 32)
enemy_win = font_win.render('Enemy WIN', True, RED) 
font_hp =pygame.font.SysFont('Arial', 32)
font_enemy =pygame.font.SysFont('Arial', 32)


player = Player('hero.png', 100, 100, 100, 500, 0, 0, 3)
font_hp_ren = font_hp.render(f'Оставшиеся жизни: {player.hp}', True, WHITE)


enemies = pygame.sprite.Group()
for i in range(5):
    enemy = Enemy('alien.png',70, 35, random.randint(0,700), -40, 0, random.randint(2,4))
    enemies.add(enemy)

bullets = pygame.sprite.Group()
asteroids =pygame.sprite.Group()
for i in range(2):
    asteroid = Asteroid('asteroid.png', 70, 70, random.randint(500,800), random.randint(-40,40), -5, 5)
    asteroids.add(asteroid)
health_point = GameSprite('heart.png', 30, 30, random.randint(200, 600), random.randint(100, 400), 0, 0)


clock = pygame.time.Clock()

game = True
finish = False

while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        elif event.type == pygame.KEYDOWN:
            #if event.key == pygame.K_w:
            #   player.speed_y = -5
            #elif event.key == pygame.K_s:
            #    player.speed_y = 5
            if event.key == pygame.K_a:
                player.speed_x = -5
            elif event.key == pygame.K_d:
                player.speed_x = 5     
            elif event.key == pygame.K_SPACE:
                player.fire()
        elif event.type == pygame.KEYUP:
            #if event.key == pygame.K_w:
            #    player.speed_y = 0
            #elif event.key == pygame.K_s:
            #    speed_y = 0
            if event.key == pygame.K_a:
                player.speed_x = 0
            elif event.key == pygame.K_d:
                player.speed_x = 0

    if not finish:
        font_hp_ren = font_hp.render(f'Оставшиеся жизни: {player.hp}', True, WHITE)
        window.blit(background, (0, 0))
        window.blit(font_hp_ren, (10, 50))
        health_point.draw_image()
        player.draw_image()
        player.update()
        enemies.draw(window)
        enemies.update()
        asteroids.draw(window)
        asteroids.update()
        bullets.draw(window)
        bullets.update()
        
        if pygame.sprite.spritecollide(player, enemies, True):
            if player.hp > 1:
                player.hp -= 1
                enemy = Enemy('alien.png', 70, 70, random.randint(0,700), -40, 0, random.randint(2,4))
                enemies.add(enemy)
            else:
                finish = True
                window.blit(enemy_win, (300, 300))
                pygame.mixer.music.stop()

        if pygame.sprite.groupcollide(enemies, bullets, True, True):
            enemy = Enemy('alien.png', 70, 70, random.randint(0,700), -40, 0, random.randint(2,4))
            enemies.add(enemy)

        if pygame.sprite.collide_rect(player, health_point):
            if player.hp < 5:
                player.hp += 1
            health_point.rect.x = random.randint(200,600)
            health_point.rect.y = random.randint(100,400)
        if pygame.sprite.spritecollide(player, asteroids, True):
            if player.hp >3:
                player.hp -= 3
                asteroid = Asteroid('asteroid.jpg', 70, 70, random.randint(500,800), random.randint(-40,40), -5, 5)
                asteroids.add(asteroid)
            else:
                finish = True
                window.blit(enemy_win, (300,300))   
                pygame.mixer.music.stop()

        

    pygame.display.update()

    clock.tick(60)
