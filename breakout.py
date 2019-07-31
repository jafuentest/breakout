# import the pygame module, so you can use it
import pygame
import math

WHITE = (255, 255, 255)
BLUE = (0, 0, 255, 120)
BLACK = (0, 0, 0)

class Ball(object):
    """docstring for Ball"""
    def __init__(self, puck):
        super(Ball, self).__init__()
        self.puck = puck
        self.x = 400
        self.y = 600
        self.direction_x = 0
        self.direction_y = -0.5

    def move(self):
        if self.x < 0 or self.x > 800:
            self.direction_x *= -1
        if self.y < 0 or self.y > 600:
            self.direction_y *= -1
        # print (f"ball <= puck @ {self.getRect().bottom <= self.puck.getRect().top}")

        was_hit_by_puck = self.getRect().colliderect(self.puck.getRect())
        was_hit_with_the_top_of_puck = self.getRect().bottom - 1 <= self.puck.getRect().top
        if was_hit_by_puck and was_hit_with_the_top_of_puck:
            # print (f"mouse @ {self.getRect().bottom} {self.puck.getRect().top}")
            self.direction_x = self.puck.getSpeedX() / 2
            self.direction_y *= -1

        self.x += self.direction_x
        self.y += self.direction_y

    def draw(self, screen):
        self.move()
        pygame.draw.rect(screen, BLACK, self.getRect())

    def getRect(self):
        return pygame.Rect(self.x, self.y, 10, 10)

    def setSpeed(self, speed_x):
        self.direction_x = speed_x


class Puck(object):
    """docstring for Puck"""
    def __init__(self):
        super(Puck, self).__init__()
        self.x = 0
        self.y = 500
        self.speed_x = 0
        self.speed_y = 0

    def move(self, mouse):
        # if y < 500:
        #     y = 500

        self.x = pygame.mouse.get_pos()[0]
        # self.y = y

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, self.getRect())

    def getRect(self):
        return pygame.Rect(self.x, self.y, 150, 50)

    def updateSpeed(self):
        current_mouse_velocity = pygame.mouse.get_rel()
        # max_speed = abs(max(current_mouse_velocity, key=abs))
        max_speed = current_mouse_velocity[0]
        print (f"mouse @ {max_speed}")

        if max_speed == 0:
            self.speed_x = 0
        else:
            self.speed_x = current_mouse_velocity[0] / max_speed

    def getSpeedX(self):
        return self.speed_x

# define a main function
def main():
    pygame.init()
    pygame.display.set_caption('Breakout')

    screen = pygame.display.set_mode((800,600), 0, 32)

    running = True
    started = True
    # started = False

    screen.fill(WHITE)
    pygame.display.update()

    puck = Puck()
    ball = Ball(puck)

    while running:
        screen.fill(WHITE)
        ball.draw(screen)
        puck.draw(screen)

        for event in pygame.event.get():
            # Stop running when the user clicks close window button
            if event.type == pygame.QUIT:
                running = False

            # if not started and event.type == pygame.MOUSEMOTION:
            #     mouse_position = pygame.mouse.get_pos()
            #     if mouse_position[0] < 10 and mouse_position[1] < 10:
            #         started = True

            if not started:
                continue

            # React to the user moving the mouse
            if event.type == pygame.MOUSEMOTION:
                mouse_position = pygame.mouse.get_pos()
                puck.updateSpeed()

                # puck.move(mouse_position[0], mouse_position[1])
                # print (f"mouse @ {pygame.mouse.get_pos()}")
                puck.move(pygame.mouse)

        pygame.display.update()

if __name__ == '__main__':
    # call the main function
    main()
