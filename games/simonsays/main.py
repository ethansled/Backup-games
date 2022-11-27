import pygame, random, time, sys, asyncio
from pygame.locals import *

# Window settings
WINHEIGHT = 500
WINWIDTH = 900
FLASHSPEED = 500 # in ms
FLASHDELAY = 200 # in ms
BUTTONSIZE = 200
BUTTONGAPSIZE = 25
TIMEOUT = 4 #times out if not pressed for 4 secs
FPS = 30
XMARGIN = int((WINWIDTH - (2 * BUTTONSIZE) - BUTTONGAPSIZE) / 2)
YMARGIN = int((WINHEIGHT - (2 * BUTTONSIZE) - BUTTONGAPSIZE) / 2)

# RGB colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (155, 0, 0)
GREEN = (0, 155, 0)
BLUE = (0, 0, 155)
YELLOW = (155, 155, 0)
BRIGHTRED = (255, 0, 0)
BRIGHTGREEN = (0, 255, 0)
BRIGHTBLUE = (0, 0, 255)
BRIGHTYELLOW = (255, 255, 0)
bgColor = BLACK


# formatting for each rectangle/color tile
YELLOWRECT = pygame.Rect(XMARGIN, YMARGIN, BUTTONSIZE, BUTTONSIZE)
BLUERECT = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE, YMARGIN, BUTTONSIZE, BUTTONSIZE)
REDRECT = pygame.Rect(XMARGIN, YMARGIN + BUTTONSIZE + BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)
GREENRECT = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE, YMARGIN + BUTTONSIZE + BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)

pygame.font.init()
FONT = pygame.font.SysFont("monospace", 16)

# game sounds
pygame.mixer.init()
SOUND1 = pygame.mixer.Sound("sound1.ogg")
SOUND2 = pygame.mixer.Sound("sound2.ogg")
SOUND3 = pygame.mixer.Sound("sound3.ogg")
SOUND4 = pygame.mixer.Sound("sound4.ogg")
SOUND5 = pygame.mixer.Sound("sound5.ogg")

pygame.init()
DIS = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
FPSCLOCK = pygame.time.Clock()


async def main():
    global FPSCLOCK, DIS, FONT, SOUND1, SOUND2, SOUND3, SOUND4, SOUND5, WINWIDTH, WINHEIGHT, YELLOWRECT, BLUERECT, GREENRECT, REDRECT
    pygame.display.set_caption('Simon')

    # instructions, placed in top left
    infoWindow = FONT.render('Follow the pattern using Q, W, A, S keys OR click tiles.', 1, WHITE)
    infoRect = infoWindow.get_rect()


    pattern = [] # stores the color pattern in array
    currentStep = 0 # the color the player must push next
    lastClickTime = 0 # timestamp of the player's last button push
    score = 0
    waitingForInput = False # when false, pattern is playing. when true, waiting for button press

    while True: # MAIN GAME LOOP
        clickedButton = None # Button that was clicked (set to YELLOW, RED, GREEN, or BLUE)
        DIS.fill(bgColor)
        await drawButtons() #draws tiles on screen

        scoreSurf = FONT.render('Score: ' + str(score), 1, WHITE) # score, displayed in right corner
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (WINWIDTH - 100, 10)
        DIS.blit(scoreSurf, scoreRect)

        DIS.blit(infoWindow, infoRect)

        for event in pygame.event.get(): 
            # maps mouse clicks to key presses
                   
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                clickedButton = await getButtonClicked(mousex, mousey)
            elif event.type == KEYDOWN:
                if event.key == K_q:
                    clickedButton = YELLOW
                elif event.key == K_w:
                    clickedButton = BLUE
                elif event.key == K_a:
                    clickedButton = RED
                elif event.key == K_s:
                    clickedButton = GREEN

        if not waitingForInput:
            # play the pattern when not waiting for user 
            pygame.display.update()
            # pygame.time.wait(1000)
            pattern.append(random.choice((YELLOW, BLUE, RED, GREEN))) # randomly chooses next color tile
            for button in pattern:
                await flashButtonAnimation(button)
                pygame.time.wait(FLASHDELAY)
            waitingForInput = True
        else:
            # wait for the player to enter buttons
            if clickedButton and clickedButton == pattern[currentStep]:
                # pushed the correct button
                await flashButtonAnimation(clickedButton)
                currentStep += 1
                lastClickTime = time.time()
                
                if currentStep == len(pattern):
                    # pushed the last button in the pattern
                    score += 1
                    waitingForInput = False
                    currentStep = 0 # reset back to first step
            elif (clickedButton and clickedButton != pattern[currentStep]) or (currentStep != 0 and time.time() - TIMEOUT > lastClickTime):
                # pushed incorrect button or has timed out
                await gameOverAnimation()
                # reset the variables for a new game
                pattern = []
                currentStep = 0
                waitingForInput = False
                score =  0
                pygame.time.wait(1000)
                await asyncio.sleep(0)
        
        await asyncio.sleep(0)
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        
   
