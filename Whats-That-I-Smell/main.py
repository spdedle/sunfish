import pygame
import sys
import random
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((800, 500))
clock = pygame.time.Clock()
SCRATCHYFONT32 = pygame.font.Font('VINERITC.ttf',32)
SCRATCHYFONT45 = pygame.font.Font('VINERITC.ttf',45)

spawn_interval = 3000
growth_interval = 100
growth_count = 80
raccoon_start_size = 64
win_time = 45000  #seconds to win
game_start_time = None

raccoon_images = [pygame.image.load(f"raccoon{i}.png").convert_alpha() for i in range(1, 4)]
raccoon_attack_image = pygame.image.load("raccoon_attack.png").convert_alpha()
background = pygame.image.load("background.png")
background_width = background.get_width()
counter = pygame.image.load("counter.png")
boom_image = pygame.image.load("boom.png").convert_alpha()

scroll_x = 0
scroll_speed = 7
crosshair = pygame.image.load("crosshair.png").convert_alpha()
cross_w, cross_h = crosshair.get_size()
booms = []  
boom_duration = 300
class RaccoonEnemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        image_index = random.randint(0, len(raccoon_images) - 1)
        self.original_image = raccoon_images[image_index]
        self.grow_count = 0
        self.spawn_time = pygame.time.get_ticks()
        self.last_grow_time = self.spawn_time
        self.transformed = False
        self.alive = True

        self.size = raccoon_start_size
        self.image = pygame.transform.scale(self.original_image, (self.size, self.size))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 1600 - self.rect.width)
        self.rect.top = random.randint(250, 350)

    def update(self, current_time):
        if not self.alive or self.transformed:
            return

        if current_time - self.last_grow_time >= growth_interval and self.grow_count < growth_count:
            self.grow()

        if current_time - self.spawn_time >= growth_count * growth_interval:
            self.transform_to_other()

    def grow(self):
        self.grow_count += 1
        self.last_grow_time = pygame.time.get_ticks()
        old_top = self.rect.top
        old_x = self.rect.x
        self.size += 1
        self.image = pygame.transform.scale(self.original_image, (self.size, self.size))
        self.rect = self.image.get_rect()
        self.rect.x = old_x
        self.rect.top = old_top

    def transform_to_other(self):
        self.transformed = True
        old_top = self.rect.top
        old_x = self.rect.x
        self.image = pygame.transform.scale(raccoon_attack_image, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.x = old_x
        self.rect.top = old_top
        global status
        status = 'lose'

raccoon_group = pygame.sprite.Group()
SPAWN_RACCOON = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_RACCOON, spawn_interval)

handsleft = pygame.image.load("handsleft.png")
handsright = pygame.image.load("handsright.png")
handsleft_h = handsleft.get_height()
handsright_h = handsright.get_height()
handsleft_w = handsleft.get_width()
handsright_w = handsright.get_width()

winscreen = pygame.image.load("winscreen.png").convert_alpha()
losescreen = pygame.image.load("losescreen.png").convert_alpha()


def start(screen, font=SCRATCHYFONT32):
    images = [pygame.image.load(f"image{i}.png") for i in range(9)]
    count = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                if count < len(images) - 1:
                    count += 1
            elif event.type == KEYDOWN and event.key == K_RETURN:
                return

        screen.fill((0, 0, 0))
        screen.blit(images[count], images[count].get_rect(center=(400, 250)))

        if count == len(images) - 1:
            text1 = font.render('Press Enter to Continue', True, (255, 255, 255))
            screen.blit(text1, text1.get_rect(center=(400, 400)))

        pygame.display.update()





