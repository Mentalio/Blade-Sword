import pygame
import math
import json

pygame.mixer.init()

yippe = pygame.mixer.Sound("yippe.mp3")
yippe.set_volume(2)
death = pygame.mixer.Sound("oof.mp3")
death.set_volume(1)

p1_name = input('What is player ones name:\n')
p2_name = input('What is player twos name:\n')
p3_name = input('What is player threes name:\n')

pygame.init()
font_sml = pygame.font.Font('freesansbold.ttf', 16)
font = pygame.font.Font('freesansbold.ttf', 32)
font_lrg = pygame.font.Font('freesansbold.ttf', 96)

display_height = 1300
display_width = 800

standard_vel = 0.3
icon = pygame.image.load('sword.png')

screen = pygame.display.set_mode([display_height, display_width])
pygame.display.set_caption('Blade of the Sword')
pygame.display.set_icon(icon)

clock = pygame.time.Clock()
running = True

def rotate_to(target, current):
    diff = (target - current) % 360
    if diff == 0: return current
    if diff <= 180:
        current += 10
    else:
        current -= 10
    return current

def newimg(position:list, img_name:str, return_img:bool, scale:int, rotation:int):
    img = pygame.image.load(img_name)
    img = pygame.transform.scale_by(img, scale)
    img = pygame.transform.rotate(img, rotation)
    position = centre(position, img)
    if return_img == True:
        return img
    if return_img == False:
        return position
    
def orbit(centre:list, radius:int, rotation:int, offset:int):
    rotation = math.radians(rotation + offset)
    orbit = [centre[0] + radius * math.cos(rotation), centre[1] + radius * math.sin(rotation)]
    return orbit

def centre(position:list, size):
    if isinstance(size, list):
        offsetx = size[0] / 2
        offsety = size[1] / 2
    else:
        offset = size.get_rect()
        offsetx = offset[2] / 2
        offsety = offset[3] / 2
    position[0] -= offsetx
    position[1] -= offsety
    return position

def newrect(position:list, size):
    position = centre(position, size)
    rect = pygame.rect.Rect(position, size)
    return rect