async def flashButtonAnimation(color, animationSpeed=50): # flashes button for pattern order
    global DIS, FPSCLOCK, YELLOWRECT, BLUERECT, REDRECT, GREENRECT
    if color == YELLOW:
        sound = SOUND1
        flashColor = BRIGHTYELLOW
        rectangle = YELLOWRECT
    elif color == BLUE:
        sound = SOUND2
        flashColor = BRIGHTBLUE
        rectangle = BLUERECT
    elif color == RED:
        sound = SOUND3
        flashColor = BRIGHTRED
        rectangle = REDRECT
    elif color == GREEN:
        sound = SOUND4
        flashColor = BRIGHTGREEN
        rectangle = GREENRECT

    originalSurf = DIS.copy()
    flashSurf = pygame.Surface((BUTTONSIZE, BUTTONSIZE))
    flashSurf = flashSurf.convert_alpha()
    r, g, b = flashColor
    sound.play()

    for start, end, step in ((0, 255, 1), (255, 0, -1)): # animation loop
        for alpha in range(start, end, animationSpeed * step):
            DIS.blit(originalSurf, (0, 0))
            flashSurf.fill((r, g, b, alpha))
            DIS.blit(flashSurf, rectangle.topleft)
            await asyncio.sleep(0)
            pygame.display.update()
            FPSCLOCK.tick(FPS)
    DIS.blit(originalSurf, (0, 0))
    return

async def drawButtons(): # draws tiles on screen
    global DIS, YELLOWRECT, BLUERECT, REDRECT, GREENRECT
    pygame.draw.rect(DIS, YELLOW, YELLOWRECT)
    pygame.draw.rect(DIS, BLUE, BLUERECT)
    pygame.draw.rect(DIS, RED, REDRECT)
    pygame.draw.rect(DIS, GREEN, GREENRECT)
    return

async def gameOverAnimation(color=WHITE, animationSpeed=50):
    global DIS, SOUND5
    # plays failure sound, then flashes background
    originalSurf = DIS.copy()
    flashSurf = pygame.Surface(DIS.get_size())
    flashSurf = flashSurf.convert_alpha()
    SOUND5.play()
    
    r, g, b = color
    for i in range(3): #do the flash 3 times
        for start, end, step in ((0, 255, 1), (255, 0, -1)):
            # The first iteration sets the loop to go from 0-255, second 255-0
            for alpha in range(start, end, animationSpeed * step):
                # alpha means transparency. 255 is opaque, 0 is invisible
                flashSurf.fill((r, g, b, alpha))
                DIS.blit(originalSurf, (0, 0))
                DIS.blit(flashSurf, (0,0))
                await drawButtons()
                pygame.display.update()
                FPSCLOCK.tick(FPS)
                await asyncio.sleep(0)
    return

async def getButtonClicked(x, y): # allows users to click squares instead
    global YELLOWRECT, BLUERECT, REDRECT, GREENRECT
    if YELLOWRECT.collidepoint((x, y)):
        return YELLOW
    elif BLUERECT.collidepoint((x,y)):
        return BLUE
    elif REDRECT.collidepoint((x,y)):
        return RED
    elif GREENRECT.collidepoint((x, y)):
        return GREEN
    return None

asyncio.run(main())