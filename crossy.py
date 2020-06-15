import pygame
import datetime
import time
from random import randint
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
size = (700, 600)
screen =  pygame.display.set_mode(size)
pygame.display.set_caption("Crossy")
pygame.init()

class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.image = pygame.transform.scale(pygame.image.load('smiley.png'), (30, 30))

        self.image.set_colorkey(WHITE) 
        self.rect = self.image.get_rect()

    def Up(self):
        self.rect.y -= 60
    def Down(self):
        self.rect.y += 60
    def Left(self):
        self.rect.x -= 3
    def Right(self):
        self.rect.x += 3

    def approx(self, group):
        for sprite in group:
            if abs(sprite.rect.y - self.rect.y) <= 25:
                self.rect.y = sprite.rect.y + 15
class Car(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        rand = randint(0, 4)
        if rand < 3:
            self.image = pygame.transform.scale(pygame.image.load('car.png'), (100, 50))
        else:
            self.image = pygame.transform.scale(pygame.image.load('truck.png'), (150, 50))
        self.image.set_colorkey(WHITE) 
        self.rect = self.image.get_rect()
        self.velocity = 5

    def update(self):
        self.rect.x -= self.velocity


class Car2(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        rand = randint(0, 4)
        if rand < 3:
            self.image = pygame.transform.scale(pygame.image.load('car2.png'), (100, 50))
        else:
            self.image = pygame.transform.scale(pygame.image.load('truck2.png'), (150, 50))
        self.image.set_colorkey(WHITE) 
        self.rect = self.image.get_rect()
        self.velocity = 5

    def update(self):
        self.rect.x += self.velocity
        
class Road(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.transform.scale(pygame.image.load('road.jpg'), (700, 60))
        self.velocity  =5
        self.image.set_colorkey(WHITE) 
        self.rect = self.image.get_rect()

class Road2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.transform.scale(pygame.image.load('road.jpg'), (700, 60))
        self.velocity = 5
        self.image.set_colorkey(WHITE) 
        self.rect = self.image.get_rect()

class Grass(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.transform.scale(pygame.image.load('grass.jpg'), (700, 60))

        self.image.set_colorkey(WHITE) 
        self.rect = self.image.get_rect()

font = pygame.font.Font('mariofont.ttf', 30)
rads = pygame.sprite.Group()
cars = pygame.sprite.Group()
CREATECAR = pygame.USEREVENT + 2
pygame.time.set_timer(CREATECAR, 2500)
new = 540
jump = 0
score = 0
roads = pygame.sprite.Group()
CREATEROAD = pygame.USEREVENT + 1
pygame.time.set_timer(CREATEROAD, 1)
clock = pygame.time.Clock()
carryOn = True
player = Player()
player.rect.x = 335
player.rect.y = 315
while carryOn:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            carryOn = False 
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_UP:
                player.Up()
                player.approx(roads)
                score += 1
                new += 60
            elif event.key==pygame.K_DOWN:
                player.Down()
                score -= 1
                new -= 60
        if event.type==CREATEROAD:
            randy = randint(0,3)
            if randy<3:
                rando = randint(0, 1)
                if rando == 0:
                    new_road = Road()
                elif rando == 1:
                    new_road = Road2()
                new_road.velocity = randint(40, 60)/10
                roads.add(new_road)
                rads.add(new_road)
                new_road.rect.y = new
                new = new - 60
            else:
                new_grass = Grass()
                roads.add(new_grass)
                new_grass.rect.y = new
                new = new - 60
            if new <= -10000:
                pygame.time.set_timer(CREATEROAD, 0)
            elif new>-10000:
                pygame.time.set_timer(CREATEROAD, 10)
        if event.type==CREATECAR:
            for sprite in rads:
                if sprite.rect.bottom > -300 and sprite.rect.top < 600:
                    if isinstance(sprite, Road):
                        new_car = Car2()
                        new_car.velocity = sprite.velocity
                        new_car.rect.right = -1 * randint(50, 275)
                    elif isinstance(sprite, Road2):
                        new_car = Car()
                        new_car.velocity = sprite.velocity
                        new_car.rect.left = randint(750, 975) 
                    new_car.rect.top = sprite.rect.top + 5
                    cars.add(new_car)
    if pygame.sprite.spritecollideany(player, cars):
        carryOn = False
    if player.rect.top > 600:
        carryOn = False
    if keys[pygame.K_RIGHT]:
        player.Right()
    elif keys[pygame.K_LEFT]:
        player.Left()
    for sprite in roads:
        sprite.rect.y+=2
        if sprite.rect.top > 600:
            sprite.kill()
    player.rect.y+=2
    screen.fill(WHITE)
    for sprite in roads:
        screen.blit(sprite.image, sprite.rect)
    screen.blit(player.image, player.rect)
    for sprite in cars:
        sprite.rect.y+=2
        sprite.update()
        screen.blit(sprite.image, sprite.rect)
    text = font.render(str(score), True, BLACK)
    textrect = text.get_rect()
    screen.blit(text, textrect)
    pygame.display.update()
    clock.tick(30)
time.sleep(0.5)
now = datetime.datetime.now()
while True:
    screen.fill(BLACK)
    gmov = font.render("GAME OVER", True, WHITE)
    gmovrect = gmov.get_rect()
    gmovrect.x = 220
    gmovrect.y = 280
    scor = font.render("SCORE:" + str(score), True, WHITE)
    scorect = scor.get_rect()
    scorect.x = 220
    scorect.y = 230
    newnow = datetime.datetime.now()
    screen.blit(gmov, gmovrect)
    screen.blit(scor, scorect)
    if (newnow - now).seconds >= 3:
        break
    pygame.display.update()
pygame.quit()
                