class player:
    def __init__(self, movement_type, name):
        self.aura_rot = 0
        self.pts = 0
        self.counter = 0
        self.position = [display_width / 2, display_height / 2]
        self.velocity = [0, 0]
        self.hammer_position = [self.position]
        self.movement_type = movement_type
        self.shield_rotate = 0
        self.disabled = False
        self.exploded = False
        self.current_shield_rotate = 0
        self.sword_rotate = self.current_shield_rotate
        self.current_sword_rotate = 0
        self.text = font
        self.text = font.render(name, True, (255, 0, 0))
        self.name = name
        self.standard_vel = 0.3
        if self.name == 'Mentos':
            self.standard_vel = 0.6
            self.text = font.render(name, True, (0, 255, 0))
        elif self.name == 'X2SWEATYCOUSINS':
            self.text = font.render(name, True, (255, 255, 0))
        elif self.name == 'IDK':
            self.text = font.render(name, True, (0, 0, 0))
        elif self.name == 'Marz':
            self.text = font.render(name, True, (255, 165, 0))

    def addvelocity(self, velocity:list):
        self.velocity = [sum(i) for i in zip(velocity, self.velocity)]

    def addposition(self):
        self.position = [sum(i) for i in zip(self.position, self.velocity)]

    def keys(self):
        keys = pygame.key.get_pressed()
        if self.movement_type == 1:
            if keys[pygame.K_a]:
                self.shield_rotate = 180
                self.sword_rotate = 180
                self.addvelocity([-self.standard_vel, 0])
            if keys[pygame.K_d]:
                self.shield_rotate = 0
                self.sword_rotate = 0
                self.addvelocity([self.standard_vel, 0])
            if keys[pygame.K_w]:
                self.shield_rotate = 270
                self.sword_rotate = 90
                self.addvelocity([0, -self.standard_vel])
            if keys[pygame.K_s]:
                self.shield_rotate = 90
                self.sword_rotate = 270
                self.addvelocity([0, self.standard_vel])
        elif self.movement_type == 2:
            if keys[pygame.K_j]:
                self.shield_rotate = 180
                self.sword_rotate = 180
                self.addvelocity([-self.standard_vel, 0])
            if keys[pygame.K_l]:
                self.shield_rotate = 0
                self.sword_rotate = 0
                self.addvelocity([self.standard_vel, 0])
            if keys[pygame.K_i]:
                self.shield_rotate = 270
                self.sword_rotate = 90
                self.addvelocity([0, -self.standard_vel])
            if keys[pygame.K_k]:
                self.shield_rotate = 90
                self.sword_rotate = 270
                self.addvelocity([0, self.standard_vel])
        elif self.movement_type == 3:
            if keys[pygame.K_LEFT]:
                self.shield_rotate = 180
                self.sword_rotate = 180
                self.addvelocity([-self.standard_vel, 0])
            if keys[pygame.K_RIGHT]:
                self.shield_rotate = 0
                self.sword_rotate = 0
                self.addvelocity([self.standard_vel, 0])
            if keys[pygame.K_UP]:
                self.shield_rotate = 270
                self.sword_rotate = 90
                self.addvelocity([0, -self.standard_vel])
            if keys[pygame.K_DOWN]:
                self.shield_rotate = 90
                self.sword_rotate = 270
                self.addvelocity([0, self.standard_vel])

    def update(self):
        if not self.name:
            self.explode()
            self.exploded = True
            self.disabled = True
            
        if self.disabled == False:
            self.current_shield_rotate = self.current_shield_rotate % 360
            self.sword_rotate = self.sword_rotate % 360
            self.keys()
            self.addposition()
            self.current_shield_rotate = rotate_to(self.shield_rotate, self.current_shield_rotate)
            self.current_sword_rotate = rotate_to(self.sword_rotate, self.current_sword_rotate)
            shield1 = orbit(self.position, 50, self.current_shield_rotate, 0)
            shield2 = orbit(self.position, 40, self.current_shield_rotate, 0)
            shield3 = orbit(self.position, 30, self.current_shield_rotate, 0)

            if self.name == 'Mentos':
                sword = newimg(orbit(self.position, 20, self.current_shield_rotate, 0), 'gr_sword.png', True, 3, self.current_sword_rotate - 45)
                sword_pos = newimg(orbit(self.position, 20, self.current_shield_rotate, 0), 'gr_sword.png', False, 3, self.current_sword_rotate - 45)
                self.aura_rot += 1
                self.aura_rot = self.aura_rot % 360
                aura_img1 = newimg([self.position[0], self.position[1]], 'aura.png', True, 2, self.aura_rot)
                aura_pos1 = newimg([self.position[0], self.position[1]], 'aura.png', False, 2, self.aura_rot)
                screen.blit(aura_img1, aura_pos1)
            elif self.name == 'X2SWEATYCOUSINS':
                sword = newimg(orbit(self.position, 20, self.current_shield_rotate, 0), 'ye_sword.png', True, 3, self.current_sword_rotate - 45)
                sword_pos = newimg(orbit(self.position, 20, self.current_shield_rotate, 0), 'ye_sword.png', False, 3, self.current_sword_rotate - 45)
            elif self.name == 'IDK':
                sword = newimg(orbit(self.position, 20, self.current_shield_rotate, 0), 'bl_sword.png', True, 3, self.current_sword_rotate - 45)
                sword_pos = newimg(orbit(self.position, 20, self.current_shield_rotate, 0), 'bl_sword.png', False, 3, self.current_sword_rotate - 45)
            else:
                sword = newimg(orbit(self.position, 20, self.current_shield_rotate, 0), 'sword.png', True, 3, self.current_sword_rotate - 45)
                sword_pos = newimg(orbit(self.position, 20, self.current_shield_rotate, 0), 'sword.png', False, 3, self.current_sword_rotate - 45)

            if self.name == 'Mentos':
                pygame.draw.circle(screen, (0, 255, 0), self.position, 10, 2)
            elif self.name == 'X2SWEATYCOUSINS':
                pygame.draw.circle(screen, (255, 255, 0), self.position, 10, 2)
            elif self.name == 'IDK':
                idk_img = pygame.image.load('IDK.png')
                idk_img = pygame.transform.scale(idk_img, [25, 25])
                screen.blit(idk_img, [self.position[0] - 12.5, self.position[1] - 12.5])
            elif self.name == 'Marz':
                marz_img = pygame.image.load('marz.png')
                marz_img = pygame.transform.scale(marz_img, [25, 25])
                screen.blit(marz_img, [self.position[0] - 12.5, self.position[1] - 12.5])
            else:
                pygame.draw.circle(screen, (255, 0, 0), self.position, 10, 2)
            screen.blit(sword, sword_pos)
            
                
            self.shield_rec1 = newrect(shield1, [15, 15])     
            self.shield_rec2 = newrect(shield2, [15, 15])    
            self.shield_rec3 = newrect(shield3, [15, 15])   
            self.player_rec = newrect([self.position[0], self.position[1]], [20, 20])

            if pygame.Rect.colliderect(self.shield_rec1, player1.player_rec):
                player1.disabled = True
            if pygame.Rect.colliderect(self.shield_rec1, player2.player_rec):
                player2.disabled = True
            if pygame.Rect.colliderect(self.shield_rec1, player3.player_rec):
                player3.disabled = True
            if pygame.Rect.colliderect(self.shield_rec2, player1.player_rec):
                player1.disabled = True
            if pygame.Rect.colliderect(self.shield_rec2, player2.player_rec):
                player2.disabled = True
            if pygame.Rect.colliderect(self.shield_rec2, player3.player_rec):
                player3.disabled = True
            if pygame.Rect.colliderect(self.shield_rec3, player1.player_rec):
                player1.disabled = True
            if pygame.Rect.colliderect(self.shield_rec3, player2.player_rec):
                player2.disabled = True
            if pygame.Rect.colliderect(self.shield_rec3, player3.player_rec):
                player3.disabled = True    

            if self.position[0] > display_height:
                self.velocity[0] = -1
            if self.position[0] < 0:
                self.velocity[0] = 1
            if self.position[1] > display_width:
                self.velocity[1] = -1
            if self.position[1] < 0:
                self.velocity[1] = 1

            text_rect = self.text.get_rect()
            screen.blit(self.text, (self.position[0] - text_rect[2] / 2, self.position[1] - text_rect[3] / 2 - 40))


        else:
            if self.exploded == False:
                self.explode()
                if self.counter == 10:
                    pygame.mixer.Sound.play(death)
    
    def explode(self):
        if self.counter == 80:
            self.exploded = True
        else:
            self.counter = self.counter + 10
            if self.name == 'Mentos':
                pygame.draw.circle(screen, (0, 255, 0), self.position, self.counter, 1)
            elif self.name == 'X2SWEATYCOUSINS':
                pygame.draw.circle(screen, (255, 255, 0), self.position, self.counter, 1)
            elif self.name == 'IDK':
                pygame.draw.circle(screen, (0, 0, 0), self.position, self.counter, 1)
            elif self.name == 'Marz':
                pygame.draw.circle(screen, (255, 165, 0), self.position, self.counter, 1)
            else:
                pygame.draw.circle(screen, (255, 0, 0), self.position, self.counter, 1)

