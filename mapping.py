import pygame
import os
import time
import sys
from player import Player
from tiles import Tile, Coin
maps = os.listdir('maps')
levels = list()
for level in maps:
    levels.append(open(f'maps/{level}', 'r').read().splitlines())
tile_size = 64
screen_width = 1200
screen_height = len(levels[0]) * tile_size
class Level:
    def __init__(self, surface):
        self.display_surface = surface
        self.setup_level(levels[0])
        self.world_shift = 0
        self.updates = 0
        self.amntcoins = 0
        self.font = pygame.font.Font('BAHNSCHRIFT.TTF', 32)
        self.level = 0
    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        for rdex,row in enumerate(layout):
            for cdex, cell in enumerate(row):
                x = cdex * tile_size
                y = rdex * tile_size
                if cell == 'X':
                    tile = Tile((x,y), tile_size)
                    self.tiles.add(tile)
                elif cell == 'P':
                    player = Player((x,y), tile_size)
                    self.player.add(player)
                elif cell == 'C':
                    coin = Coin((x,y), tile_size)
                    self.coins.add(coin)
                elif cell == ' ':
                    pass
                else:
                    print(f'unknown cell {cell} at Ln {rdex}, Col {cdex}')
                    pygame.quit()
        self.amntcoins = len(self.coins.sprites())
    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x
        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = self.pspeed
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -self.pspeed
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = self.pspeed
        if player.rect.centery > 2000:
            self.setup_level(levels[self.level])
    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
        for coin in self.coins.sprites():
            if coin.rect.colliderect(player.rect):
                coin.kill()
                player.coins += 1
    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
            player.jumpable = player.direction.y == 0
    def nextlevel(self):
        if self.level + 1 == len(levels):
            self.coinstr = 'Good  Job ,  You  Beat  The  Game!'
            self.coinsurf = self.font.render(self.coinstr,False,(255,255,255))
            x, y = screen_width / 2, screen_height / 2
            self.coinrect = self.coinsurf.get_rect(center=(x, y))
            self.display_surface.blit(self.coinsurf, self.coinrect)
            pygame.display.flip()
            pygame.event.pump()
            pygame.time.delay(4 * 1000)
            print('Good Job, You Beat The Game!')
            pygame.quit()
            sys.exit()
        else:
            self.level += 1
            self.setup_level(levels[self.level])
    def __call__(self):
        if self.updates == 0:
            self.setup_level(levels[0])
            self.pspeed = self.player.sprite.speed
        if self.player.sprite.coins == self.amntcoins:
            self.nextlevel()
        self.coinstr = str(self.player.sprite.coins) if self.player.sprite.coins != self.amntcoins else 'You Win!'
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.coins.update(self.world_shift)
        self.coins.draw(self.display_surface)
        self.player.update()
        self.player.draw(self.display_surface)
        self.coinsurf = self.font.render(self.coinstr,False,(255,255,255))
        self.coinrect = self.coinsurf.get_rect(topleft = (20,20))
        self.display_surface.blit(self.coinsurf, self.coinrect)
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.scroll_x()
        self.updates += 1