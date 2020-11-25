#1
import math, random, sys
import pygame as py
from pygame.locals import *
import sys
import os
import neat
import pickle
import numpy as np
from scipy.special import softmax
# from PyQt5 import QtWidgets


# define the colors

# db = nullEscDBClass()
# db.startGameCon()
py.init()
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 225)
green = (0, 225, 0)
red = (225, 0, 0)
colors = [green, red, blue]
newcolors = [(100,20,30), (60,10,10), (40,5,5)]

# define the size of the blocks

block_width = 46
block_height = 15



# wait for return to be pressed to start game
def pause():
    while True:
        events()
        k = py.key.get_pressed()
        if k[K_RETURN]:
            break


# exit the game
def events():
    for event in py.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            py.quit()
            sys.exit()


class Block(py.sprite.Sprite):
    """ this class respresent each block that gets knocked out"""
    def __init__(self, color, x, y):
        # call the parent sprite class constructor
        super().__init__()

        # make an image of block of appropriate size
        self.image = py.SurfaceType([block_width, block_height])

        # fill the image with the color
        self.image.fill(color)

        # fetch the retangle object demensions of the image
        self.rect = self.image.get_rect()

        # move the top left of the rectangle to x,y
        # where the block will appear
        self.rect.x = x
        self.rect.y = y


class Ball(py.sprite.Sprite):
    """ This class is for the ball """
    # speed of the pixels per cycle
    speed = 9.0

    # floating point representation of where the ball is
    x = 0.0
    y = 180.0

    # direction of ball ( in degrees )
    direction = 200
    width = 10
    height = 10

    # contructor
    def __init__(self):
        # call the parent class (sprite) constructor
        super().__init__()

        # create the image of the ball
        self.image = py.Surface((self.width, self.height), py.SRCALPHA)

        # color of the ball
        self.image.fill(white)

        # get a rectangle object that shows where our image is
        self.rect = self.image.get_rect()

        # getting the screen attributes for height/width
        self.screenheight = py.display.get_surface().get_height()
        self.screenwidth = py.display.get_surface().get_width()
        self.dx = 1
        self.dy = 1

    def bounce(self, diff):
        """This function will bounce the ball in the opposite direction"""

        # self.direction = (180 - self.direction) % 360
        # self.direction -= diff
        self.dy *= -1
        # self.dx *= -1

    def update(self):
        """Updating the position of the ball"""

        # convert into degrees
        direction_radians = math.radians(self.direction)

        # change the position of x and y according to speed and direction
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

        # move the image
        self.rect.x = self.x
        self.rect.y = self.y
        # print(self.x, self.y)

        # test if the ball bounced off the top
        if self.y <= 0:
            self.dy *= -1
            # self.bounce(0)
            # self.y = 1

        # test if the ball bounced off the left of the screen
        if self.x <= 0:
            self.dx *= -1
            # self.direction = (360 - self.direction) % 360
            # self.x = 1

        # test if the ball bounced off the right of the screen
        if self.x > self.screenwidth - self.width:
            self.dx *= -1
            # self.direction = (360 - self.direction) % 360
            # self.x = self.screenwidth - self.width - 1

        # test if the ball hit the bottom
        if self.y > 600:
            return True
        else:
            return False


# class UserMouse(py.sprite.Sprite):
#     """Represents the bar that the player will be moving with the mouse"""
#     def __init__(self):
#         # Call the parent's construtor
#         super().__init__()
#
#         self.width = 75
#         self.height = 15
#         self.image = py.Surface([self.width, self.height])
#         self.image.fill(white)
#
#         # make the top-left corner the pass in location
#         self.rect = self.image.get_rect()
#         self.screenheight = py.display.get_surface().get_height()
#         self.screenwidth = py.display.get_surface().get_width()
#
#         self.rect.x = 0
#         self.rect.y = self.screenheight - self.height
#
#     def update(self):
#         """Update the user pos"""
#         # get the user pos
#         pos = py.mouse.get_pos()
#         # set the left side of the user bar to the mouse position
#         self.rect.x = pos[0]
#         # make sure we don't push user off
#         if self.rect.x > self.screenwidth - self.width:
#             self.rect.x = self.screenwidth - self.width


class UserKey(py.sprite.Sprite):
    """Represents the bar that the player will be moving with the keys"""
    def __init__(self):
        # Call the parent's construtor
        super().__init__()

        self.velocity = 15
        self.width = 75
        self.height = 15
        self.image = py.Surface([self.width, self.height])
        self.image.fill(white)
        self.score = 0
        self.collision = 0
        self.dead = False

        # make the top-left corner the pass in location
        self.rect = self.image.get_rect()
        self.screenheight = py.display.get_surface().get_height()
        self.screenwidth = py.display.get_surface().get_width()

        self.rect.x = 0
        self.rect.y = self.screenheight - self.height

    def update(self):
        """Update the user pos"""
        # get the keys the the user presses
        move = py.key.get_pressed()

        # user moving left
        if move[K_LEFT]:
            self.rect.x -= self.velocity
        # user moving right
        elif move[K_RIGHT]:
            self.rect.x += self.velocity
        # if the user goes to far right
        if self.rect.x > self.screenwidth - self.width:
            self.rect.x = self.screenwidth - self.width

        # if the user goes to far left
        if self.rect.x < 0:
            self.rect.x = 0



SCORE = 0
GENERATION = 0
MAX_FITNESS = 0
BEST_GENOME = 0

# initialize pygame
py.init()

