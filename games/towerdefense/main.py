from operator import truediv
import pygame
import sys
import os
import time

print("Goblin Defense By Thomas Thompson")
pygame.init()

win_width = 500
win_height = 500

win = pygame.display.set_mode((win_width,win_height))
bg_image = pygame.image.load("games/towerdefense/bg.png")
pygame.display.set_caption("Goblin Defense")
bg = pygame.transform.scale(bg_image, (500,500))
font = pygame.font.Font('freesansbold.ttf', 15)
gameFont = pygame.font.Font('freesansbold.ttf', 25)


#Sprite Images
stationary = pygame.image.load(os.path.join("games/towerdefense/Hero","standing.png"))
tower = pygame.image.load(os.path.join("games/towerdefense/Tower","Tower.png"))
bulletImg = pygame.transform.scale(pygame.image.load(os.path.join("games/towerdefense/Bullet","bullet.png")),(10,10))
cannon = pygame.image.load(os.path.join("games/towerdefense/Cannon","cannon.png")) 
pygame_icon = pygame.image.load('games/towerdefense/Hero/standing.png')
pygame.display.set_icon(pygame_icon)

left = [pygame.image.load(os.path.join("games/towerdefense/Hero","L1.png")),
pygame.image.load(os.path.join("games/towerdefense/Hero","L2.png")),
pygame.image.load(os.path.join("games/towerdefense/Hero","L3.png")),
pygame.image.load(os.path.join("games/towerdefense/Hero","L4.png")),
pygame.image.load(os.path.join("games/towerdefense/Hero","L5.png")),
pygame.image.load(os.path.join("games/towerdefense/Hero","L6.png")),
pygame.image.load(os.path.join("games/towerdefense/Hero","L7.png")),
pygame.image.load(os.path.join("games/towerdefense/Hero","L8.png")),
pygame.image.load(os.path.join("games/towerdefense/Hero","L9.png")),]

#Right Facing
right = [pygame.image.load(os.path.join("games/towerdefense/Hero","R1.png")),
pygame.image.load(os.path.join("games/towerdefense/Hero","R2.png")),
pygame.image.load(os.path.join("games/towerdefense/Hero","R3.png")),
pygame.image.load(os.path.join("games/towerdefense/Hero","R4.png")),
pygame.image.load(os.path.join("games/towerdefense/Hero","R5.png")),
pygame.image.load(os.path.join("games/towerdefense/Hero","R6.png")),
pygame.image.load(os.path.join("games/towerdefense/Hero","R7.png")),
pygame.image.load(os.path.join("games/towerdefense/Hero","R8.png")),
pygame.image.load(os.path.join("games/towerdefense/Hero","R9.png")),]

#enemy animations
left_enemy = [pygame.image.load(os.path.join("games/towerdefense/Enemy", "L1E.png")),
pygame.image.load(os.path.join("games/towerdefense/Enemy", "L2E.png")),
pygame.image.load(os.path.join("games/towerdefense/Enemy", "L3E.png")),
pygame.image.load(os.path.join("games/towerdefense/Enemy", "L4E.png")),
pygame.image.load(os.path.join("games/towerdefense/Enemy", "L5E.png")),
pygame.image.load(os.path.join("games/towerdefense/Enemy", "L6E.png")),
pygame.image.load(os.path.join("games/towerdefense/Enemy", "L7E.png")),
pygame.image.load(os.path.join("games/towerdefense/Enemy", "L8E.png")),
pygame.image.load(os.path.join("games/towerdefense/Enemy", "L9P.png")),
pygame.image.load(os.path.join("games/towerdefense/Enemy", "L10P.png")),
pygame.image.load(os.path.join("games/towerdefense/Enemy", "L11P.png"))
        ]
right_enemy = [pygame.image.load(os.path.join("games/towerdefense/Enemy", "R1E.png")),
pygame.image.load(os.path.join("games/towerdefense/Enemy", "R2E.png")),
pygame.image.load(os.path.join("games/towerdefense/Enemy", "R3E.png")),
pygame.image.load(os.path.join("games/towerdefense/Enemy", "R4E.png")),
pygame.image.load(os.path.join("games/towerdefense/Enemy", "R5E.png")),
pygame.image.load(os.path.join("games/towerdefense/Enemy", "R6E.png")),
pygame.image.load(os.path.join("games/towerdefense/Enemy", "R7E.png")),
pygame.image.load(os.path.join("games/towerdefense/Enemy", "R8E.png")),
pygame.image.load(os.path.join("games/towerdefense/Enemy", "R9P.png")),
pygame.image.load(os.path.join("games/towerdefense/Enemy", "R10P.png")),
pygame.image.load(os.path.join("games/towerdefense/Enemy", "R11P.png"))
        ]