def instructions(screen, font = SCRATCHYFONT32):
    screen.fill((0,0,0))
    text1 = SCRATCHYFONT45.render('How To Play', True, (200,222,195))
    screen.blit(text1, text1.get_rect(center=(400, 50)))
    text2 = font.render("Don't let the raccoons near you! ", True, (200,222,195))
    screen.blit(text2, text2.get_rect(center=(400, 150)))
    text3 = font.render('Use your mouse to aim!', True, (200,222,195))
    screen.blit(text3, text3.get_rect(center=(400, 200)))
    text4 = font.render("Left-click to shoot! ", True, (200,222,195))
    screen.blit(text4, text4.get_rect(center=(400, 250)))
    text5 = font.render("Use A and D to move along the counter! ", True, (200,222,195))
    screen.blit(text5, text5.get_rect(center=(400, 300)))
    text6 = font.render("Press Enter to Continue ", True, (200,222,195))
    screen.blit(text6, text6.get_rect(center=(400, 400)))
    pygame.display.update()

def win(screen):
    screen.fill((0,0,0))
    screen.blit(winscreen, (150, 0))
    text = SCRATCHYFONT32.render('Press Enter to Play Again', True, (255,255,255))
    screen.blit(text, text.get_rect(center=(400, 450)))
    pygame.display.update()

def lose(screen):
    screen.fill((0,0,0))
    screen.blit(losescreen, (150,0))
    text = SCRATCHYFONT32.render('Press Enter to Play Again', True, (255,255,255))
    screen.blit(text, text.get_rect(center=(400, 450)))
    pygame.display.update()

def reset_game():
    global scroll_x, scroll_y, status, raccoon_group, game_start_time
    scroll_x = 0
    scroll_y = 0
    status = 'game'
    raccoon_group.empty()
    booms.clear()
    game_start_time = pygame.time.get_ticks()

scroll_x = 0
scroll_y = 0
status = 'startstat'
running = True

while running:
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == SPAWN_RACCOON and status == 'game':
            raccoon_group.add(RaccoonEnemy())
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_RETURN and status == 'startstat':
                status = 'instructions'
            elif event.key == K_RETURN and status == 'instructions':
                status = 'game'
                game_start_time = current_time
            elif event.key == K_RETURN and status in ['win', 'lose']:
                reset_game()
        elif (event.type == MOUSEBUTTONUP or (event.type == KEYDOWN and event.key == K_SPACE)) and status == 'game':
            mx, my = pygame.mouse.get_pos()
            for raccoon in raccoon_group:
                raccoon_screen_rect = raccoon.rect.move(scroll_x, -scroll_y)
                if raccoon.alive and raccoon_screen_rect.collidepoint(mx, my):
                    raccoon.alive = False
                    raccoon.kill()
                    boom_x = raccoon.rect.x  
                    boom_y = raccoon.rect.y  
                    booms.append((boom_x, boom_y, current_time))
                    break

    if status == 'startstat':
        start(screen)
        status = 'instructions'
    elif status == 'instructions':
        instructions(screen)
    elif status == 'game':
        keys = pygame.key.get_pressed()
        if keys[K_a]:
            scroll_x = min(scroll_x + scroll_speed, 0)
        if keys[K_d]:
            max_scroll = screen.get_width() - background_width
            scroll_x = max(scroll_x - scroll_speed, max_scroll)

        if game_start_time and current_time - game_start_time >= win_time:
            status = 'win'

        pygame.mouse.set_visible(False)
        screen.blit(background, (scroll_x, scroll_y))
        mouse_x, mouse_y = pygame.mouse.get_pos()

        raccoon_group.update(current_time)
        for raccoon in raccoon_group:
            screen.blit(raccoon.image, (raccoon.rect.x + scroll_x, raccoon.rect.y - scroll_y))
        for boom in booms[:]:
            x, y, t = boom
            if current_time - t < boom_duration:
                screen.blit(boom_image, (x + scroll_x, y - scroll_y))  # apply scroll here
            else:
                booms.remove(boom)

        screen.blit(crosshair, (mouse_x - cross_w // 2, mouse_y - cross_h // 2))
        screen.blit(counter, (scroll_x, scroll_y))

        if mouse_x > 400:
            screen.blit(handsright, (400, 500 - handsright_h))
        else:
            screen.blit(handsleft, (400 - handsleft_w, 500 - handsleft_h))

    elif status == 'win':
        win(screen)
    elif status == 'lose':
        lose(screen)

    pygame.display.flip()
    clock.tick(120)

pygame.quit()
sys.exit()