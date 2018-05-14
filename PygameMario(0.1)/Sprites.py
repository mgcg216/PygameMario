import pygame as pg
from Settings import *
vec = pg.math.Vector2

class Spritesheet:
    #utility class for loading and parsing spritesheets
    def __init__(self,filename):
        self.spritesheet = pg.image.load(filename).convert()


    def get_image(self, x, y, width, height):
        #grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x, y, width, height))
        image = pg.transform.scale(image, (width * SCALE, height * SCALE))
        return image


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.walking = False
        self.jumping = False
        self.isRight = True
        self.running = False
        self.dead = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_r
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 5.5, HEIGHT / 1.075)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def load_images(self):
        self.standing_r = self.game.spritesheet.get_image(80, 34, 15, 15)
        self.standing_r.set_colorkey(WHITE)
        self.standing_l = pg.transform.flip(self.standing_r, True, False)
        self.walk_frames_r = [self.game.spritesheet.get_image(97, 34, 15, 15),
                              self.game.spritesheet.get_image(114, 34, 15, 15),
                              self.game.spritesheet.get_image(131, 34, 15, 15)]

        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            frame.set_colorkey(WHITE)
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))
        self.jump_frame_r = self.game.spritesheet.get_image(165, 34, 15, 15)
        self.jump_frame_r.set_colorkey(WHITE)
        self.jump_frame_l = pg.transform.flip(self.jump_frame_r, True, False)
        self.turn_r = self.game.spritesheet.get_image(148, 34, 15, 15)
        self.turn_r.set_colorkey(WHITE)
        self.turn_l = pg.transform.flip(self.turn_r, True, False)

    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def jump(self):
        # jump only if standing on a platform
        self.rect.x += 2*SCALE
        self.rect.bottom += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 2*SCALE
        self.rect.bottom -= 2
        if hits and not self.jumping:
            self.game.jump_sound_small.play()
            self.jumping = True
            self.vel.y = -PLAYER_JUMP


    def update(self):
        self.animate()
        #jumping up slower than coming down

        if self.vel.y >= 0:
            self.acc = vec(0, PLAYER_GRAV)
        if self.vel.y < 0:
            self.acc = vec(0, PLAYER_GRAV*.4)


        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC
        if keys[pg.K_x]:
            if keys[pg.K_LEFT]:
                self.acc.x = -PLAYER_ACC*5/3
            if keys[pg.K_RIGHT]:
                self.acc.x = PLAYER_ACC*5/3

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        if not self.jumping:
            self.vel += self.acc
        #locks in jump animation to a certain extent
        if self.jumping:
            self.vel.y += self.acc.y
            self.vel.x += self.acc.x*.4
        if abs(self.vel.x) < 0.2:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        # player hits left side of screen
        if self.pos.x <0 + self.rect.width/2:
            self.pos.x =0 + self.rect.width/2
        self.rect.midbottom = self.pos

    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x !=0:
            self.walking = True
        else:
            self.walking = False
        #show walk animation
        if self.walking:
            speed = 1;
            if self.running:
                speed = 5/3
            else:
                speed = 1
            if now - self.last_update > 75/speed:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_r)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    if not self.jumping: #lock in left and right when jumping to match game
                        self.isRight = True
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    if not self.jumping:
                        self.isRight = False
                    self.image = self.walk_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        # show idle animation
        if not self.jumping and not self.walking:
            if self.isRight:
                self.image = self.standing_r
            if not self.isRight:
                self.image = self.standing_l
        # show jumping animation
        if self.jumping:
            if self.isRight:
                self.image = self.jump_frame_r
            if not self.isRight:
                self.image = self.jump_frame_l


class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y, t):
        self.groups = game.all_sprites, game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        images = [(self.game.spritesheet_tile.get_image(0,0,15,15)),  #ground
                  (self.game.spritesheet_tile.get_image(0,16,15,15)),  #brick
                  (self.game.spritesheet_tile.get_image(0, 128, 32, 32)),  # small pipe]
                  (self.game.spritesheet_tile.get_image(0, 144, 32, 16)),  # pipe body
                  (self.game.spritesheet_tile.get_image(16, 0, 15, 15)),  # brick
                  ]
        self.image = images[t]
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class PowerUp(pg.sprite.Sprite):
    def __init__(self, game, x, y, t):
        self.groups = game.all_sprites, game.powerup
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        images = [(self.game.spritesheet_tile.get_image(0,0,15,15)),  #ground
                  (self.game.spritesheet_tile.get_image(0,16,15,15)),  #brick
                  (self.game.spritesheet_tile.get_image(0, 128, 32, 32)),  # small pipe]
                  (self.game.spritesheet_tile.get_image(0, 144, 32, 16)),  # pipe body
                  (self.game.spritesheet_tile.get_image(16, 0, 15, 15)),  # brick
                  ]
        self.image = images[t]
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        def update(self):
            pass


class Block(pg.sprite.Sprite):
    def __init__(self, game, x, y, t):
        self.groups = game.all_sprites, game.blocks
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        images = [(self.game.spritesheet_tile.get_image(368, 0, 15, 15)),  # Question 1
                  (self.game.spritesheet_tile.get_image(385, 0, 15, 15)),  # Question 2
                  (self.game.spritesheet_tile.get_image(400, 0, 15, 15)),  # Question 3
                  (self.game.spritesheet_tile.get_image(416, 0, 15, 15)),  # Question Empty
                  (self.game.spritesheet_tile.get_image(16, 0, 15, 15)),   # brick
                  ]
        self.image = images[t]
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def animate(self):
        pass



