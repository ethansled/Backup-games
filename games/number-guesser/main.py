import asyncio
import random
import pygame

# porting this to pygame is still WIP but this is a decent template for your apps
# refer to https://github.com/pygame-web/pygbag/blob/main/README.md for explanation

ATTEMPTS = []
SCREEN = pygame.display.set_mode(1280, 720)


def show_score():
    if len(ATTEMPTS) <= 0:
        print("There is currently no high score, it's yours for the taking!")
    else:
        print("The current high score is {} attempts".format(min(len(ATTEMPTS))))

print("Hello traveler! Welcome to the game of guesses!")


async def main():
    global ATTEMPTS
    global SCREEN
    while True:
        random_number = int(random.randint(1, 10))
        try:
            guess = input("Pick a number between 1 and 10 ")
            if int(guess) < 1 or int(guess) > 10:
                raise ValueError(
                    "Please guess a number within the given range")
            if int(guess) == random_number:
                print("Nice! You got it!")
                attempts += 1
                ATTEMPTS.append(attempts)
                print("It took you {} attempts".format(attempts))
                play_again = input(
                    "Would you like to play again? (Enter Yes/No) ")
                attempts = 0
                show_score()
                random_number = int(random.randint(1, 10))
                if play_again.lower() == "no":
                    print("That's cool, have a good one!")
                    break
            elif int(guess) > random_number:
                print("It's lower")
                attempts += 1
            elif int(guess) < random_number:
                print("It's higher")
                attempts += 1
        except ValueError as err:
            print("Oh no!, that is not a valid value. Try again...")
            print("({})".format(err))
    
    pygame.display.flip()


asyncio.run(main())