kills = 0
def game_over():
    #Text
    game_over_text = gameFont.render('Game Over', True, (255, 0 , 0))
    score_text = font.render('Score: ' + str(player.score), True, (0, 255, 0))
    kill_count = font.render('Kills: ' + str(player.kills), True, (0, 255, 0))
    win.fill((0,0,0))
    win.blit(game_over_text, (175, 220))
    win.blit(score_text, (win_width/2 - (score_text.get_width()/2),(win_height/2+score_text.get_height()*1.5)))
    win.blit(kill_count, (win_width/2 -(kill_count.get_width()/2),(win_height/2 + kill_count.get_height()*2.5)))
    
    pygame.display.update()
    time.sleep(5)
    reset_game()
def reset_game():
    player.score = 0
    player.kills = 0 
    player.lives = 2
    towerGame.lives = 2
    run = True
    player.alive = True
    player.x = 60
    player.y = 415
    for enemy in enemies:
        enemy.x = 450
        enemy.y = 415
        enemy.health = 30

    speed = 0.5


#def pause():
    #pause = True
    #while pause:
           ## for event in pygame.event.get():
            #    if event.type == pygame.QUIT():
            #        win.fill((0,0,0))
            #        pauseText = gameFont.render("Paused", True, (255,255,255))
             #       win.blit(pauseText, [20, 250])

#Tower Class
class Tower:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        #Tower Health
        self.hitbox = (self.x, self.y, 64, 128)
        self.health = 200
        self.max_health = self.health
        self.lives = 2
        self.alive = True
        self.stationary = True
    def draw(self, win):
        self.hitbox = (self.x + 15, self.y + 15,  30, 40)
       
        if self.stationary:
            win.blit(tower, (self.x, self.y))
        if self.health >= 0:
            pygame.draw.rect(win, (0, 255, 0), (140,0, self.health, 10))

#Cannon Class
class Cannon:
    def __init__(self, x,y):
        self.x = x
        self.y = y 
        self.face_right = True
        self.alive = True
        self.bullets = []
        self.cool_down_count = 0
        self.stationary = True
    def draw(self,win):
        if self.stationary:
            win.blit(cannon, (self.x, self.y))

    def shoot(self):
        self.hit()
        self.cooldown()
        if (userInput[pygame.K_z])and self.cool_down_count == 0:
            bullet = Bullet(self.x, self.y, self.direction())
            self.bullets.append(bullet)
            self.cool_down_count = 1
        for bullet in self.bullets:
            bullet.move()
            if bullet.off_screen():
                self.bullets.remove(bullet)
    
    def direction(self):
        if self.face_right:
            return 1
    
    def cooldown(self):
        if player.score >= 0:
            if self.cool_down_count >= 25:
                self.cool_down_count = 0
            elif self.cool_down_count > 0:
                self.cool_down_count += 1
        if player.score >= 200:
                if self.cool_down_count >= 15:
                    self.cool_down_count = 0
                elif self.cool_down_count > 0:
                    self.cool_down_count += 1
        if player.score >= 500:
                if self.cool_down_count >= 12:
                    self.cool_down_count = 0
                elif self.cool_down_count > 0:
                    self.cool_down_count += 1
        if player.score >= 10000:
            if self.cool_down_count >= 7:
                self.cool_down_count = 0
            elif self.cool_down_count > 0:
                self.cool_down_count += 1
    
    def hit(self):
        for enemy in enemies:
            for bullet in self.bullets:
                if enemy.hitbox[0] < bullet.x < enemy.hitbox[0] + enemy.hitbox[2] and enemy.hitbox[1] < bullet.y < \
                        enemy.hitbox[1] + enemy.hitbox[3]:
                    enemy.health -= 5
                    cannonGame.bullets.remove(bullet)
