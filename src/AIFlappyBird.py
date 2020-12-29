if __name__ == "__main__":
    import pygame
    import os
    import random
    import pickle
    import neat

    pygame.init()

    width, height = 300, 540

    screen = pygame.display.set_mode((width, height))

    pygame.display.set_caption("Flappy Bird")
    bg_image = pygame.transform.scale(pygame.image.load("./bg.png"), (width, height))

    b_w, b_h = width // 10, height // 20
    bird_imgs = [pygame.transform.scale(pygame.image.load("./bird" + str(i) + ".png"), (b_w, b_h)) for i in range(1, 4)]

    pipe_img = pygame.image.load("./pipe.png")

    Clock = pygame.time.Clock()

    x = 40
    y = 40


    class Bg:
        def __init__(self):
            self.b1 = pygame.transform.scale(pygame.image.load("./bg.png"), (width, height))
            self.b2 = pygame.transform.scale(pygame.image.load("./bg.png"), (width, height))
            self.base1 = pygame.transform.scale(pygame.image.load("./base.png"), (width, height // 20))
            self.base2 = pygame.transform.scale(pygame.image.load("./base.png"), (width, height // 20))
            self.v = width // 80
            self.x = 0

        def show(self):
            screen.blit(self.b1, (self.x, 0))
            screen.blit(self.b2, (self.x + width, 0))
            _, h = self.base1.get_rect().size
            screen.blit(self.base1, (self.x, height - h))
            screen.blit(self.base2, (self.x + width, height - h))

        def move(self):
            self.x -= self.v
            if self.x <= -1 * width:
                self.x = 0

        def stop(self):
            self.v = 0


    class Bird(pygame.sprite.Sprite):
        IMGS = bird_imgs

        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.ALIVE_TIME = 0
            self.x, self.y = x, y
            self.tilt_angle = 0
            self.vy, self.vx, self.omega = 0, 0, 5
            self.g = 30
            self.dt = 0.1
            self.MAX_ANGLE, self.MIN_ANGLE = 45, -45
            self.start_time = self.ALIVE_TIME
            self.jump_vel = 65
            self.alive = True
            self.distance = 0
            self.mask = None
            self.image = None
            self.score = 0
            self.pipeCollision = False

        def show(self):
            Clock.tick(50)
            if self.tilt_angle <= self.MIN_ANGLE:
                img = 1
            else:
                img = self.ALIVE_TIME % 3

            rotated_image = pygame.transform.rotate(self.IMGS[img], self.tilt_angle)
            new_rect = rotated_image.get_rect(center=self.IMGS[img].get_rect(topleft=(self.x, self.y)).center)
            screen.blit(rotated_image, new_rect.topleft)

            self.mask = pygame.mask.from_surface(rotated_image)
            self.image = rotated_image

            if self.alive:
                self.ALIVE_TIME += 1
            else:
                self.tilt_angle = 0

        def click(self):
            if self.alive:
                self.vy = -1 * self.jump_vel
                self.tilt_angle = self.MAX_ANGLE

        def move(self):
            (self.x, self.y, self.vy, self.g)
            if self.alive:
                if not self.pipeCollision:
                    self.distance += 1
                    self.score += 3

                self.x += self.vx * self.dt
                self.y += self.dt * (self.vy + 0.5 * self.g * self.dt)
                self.vy = self.vy + self.g * self.dt
                self.tilt_angle -= self.omega * self.dt

            if self.tilt_angle <= self.MIN_ANGLE:
                self.tilt_angle = self.MIN_ANGLE

        def groundCollision(self):
            if self.y <= height - height // 20:
                return False
            else:
                self.alive = False
                return True

        def stop(self):
            self.vy = 0
            self.vx = 0

            self.ALIVE_TIME = -1

        def getx(self):
            return self.x

        def getime(self):
            return self.ALIVE_TIME


    class Pipes:
        def __init__(self, x):
            pygame.sprite.Sprite.__init__(self)
            self.x = x
            self.pipe_1 = pygame.transform.flip(pipe_img, False, True)
            self.pipe_2 = pipe_img
            self.v = width // 80
            self.space = height // 4
            self.y = height // 6 + random.randint(0, height - self.space - height // 20 - height // 6 - height // 9)
            self.top = self.y
            self.bottom = self.y + self.space

        def getx(self):
            return self.x

        def gety(self):
            return self.y, self.y + self.space

        def show(self):
            self.top = self.y

            self.pipe_1 = pygame.transform.scale(self.pipe_1, (int(b_w * (1.5)), self.y))
            screen.blit(self.pipe_1, (self.x, 0))
            yPos = height - self.space - self.y - height // 20

            self.bottom = self.y + self.space
            self.pipe_2 = pygame.transform.scale(self.pipe_2, (int(b_w * (1.5)), yPos))
            screen.blit(self.pipe_2, (self.x, self.y + self.space))

        def passed(self):
            if self.x >= -1 * b_w * 1.5:
                return False
            return True

        def move(self):
            self.x -= self.v

        def stop(self):
            self.v = 0


    def main():

        Nnets = pickle.load(open('FlappyBest.pickle', 'rb'))

        playing = True
        b = Bird(x, y)
        bg = Bg()
        DIST = 8 * width // 10
        pipes = [Pipes(5 * width), Pipes(5 * width + DIST)]
        score = None
        while playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:

                    pygame.quit()
                    playing = False

                if playing == False:
                    break


            activatedNodeVal = Nnets.activate((b.y, abs(b.y - pipes[0].top), abs(b.y - pipes[0].bottom)))

            if activatedNodeVal[0] > 0.5:
                b.click()

            font = pygame.font.SysFont("comicsans", 18)
            score = font.render('Score ' + str(b.score), True, (150, 150, 150), (255, 255, 255))

            bg.show()
            b.show()
            for p in pipes:
                p.show()
            screen.blit(score, (width - score.get_width() - 15, 10))

            b.move()
            bg.move()
            for p in pipes:
                p.move()

            if b.groundCollision():
                bg.stop()
                b.stop()

                for p in pipes:
                    p.stop()
                b.g = 0
                b.vy = 0
                b.y = 19 * height // 20 - b_h
                score = b.score

            for p in pipes:
                if (0 <= b.y <= p.y or p.y + p.space <= b.y <= height) and p.x <= b.x <= p.x + 1.5 * (b_w):
                    # print("collided")
                    bg.stop()
                    pipes[0].stop()
                    pipes[1].stop()
                    b.pipeCollision = True
                    b.vx = -5
                    b.vy = 100
                    break

            if pipes[0].passed():
                if not pipes[1].passed():
                    pipes[0], pipes[1] = pipes[1], Pipes(pipes[1].getx() + DIST)
                else:
                    pipes[0] = Pipes(b.getx() + width)
                    pipes[1] = Pipes(pipes[0].getx() + DIST)

            pygame.display.update()
        print(b.score)
        print("test")


    main()
