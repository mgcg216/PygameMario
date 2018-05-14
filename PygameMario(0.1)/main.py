import pygame as pg
import random
from Settings import *
from Sprites import *
from os import path


class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):
        #load spritesheets
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        #load spritesheet image
        self.spritesheet_bk = Spritesheet(path.join(img_dir,SPRITESHEET_WORLD))
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET_CHAR))
        self.spritesheet_tile = Spritesheet(path.join(img_dir, SPRITESHEET_TILE))
        #load sound
        self.snd_dir = path.join(self.dir, 'snd')
        self.jump_sound_small = pg.mixer.Sound(path.join(self.snd_dir,'smb_jump-small.wav'))
        self.jump_sound_super = pg.mixer.Sound(path.join(self.snd_dir, 'smb_jump-super.wav'))


    def new(self):
        # start a new game
        self.score = 0 #work on this later
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.powerup = pg.sprite.Group()
        self.blocks = pg.sprite.Group()
        self.player = Player(self)
        for plat in PLATFORM_LIST:
            Platform(self,*plat)

        for block in BLOCKS_LIST:
            Block(self,*block)

        pg.mixer.music.load(path.join(self.snd_dir, 'SuperMarioBros.ogg'))
        self.run()

    def run(self):
        # Game Loop
        pg.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.stop()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        self.collision()


        # Die!
        if self.player.rect.bottom > HEIGHT:
            self.playing = False

    def collision(self):
        # check if player hits a platform
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                highest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                    if hit.rect.bottom < highest.rect.bottom:
                        highest = hit
                #if self.player.pos.x < lowest.rect.right + 15*SCALE and self.player.pos.x > lowest.rect.left - 15*SCALE:
                if self.player.pos.y < lowest.rect.centery:
                    if self.player.vel.y > 0:
                        self.player.pos.y = lowest.rect.top
                        self.player.vel.y = 0
                        self.player.jumping = False
        # checks collision in the y axis
        self.player.rect.bottom -= 30
        hits = pg.sprite.spritecollide(self.player, self.platforms, False)
        self.player.rect.bottom += 30
        if hits:
            left = hits[0]
            for hit in hits:
                if hit.rect.left > left.rect.left:
                    left = hit
            right = hits[0]
            for hit in hits:
                if hit.rect.right > left.rect.right:
                    left = hit
            if self.player.vel.x > 0:
                self.player.pos.x = left.rect.left -7.5*SCALE #hits[0].rect.left - hits[0].rect.width / 4
            if self.player.vel.x < 0:
                self.player.pos.x = right.rect.right + 7.5*SCALE #hits[0].rect.right + hits[0].rect.width / 4

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_z:
                    self.player.jump()
            if event.type == pg.KEYUP:
                if event.key == pg.K_z:
                    self.player.jump_cut()

        # if player righcest left 1/2 Scroll Right
        if self.player.rect.right >= WIDTH/2 and self.player.vel.x >0:
            self.player.pos.x += -self.player.vel.x
            for play in self.platforms:
                play.rect.right += -self.player.vel.x

    def draw(self):
        # Game Loop - draw

        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score),22, WHITE,20, 20)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        pass

    def show_go_screen(self):
        # game over/continue
        pass

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()