#Player Class
class Player:
    def __init__(self,x,y):
     #walk
        self.x = x
        self.y = y
        self.velx = 10
        self.vely = 6
        self.face_right = True
        self.face_right = True
        self.face_left = False
        self.stepIndex = 0
        #Jump
        self.jump = False
        #Bullets
        self.bullets = []
        self.cool_down_count = 0
        #health
        self.hitbox = (self.x, self.y, 64, 64)
        self.health = 30
        self.lives = 2
        self.alive = True
        self.score = 0
        self.kills = 0




    #functions
    def move_player(self, userInput):
        if userInput[pygame.K_RIGHT]:
            self.x += self.velx
            self.face_right = True
            self.face_left = False
        elif userInput[pygame.K_LEFT]:
            self.x -= self.velx
            self.face_right = False
            self.face_left = True
        else:
             self.stepIndex = 0

    def draw(self, win):
        self.hitbox = (self.x + 15, self.y + 15,  30, 40)
        pygame.draw.rect(win, (255, 0, 0), (self.x + 15, self.y, 30, 10))
        if self.stepIndex >= 9:
            self.stepIndex = 0
        if self.health >= 0:
            pygame.draw.rect(win, (0, 255, 0), (self.x + 15, self.y, self.health, 10))
        if self.face_left:
            win.blit(left[self.stepIndex], (self.x, self.y))
            self.stepIndex +=1
        elif self.face_right:
            win.blit(right[self.stepIndex],(self.x,self.y))
            self.stepIndex += 1
        else:
            win.blit(stationary,(self.x,self.y))

    def playerJump (self, userInput):
        if userInput[pygame.K_SPACE] and self.jump is False:
            self.jump = True
        if self.jump:
            self.y -= self.vely*4
            self.vely -=1
        if self.vely < -6:
            self.jump = False
            self.vely = 6

    def direction(self):
        if self.face_right:
            return 1
        if self.face_left:
            return -1
    
    def cooldown(self):
        if player.score >= 0:
            if self.cool_down_count >= 25:
                self.cool_down_count = 0
            elif self.cool_down_count > 0:
                self.cool_down_count += 1
        if player.score >= 200:
                if self.cool_down_count >= 15:
                    self.cool_down_count = 0
                elif self.cool_down_count > 0:
                    self.cool_down_count += 1
        if player.score >= 500:
                if self.cool_down_count >= 12:
                    self.cool_down_count = 0
                elif self.cool_down_count > 0:
                    self.cool_down_count += 1
        if player.score >= 10000:
            if self.cool_down_count >= 7:
                self.cool_down_count = 0
            elif self.cool_down_count > 0:
                self.cool_down_count += 1
        if player.score >= 2000:
            if self.cool_down_count >= 7:
                self.cool_down_count = 0
            elif self.cool_down_count > 0:
                self.cool_down_count += 1
    
    def shoot(self):
        self.hit()
        self.cooldown()
        if (userInput[pygame.K_z])and self.cool_down_count == 0:
            bullet = Bullet(self.x, self.y, self.direction())
            self.bullets.append(bullet)
            self.cool_down_count = 1
        for bullet in self.bullets:
            bullet.move()
            if bullet.off_screen():
                self.bullets.remove(bullet)


    def hit(self):
        for enemy in enemies:
            for bullet in self.bullets:
                if enemy.hitbox[0] < bullet.x < enemy.hitbox[0] + enemy.hitbox[2] and enemy.hitbox[1] < bullet.y < \
                        enemy.hitbox[1] + enemy.hitbox[3]:
                    enemy.health -= 5
                    player.bullets.remove(bullet)


#Bullet Class
class Bullet:
    def __init__(self, x, y, direction):
        self.x = x + 15
        self.y = y + 25
        self.direction = direction

    def draw_bullet(self):
        win.blit(bulletImg,(self.x,self.y))

    def move(self):
        if self.direction == 1:
            self.x += 15
        if self.direction == -1:
            self.x -= 15
        

    def off_screen(self):
        return not (self.x >=0 and self.x <= win_width)
