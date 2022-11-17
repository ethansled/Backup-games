import pygame, random, asyncio

pygame.init()

# defines RGB values of colors to be used
green = (0, 255, 0)
brown = (79, 67, 1)

# Intended dimensions of window
dis_width = 900
dis_height = 500

# Sets name of window
pygame.display.set_caption('Snake')

# Dimensions of game window applied 
dis = pygame.display.set_mode((dis_width, dis_height))

# Controls game framerate
clock = pygame.time.Clock()

# Creates font used to keep score
myfont = pygame.font.SysFont("monospace", 16)

# Starts the game
def main():
    # x1 and y1 are the coordinates of the snake
    x1 = dis_width / 2
    y1 = dis_height / 2
    # dir is the direction the snake will move
    dir = [0, 0]
    # snake_list keeps track of the coordinates of the snake's body
    snake_list = []
    # snake_len will keep track of the snake's length
    snake_len = 1
    # foodx and foody represent where food will spawn
    foodx = 30
    foody = 30
    # initial score
    score = 0
    # beginning of main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # Moves snake according to direction arrows on keyboard
                if event.key == pygame.K_LEFT:
                    dir = [-10, 0]
                elif event.key == pygame.K_RIGHT:
                    dir = [10, 0]
                elif event.key == pygame.K_UP:
                    dir = [0, -10]
                elif event.key == pygame.K_DOWN:
                    dir = [0, 10]
                
        # This updates the direction of the keyboard 
        x1 += dir[0]
        y1 += dir[1]
        # Sets the surface (window) color to brown
        dis.fill(brown)
        
        # Snake shape
        pygame.draw.rect(dis, green, [foodx, foody, 10, 10])

        snake_list.append([x1, y1])
        if len(snake_list) > snake_len:
            del snake_list[0]

        # Resets game if snake hits itself
        if ([x1, y1] in snake_list[:-1]):
            # Resets scoreboard on impact
            score = 0
            main()  

        # Restarts the game if snake hits the window border
        if (x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0):
            # Resets score on impact
            score = 0
            main()

        # Draws additional snake piece 
        for x in snake_list:
            pygame.draw.rect(dis, green, [x[0], x[1], 10, 10])

        # If snake touches food, it adds new food to random spot and makes snake longer
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - 10) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - 10) / 10.0) * 10.0
            snake_len += 1
            # Score increases with each food eaten
            score += 1
            
        # Score counter text, placed in the top left area of window
        text = myfont.render("Score {0}".format(score), 1, (0, 0, 0))
        dis.blit(text, (5, 10))

        # updates content on screen
        pygame.display.update()
        # controls framerate/speed of game
        clock.tick(15)


if __name__ == '__main__':
    asyncio.run(main())


