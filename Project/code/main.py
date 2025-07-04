import pygame
from os.path import join

import random

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('Project', 'images', 'player.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, size_adjusted_player)
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.direction = pygame.Vector2()
        self.speed = 300

        # cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surf, self.rect.midtop, all_sprites)
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.image = pygame.transform.scale(self.image, size_adjusted_star)
        self.rect = self.image.get_frect(center = (random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)))

class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.image = pygame.transform.scale(self.image, size_adjusted_laser)
        self.rect = self.image.get_frect(midbottom = pos)

    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.image = pygame.transform.scale(self.image, size_adjusted_meteor)
        self.rect = self.image.get_frect(center = pos)
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 3000
        self.direction = pygame.Vector2(random.uniform(-0.5, 0.5), 1)
        self.speed = random.randint(400, 500)

    def update(self, dt):
        self.rect.centery += 350 * dt
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()

# general setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Space Shooter')
running = True
clock = pygame.time.Clock()

width_star = 90
height_star = 90
size_adjusted_star = (width_star, height_star)

width_player = 100
height_player = 93
size_adjusted_player = (width_player, height_player)

width_meteor = 132
height_meteor = 132
size_adjusted_meteor = (width_meteor, height_meteor)

width_laser = 20
height_laser = 58
size_adjusted_laser = (width_laser, height_laser)

# import
star_surf = pygame.image.load(join('Project', 'images', 'star.png')).convert_alpha()
meteor_surf = pygame.image.load(join('Project', 'images', 'meteor.png')).convert_alpha()
laser_surf = pygame.image.load(join('Project', 'images', 'laser.png')).convert_alpha()

# sprites
all_sprites = pygame.sprite.Group()
for i in range(20):
    Star(all_sprites, star_surf)
player = Player(all_sprites)

# custo event -> meteor event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)

while running:
    dt = clock.tick() / 1000 # FPS  |  dt = delta time
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            x, y = random.randint(0, WINDOW_WIDTH), random.randint(-200, -100)
            Meteor(meteor_surf, (x, y), all_sprites)

    # update
    all_sprites.update(dt)

    # draw the game
    display_surface.fill('darkgray')
    all_sprites.draw(display_surface)
    pygame.display.update()

pygame.quit()





# codes:

# plain surface
# surf = pygame.Surface((100, 200))
# surf.fill('blue')
# x = 150

# imports
# player_surf = pygame.image.load('Project/images/player.png').convert_alpha()
# player_surf = pygame.transform.scale(player_surf, size_adjusted_player)
# player_rect = player_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
# player_direction = pygame.math.Vector2(0, 0)
# player_speed = 300

# star_surf = pygame.image.load('Project/images/star.png').convert_alpha()

# meteor_surf = pygame.image.load('Project/images/meteor.png').convert_alpha()
# meteor_rect = meteor_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

# laser_surf = pygame.transform.scale(laser_surf, size_adjusted_laser)
# laser_rect = laser_surf.get_frect(bottomleft = (20, WINDOW_HEIGHT - 20))

# for pos in star_position:
#     display_surface.blit(star_surf, pos)

# player movement
# if player_rect.bottom >= WINDOW_HEIGHT or player_rect.top <= 0:
#      player_direction.y *= -1
# if player_rect.right >= WINDOW_WIDTH or player_rect.left <= 0:
#      player_direction.x *= -1
# player_rect.center += player_direction * player_speed * dt

# if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
        #     print(1)
        # if event.type == pygame.MOUSEMOTION:
        #     player_rect.center = event.pos

    # display_surface.blit(laser_surf, laser_rect)
    # display_surface.blit(meteor_surf, meteor_rect)

# display_surface.blit(player_surf, player_rect)