#Enemy Class
class Enemy:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.stepIndex = 0
        #Enemy Health
        self.hitbox = (self.x, self.y, 64, 64)
        self.health = 30

    def step(self):
        if self.stepIndex >= 33:
            self.stepIndex = 0

    def draw(self, win):
        self.hitbox = (self.x + 20, self.y + 15, 30, 45)
        pygame.draw.rect(win, (255, 0, 0), (self.x + 15, self.y, 30, 10))
        if self.health >= 0:
            pygame.draw.rect(win, (0, 255, 0), (self.x + 15, self.y, self.health, 10))
        self.step()
        win.blit(left_enemy[self.stepIndex// 3], (self.x, self.y))
        self.stepIndex += 1


    def move(self):
        self.hit()
        self.x -= speed
    def hit(self):
        if player.hitbox[0] < enemy.x + 32 < player.hitbox[0] + player.hitbox[2] and player.hitbox[1] < enemy.y + 32 < \
            player.hitbox[1] + player.hitbox[3]:
            if player.health >= 0:
                player.health -= 1
                if player.health == 0 and player.lives > 0:
                    player.lives -= 1
                    player.health = 30
                elif player.health == 0 and player.lives == 0:
                    player.alive = False
        if towerGame.hitbox[0] < enemy.x + 32 < towerGame.hitbox[0] + towerGame.hitbox[2] and towerGame.hitbox[1] < enemy.y + 32 < \
            towerGame.hitbox[1] + towerGame.hitbox[3]:
            if towerGame.health >= 0:
                towerGame.health -= 1
                if towerGame.health == 0 and towerGame.lives > 0:
                    towerGame.lives -= 1
                    towerGame.health = 200
                elif towerGame.health == 0 and towerGame.lives == 0:
                    towerGame.alive = False

    def die (self):
        if enemy.health == 0:
            player.score += 50



    def off_screen(self):
        return not (self.x >= -1 and self.x <= win_width +1)



#Game function
def draw_game():
    win.fill((0, 0, 0))
    win.blit(bg,(0,0))
    #Draw Player and Tower
    player.draw(win)
    towerGame.draw(win)
    if player.score >= 1500:
        cannonGame.draw(win)
        
    for bullet in cannonGame.bullets:
        bullet.draw_bullet()
    #Draw Bullets
    for bullet in player.bullets:
        bullet.draw_bullet()
    #Draw Enemies
    for enemy in enemies:
        enemy.draw(win)
    #Gamer over argument
    if player.alive == False:
        game_over()

    text1 = font.render('Tower Health: ' + str(towerGame.health), True,(255,255,255))
    win.blit(text1, [0,0])
    text2 = font.render('Score: ' + str(player.score), True, (255,255,255))
    win.blit(text2, [400, 0])
    text3 = font.render('Kills: ' + str(player.kills), True, (255,255,255))
    win.blit(text3, [400, 20])



    pygame.time.delay(30)
    pygame.display.update()

#Player and Tower Instance
player = Player(60, 415)
towerGame = Tower(20, 370)
cannonGame = Cannon(150,415)

#Enemies
enemies = []
speed = 0.5

run = True
#Loop that runs the game and updates display
while run:

    #Quit game
    for event in pygame.event.get():...
    #input
    userInput = pygame.key.get_pressed()

        

    if event.type == pygame.QUIT:
        run = False

    player.shoot()
    if player.score >= 1500:
        cannonGame.shoot()
    #movement
    player.move_player(userInput)
    player.playerJump(userInput)
    if player.lives == 0:
        player.alive = False

    if towerGame.lives == 0:
        player.alive = False
    

    #enemies
    if len(enemies) == 0:
        enemy = Enemy(450,415, speed)
        enemies.append(enemy)
    
        if speed <= 10:
            speed += 0.25
    for enemy in enemies:
        enemy.move()
        if enemy.off_screen() or enemy.health == 0:
            enemies.remove(enemy)
            enemy.die()
        if enemy.x < 20:
            enemies.remove(enemy)
            towerGame.health -= 10
            if player.kills == 20:
                towerGame.health -= 20
        
    if towerGame.health == 0 and towerGame.lives > 0 :
        towerGame.lives -=1 
        towerGame.health = 200


    if enemy.health == 0:
        player.kills +=1

    print("tower: " + str(towerGame.lives))
    print("Player: " + str(player.lives))

    draw_game()
print("Player Score: " + str(player.score))