# create an 800X600 screen
screen = py.display.set_mode([800,600])

# set then title of the window
py.display.set_caption("Breakout")

# make the mouse disappear
py.mouse.set_visible(0)

# font for text
font = py.font.Font(None, 36)
# imagebg = py.image.load("SpaceBackground1.png")

# making the surface to draw on
background = py.Surface(screen.get_size())

def breakout(genome, config):
    net = pickle.load(open('breakoutAI.pickle', 'rb'))
    # net = neat.nn.FeedForwardNetwork.create(genome, config)

    global SCORE
    # screen.blits(imagebg)

    # creating sprite lists
    blocks = py.sprite.Group()
    balls = py.sprite.Group()
    allsprites = py.sprite.Group()

    # the top of the blocks (y position)
    top = 25

    # the numbers of blocks to make
    blockcount = 16

    # --- Create blocks
    # five rows of blocks
    for row in range(5):
        # 32 columns of blocks
        for column in range(0, blockcount):
            # create a block (color, x, y)
            block = Block(blue, column * (block_width + 2) + 10, top)
            blocks.add(block)
            allsprites.add(block)
        # move the top of the next row down
        top += block_height + 3




    # create the ball
    ball = Ball()
    ballStartX = random.randint(100, 200)
    ball.x = ballStartX
    allsprites.add(ball)
    balls.add(ball)

    # create the user paddle
    # user = UserMouse()
    user = UserKey()
    allsprites.add(user)

    # # score keeper
    # SCORE = 0

    # clock to limit speed
    clock = py.time.Clock()

    # is the game over?
    game_over = False

    # exit the game?
    exit_program = False

    # wait player to hit enter
    # pause()
    lastBallY = 0
    currentBallY = 1

    while not exit_program:

        events()

        # limit to 30 fps
        clock.tick(300)

        # clear the screen
        screen.fill(black)

        # input vaiables
        input = (user.rect.x, ball.rect.x, ball.rect.y, ballStartX)


        output = net.activate(input)
        output = softmax(np.asarray(output)).tolist()

        outputVAL = max(output)
        outputIndex = output.index(outputVAL)

        if outputIndex == 0:
            # move right
            user.rect.x += user.velocity
        elif outputIndex == 1:
            # move left
            user.rect.x -= user.velocity
        else:
            pass

        # update the ball
        if not game_over:
            user.update()
            # seeing it ball in game over state
            game_over = ball.update()



        # if game over
        if game_over:
            # allsprites.remove(ball)
            # balls.remove(ball)
            # fitness = SCORE
            # return fitness
            text = font.render("Game Over: Your Score was " + str(user.score), True, red)
            exit_program = True
            textpos = text.get_rect(centerx = background.get_width()/2)
            textpos.top = 300
            screen.blit(text, textpos)

        # see if the ball hits the paddle
        if py.sprite.spritecollide(user, balls, False):
            """the 'diff' lets you try to bounce the ball left or right
                depending where on the paddle you hit it"""
            diff = (user.rect.x + user.width/2) - (ball.rect.x + ball.width/2)

            """ set the balls y pos in case we hit the ball on
                the edge of the paddle"""
            ball.rect.y = screen.get_height() - user.rect.height - ball.rect.height - 1

            if lastBallY == currentBallY:
                ball.bounce(0)
            else:
                ball.bounce(diff)

        # check if collisions  between ball and blocks
        goneBlocks = py.sprite.spritecollide(ball, blocks, True)

        # if we hit a block, bounce the ball
        if len(goneBlocks) > 0:
            ball.bounce(0)
            SCORE += 1

            # game ends if all the blocks are gone
            if len(blocks) == 0:
                game_over = True




        # draw everything
        allsprites.draw(screen)

        # flip the screen and show is drawn
        py.display.flip()

        lastBallY = currentBallY
        currentBallY = ball.rect.y
    return SCORE, net


# inputs: left and right position of the ball
# outputs: left or right
# activation function: Use TanH at 0.5 as mid (can change)
# population size: start with 10
# fitness button: if the ball with the biggest score

#
# def eval_genomes(genomes, config):
#     i = 0
#     global SCORE
#     global GENERATION, MAX_FITNESS, BEST_GENOME
#
#     GENERATION += 1
#     for genome_id, genome in genomes:
#
#         genome.fitness = breakout(genome, config)
#         print("Gen : %d Genome # : %d  Fitness : %f Max Fitness : %f" % (GENERATION, i, genome.fitness, MAX_FITNESS))
#         if genome.fitness >= MAX_FITNESS:
#             MAX_FITNESS = genome.fitness
#             BEST_GENOME = genome
#         SCORE = 0
#         i += 1


# def run(config_path):
#     config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
#                          neat.DefaultSpeciesSet, neat.DefaultStagnation,
#                          config_path)
#
#     # generate population
#     p = neat.Population(config)
#     p.add_reporter(neat.StdOutReporter(True))
#     stats = neat.StatisticsReporter()
#     p.add_reporter(stats)
#
#     winner = p.run(eval_genomes, 50)
#     pickle.dump(winner, open("../../machine_learning/breakoutAI.pickle", "wb"))
#
#     print(winner)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    # run(config_path)

    genome = pickle.load(open('breakoutAI.pickle', 'rb'))

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                          neat.DefaultSpeciesSet, neat.DefaultStagnation,
                          'breakoutconfig-feedforward.txt')

    breakout(genome, config)
    # # db.saveScore("BreakOut ",x)
    # py.quit()
