from pygame import *
from random import *
from config import *

init()
font.init()
mixer.init()

# parametros iniciales
vidas = 5
puntos = 0
fallos = 0 # VARIABLE GLOBAL

# SONIDOS
# Musica de fondo
mixer.music.load(BGM)
mixer.music.play()

laser_sfx = mixer.Sound(FIRE_FX)

# clases
class GameSprite(sprite.Sprite):
    def __init__(self, sprite_img, cord_x, cord_y, sprite_width, sprite_height, speed):
        super().__init__()
        self.width = sprite_width
        self.height = sprite_height
        self.image = transform.scale(image.load(sprite_img), (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = cord_x
        self.rect.y = cord_y
        self.speed = speed

    def reset(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x >= 0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x <= ANCHO - self.width:
            self.rect.x += self.speed

    def fire(self):
        bala = Bullet(BULLET_IMG, self.rect.centerx - 5, self.rect.top, 10, 15, 5)
        balas.add(bala)
        laser_sfx.play()

class Enemy(GameSprite):
    def update(self):
        global fallos
        self.rect.y += self.speed
        if self.rect.y >= ALTO: # El enemigo cruza el borde inferior de la pantalla
            self.rect.y = -self.height
            self.rect.x = randint(0, ANCHO - 60)
            self.speed = randint(1, 6)
            fallos += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= -15:
            self.kill() # Remuevo la instancia del juego


# Objetos
window = display.set_mode((ANCHO, ALTO))
display.set_caption(TITULO)

# Trabajo con fuentes
font_1 = font.Font(GAME_FONT, 24)
font_2 = font.Font(GAME_FONT, 60)

player = Player(PLAYER_IMG, (ANCHO - 60) // 2, ALTO - 60, 60, 60, 5)
balas = sprite.Group()
aliens = sprite.Group()
asteroids = sprite.Group()

for i in range(5):
    enemy = Enemy(ENEMY_IMG, randint(0, ANCHO - 60), -60, 80, 60, randint(1, 6))
    aliens.add(enemy)

for i in range (3):
    rock = Enemy(ROCK_IMG, randint(0, ANCHO - 60), -40, 40, 40, randint(3, 7))
    asteroids.add(rock)

# fondo
background = transform.scale(image.load(BACKGROUND_IMG), (ANCHO, ALTO))

run = True
finish = False
clock = time.Clock()

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()

            if e.key == K_r:
                finish = False
                vidas = 5
                puntos = 0
                fallos = 0
        
    if not finish:
        window.fill(BACK_COLOR)
        window.blit(background, (0, 0))
        puntos_txt = font_1.render(f'PUNTOS: {puntos}', 1, WHITE)
        fallos_txt = font_1.render(f'FALLOS: {fallos}', 1, WHITE)
        vidas_txt = font_2.render(f'{vidas}', 1, GREEN)
        window.blit(puntos_txt, (40, 40))
        window.blit(fallos_txt, (40, 70))
        window.blit(vidas_txt, (550, 40))

        player.reset(window)
        player.update()
        aliens.draw(window)
        aliens.update()
        asteroids.draw(window)
        asteroids.update()
        balas.draw(window)
        balas.update()

        obst = sprite.groupcollide(balas, asteroids, True, False)

        collision = sprite.groupcollide(balas, aliens, True, True)
        for c in collision:
            puntos += 1
            enemy = Enemy(ENEMY_IMG, randint(0, ANCHO - 60), -60, 80, 60, randint(1, 6))
            aliens.add(enemy)

        if sprite.spritecollide(player, aliens, True):
            vidas -= 1
            enemy = Enemy(ENEMY_IMG, randint(0, ANCHO - 60), -60, 80, 60, randint(1, 6))
            aliens.add(enemy)

        # CONDICION DE DERROTA:
        if fallos >= 10 or vidas <= 0:
            finish = True
            window.fill(BLACK)
            game_over = transform.scale(image.load(GAMEOVER_IMG), (ANCHO, ALTO))
            window.blit(game_over, (0, 0))
            restart_txt = font_1.render(f'"R" para reiniciar!', 1, WHITE)
            window.blit(restart_txt, (180, 420))

        # CONDICION DE VICTORIA
        if puntos == 20:
            finish = True
            window.fill(WHITE)
            # RENDERIZAR IMAGEN DE VICTORIA


    if finish:
        mixer.music.stop()

    # NO TOCAR
    display.update()
    clock.tick(FPS)
quit()