player1 = player(int(1), p1_name)
player2 = player(int(2), p2_name)
player3 = player(int(3), p3_name)

player1.player_rec = newrect([1000, 1000], [10, 10])
player2.player_rec = newrect([1000, 1000], [10, 10])
player3.player_rec = newrect([1000, 1000], [10, 10])
player1.position = [(display_height / 6) * 1, display_width / 2]
player2.position = [(display_height / 6) * 3, display_width / 2]
player3.position = [(display_height / 6) * 5, display_width / 2]

reseting = 200
countdown = 200
winning = player1

while running:
    clock.tick(60)
    for event in pygame.event.get():   
        if event.type == pygame.QUIT:
            running = False
            
    screen.fill((20, 20, 20))  

    player1.update()
    player2.update()
    player3.update()

    if player1.disabled == True and player2.disabled == True:
        player1.position = [(display_height / 6) * 1, display_width / 2]
        player2.position = [(display_height / 6) * 3, display_width / 2]
        player3.position = [(display_height / 6) * 5, display_width / 2]
        player1.velocity = [0, 0]
        player2.velocity = [0, 0]
        player3.velocity = [0, 0]
        player1.counter = 0
        player2.counter = 0
        player3.counter = 0
        winning = player3
        player3.pts += 1
        reseting = 200
        pygame.mixer.Sound.play(yippe)

    if player2.disabled == True and player3.disabled == True:
        player1.position = [(display_height / 6) * 1, display_width / 2]
        player2.position = [(display_height / 6) * 3, display_width / 2]
        player3.position = [(display_height / 6) * 5, display_width / 2]
        player1.velocity = [0, 0]
        player2.velocity = [0, 0]
        player3.velocity = [0, 0]
        player1.counter = 0
        player2.counter = 0
        player3.counter = 0
        winning = player1
        player1.pts += 1
        reseting = 200
        pygame.mixer.Sound.play(yippe)

    if player1.disabled == True and player3.disabled == True:
        player1.position = [(display_height / 6) * 1, display_width / 2]
        player2.position = [(display_height / 6) * 3, display_width / 2]
        player3.position = [(display_height / 6) * 5, display_width / 2]
        player1.velocity = [0, 0]
        player2.velocity = [0, 0]
        player3.velocity = [0, 0]
        player1.counter = 0
        player2.counter = 0
        player3.counter = 0
        winning = player2
        player2.pts += 1
        reseting = 200
        pygame.mixer.Sound.play(yippe)

    if reseting > 0:
        reseting -= 1
        player1.disabled = False
        player2.disabled = False
        player3.disabled = False
        player1.exploded = False
        player2.exploded = False
        player3.exploded = False
        player1.position = [(display_width / 6) * 1, display_height / 2]
        player2.position = [(display_width / 6) * 3, display_height / 2]
        player3.position = [(display_width / 6) * 5, display_height / 2]
        player1.velocity = [0, 0]
        player2.velocity = [0, 0]
        player3.velocity = [0, 0]
        countdown = reseting / 60
        countdown = countdown.__round__(1)

    countdown_font = font_lrg.render(str(countdown), True, (255, 255, 255))
    countdown_font_pl = font.render('Player: ' + str(winning.name) + ' Has Won!', True, (255, 255, 255))
    player_1_scr = font_sml.render(str(player1.name) + "'s Points: " + str(player1.pts), True, (255, 255, 255))
    player_2_scr = font_sml.render(str(player2.name) + "'s Points: " + str(player2.pts), True, (255, 255, 255))
    player_3_scr = font_sml.render(str(player3.name) + "'s Points: " + str(player3.pts), True, (255, 255, 255))

    screen.blit(player_1_scr, [10 , 10])
    screen.blit(player_2_scr, [10 , 50])
    screen.blit(player_3_scr, [10 , 90])

    if countdown != 0:
        screen.blit(countdown_font, [(display_height / 2) - countdown_font.get_rect()[2] / 2, 10])
        screen.blit(countdown_font_pl, [(display_height / 2) - countdown_font_pl.get_rect()[2] / 2, 100])
        

    pygame.display.flip()


pygame.quit()