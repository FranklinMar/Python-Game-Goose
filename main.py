import pygame
from pygame.constants import *
import random
import os

  
_circle_cache = {}
def _circlepoints(r):
    r = int(round(r))
    if r in _circle_cache:
        return _circle_cache[r]
    x, y, e = r, 0, 1 - r
    _circle_cache[r] = points = []
    while x >= y:
        points.append((x, y))
        y += 1
        if e < 0:
            e += 2 * y - 1
        else:
            x -= 1
            e += 2 * (y - x) - 1
    points += [(y, x) for x, y in points if x > y]
    points += [(-x, y) for x, y in points if x]
    points += [(x, -y) for x, y in points if y]
    points.sort()
    return points

'''
Code for rendering text with outline
Credit to: 
https://stackoverflow.com/questions/54363047/how-to-draw-outline-on-the-fontpygame
'''
def render(text, font, gfcolor=pygame.Color('dodgerblue'), ocolor=(255, 255, 255), opx=2):
    textsurface = font.render(text, True, gfcolor).convert_alpha()
    w = textsurface.get_width() + 2 * opx
    h = font.get_height()

    osurf = pygame.Surface((w, h + 2 * opx)).convert_alpha()
    osurf.fill((0, 0, 0, 0))

    surf = osurf.copy()

    osurf.blit(font.render(text, True, ocolor).convert_alpha(), (0, 0))

    for dx, dy in _circlepoints(opx):
        surf.blit(osurf, (dx + opx, dy + opx))

    surf.blit(textsurface, (opx, opx))
    return surf


pygame.init()

# Color parameters
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (125, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Display parameters
DISPLAY_HEIGHT = 800
DISPLAY_WIDTH = 1200
FPS = pygame.time.Clock()
FONT = pygame.font.SysFont('Roboto', 25)

IMAGE_PATH = 'goose'
PLAYER_IMAGES = os.listdir(IMAGE_PATH)

main_display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
background = pygame.transform.scale(pygame.image.load('background.png'), main_display.get_size())
bg_endpoints = [0, background.get_width()]
# bg_endpoint_2 = background.get_width()
bg_move = 3

class Player:
  # Player parameters
  MAX_SPEED = 4
  
  def __init__(self):
    self.object = pygame.image.load('player.png').convert_alpha()  # pygame.Surface((self._WIDTH, self._HEIGHT))
    self.rect = pygame.Rect(main_display.get_width() / 2, main_display.get_height() / 2, *self.object.get_size())  # self.object.get_rect()
    # self.object.fill(GREEN)
    self.speed = [0, 0]
    self.score = 0
    self.image_index = 0
  

class Enemy:
  # Enemy parameters
  _MAX_SPEED = 6
  _MIN_SPEED = 3

  def __init__(self):
      self.object = pygame.image.load('enemy.png').convert_alpha()  # pygame.Surface(self._SIZE)
      self.rect = pygame.Rect(main_display.get_width(), random.randint(0, main_display.get_height() - self.object.get_height()), *self.object.get_size())
      # self.object.fill(RED)
      self.speed = [-random.randint(self._MIN_SPEED, self._MAX_SPEED), 0]


class Bonus:
  # Bonus parameters
  _VALUE = 1
  _MAX_SPEED = 3
  _MIN_SPEED = 1
  _SIZE = (100, 150)

  def __init__(self):
      self.object = pygame.transform.scale(pygame.image.load('bonus.png').convert_alpha(), self._SIZE)  # pygame.Surface(self._SIZE)
      self.rect = pygame.Rect(random.randint(0, main_display.get_width() - self.object.get_width()), 0, *self.object.get_size())
      # self.object.fill(BLUE)
      self.speed = [0, random.randint(self._MIN_SPEED, self._MAX_SPEED)]

  @property
  def value(self):
    return self._VALUE * self.speed[1]
  

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 5000)

CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMAGE, 200)

player = Player()
enemies = []
bonuses = []

GAME = True
while GAME:
  player.speed = [0, 0]
  
  for event in pygame.event.get():
    if event.type == QUIT:
      GAME = False
    if event.type == CREATE_ENEMY:
      enemies.append(Enemy())
    if event.type == CREATE_BONUS:
      bonuses.append(Bonus())
    if event.type == CHANGE_IMAGE:
      player.image_index += 1
      if player.image_index >= len(PLAYER_IMAGES):
        player.image_index = 0
      # player.image_index = (0 if player.image_index >= len(PLAYER_IMAGES) else (player.image_index + 1))
      player.object = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[player.image_index]))
      
  FPS.tick(250)
  # if player_rect.bottom >= main_display.get_height() or player_rect.top < 0:
  #   player_speed[0] = player_speed[0] * (1 if random.random() < 0.5 else -1)
  #   player_speed[-1] = -player_speed[-1]
  # if player_rect.right >= main_display.get_width() or player_rect.left < 0:
  #   player_speed[0] = -player_speed[0]
  #   player_speed[-1] = player_speed[-1] * (1 if random.random() < 0.5 else -1)
  # main_display.fill(BLACK)
  
  for i in range(len(bg_endpoints)):
    bg_endpoints[i] -= bg_move
    if bg_endpoints[i] < -background.get_width():
      bg_endpoints[i] = background.get_width()
    main_display.blit(background, (bg_endpoints[i], 0))
  
  # bg_endpoint_1 -= bg_move
  # bg_endpoint_2 -= bg_move
  # if bg_endpoint_1 < -background.get_width():
  #   bg_endpoint_1 = background.get_width()
  # if bg_endpoint_2 < -background.get_width():
  #   bg_endpoint_2 = background.get_width()
  # main_display.blit(background, (bg_x1, 0))
  # main_display.blit(background, (bg_x2, 0))
  
  keys = pygame.key.get_pressed()
  
  if keys[K_LEFT] and player.rect.left > 0:
    player.speed[0] = -Player.MAX_SPEED
  
  if keys[K_RIGHT] and player.rect.right < main_display.get_width():
    player.speed[0] = Player.MAX_SPEED
  
  if keys[K_UP] and player.rect.top > 0:
    player.speed[-1] = -Player.MAX_SPEED
  
  if keys[K_DOWN] and player.rect.bottom < main_display.get_height():
    player.speed[-1] = Player.MAX_SPEED
  
  main_display.blit(render(f"Score: {player.score}", FONT, WHITE, ocolor=BLACK), (main_display.get_width() - 140, 25))
  main_display.blit(player.object, player.rect)
  player.rect = player.rect.move(player.speed)
  
  for enemy in enemies:
    if enemy.rect.left < 0:
      enemies.remove(enemy)
    else:
      main_display.blit(enemy.object, enemy.rect)
      enemy.rect = enemy.rect.move(enemy.speed)
      if player.rect.colliderect(enemy.rect):
        GAME = False
  
  for bonus in bonuses:
    if bonus.rect.top > main_display.get_height():
      bonuses.remove(bonus)
    else:
      main_display.blit(bonus.object, bonus.rect)
      bonus.rect = bonus.rect.move(bonus.speed)
      if player.rect.colliderect(bonus.rect):
        player.score += bonus.value
        bonuses.remove(bonus)
    
  pygame.display.flip()

pygame.quit()
quit()
