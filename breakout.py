import pygame
import math

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREY = (100, 100, 100)

SCREEN_SIZE = (800, 600)

BALL_SIZE = (10, 10)
BALL_SPEED = 0.75

BRICK_SIZE = (40, 25)


class Brick(object):
    """docstring for Brick"""
    def __init__(self, i, j):
        super(Brick, self).__init__()
        self.i = i
        self.j = j

    def draw(self, screen):
        pygame.draw.rect(screen, GREY, self.getRect())

    def getRect(self):
        return pygame.Rect(self.i + 2, self.j + 2, BRICK_SIZE[0] - 4, BRICK_SIZE[1] - 4)


class Ball(object):
    """docstring for Ball"""
    def __init__(self, puck, bricks):
        super(Ball, self).__init__()
        self.puck = puck
        self.direction = math.radians(270)
        self.speed = BALL_SPEED
        self.i = 400
        self.j = 300

    def move(self):
        # If it hits a side of the screen, flip angle vertically
        if self.i < 0 or self.i > 800:
            self.direction = math.radians(180 - math.degrees(self.direction))

        # If it hits top/bottom of the screen, flip angle horizontally
        if self.j < 0 or self.j > SCREEN_SIZE[1]:
            self.direction = math.radians(360 - math.degrees(self.direction))

        was_hit_by_puck = self.getRect().colliderect(self.puck.getRect())
        was_hit_with_the_top_of_puck = self.getRect().bottom - 1 <= self.puck.getRect().top

        # If hit by the puck go up and apply angle depending on which part of
        # the puck it was hit by
        if was_hit_by_puck and was_hit_with_the_top_of_puck:
            collision_x = self.i - self.puck.getX() + BALL_SIZE[0]
            collision_x *= 150 / 180
            self.direction = math.radians(180 - collision_x)
            print (f"mouse @ { collision_x }")

        # Set new position base on speed and angle
        self.i += self.speed * math.cos(self.direction)
        self.j -= self.speed * math.sin(self.direction)

    def draw(self, screen):
        self.move()
        pygame.draw.rect(screen, BLACK, self.getRect())

    def getRect(self):
        return pygame.Rect((self.i, self.j), BALL_SIZE)


class Puck(object):
    """docstring for Puck"""
    def __init__(self):
        super(Puck, self).__init__()
        self.i = 0
        self.j = 500

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, self.getRect())

    def getRect(self):
        return pygame.Rect(self.i, self.j, 170, 50)

    def getX(self):
        return self.i

    def setX(self, i):
        self.i = i


def generateGrid():
    rows = 3 * BRICK_SIZE[1]
    bricks = []
    for i in range(0, SCREEN_SIZE[0] - 1, BRICK_SIZE[0]):
        for j in range(0, rows - 1, BRICK_SIZE[1]):
            bricks.append(Brick(i, j))

    return bricks


def main():
    pygame.init()
    pygame.display.set_caption('Breakout')

    screen = pygame.display.set_mode((800, SCREEN_SIZE[1]), 0, 32)

    running = True

    puck = Puck()
    bricks = generateGrid()
    ball = Ball(puck, bricks)

    while running:
        screen.fill(WHITE)
        ball.draw(screen)
        puck.draw(screen)
        for brick in bricks:
            brick.draw(screen)

        for event in pygame.event.get():
            # Stop running when the user clicks close window button
            if event.type == pygame.QUIT:
                running = False

            # React to the user moving the mouse
            if event.type == pygame.MOUSEMOTION:
                mouse_position = pygame.mouse.get_pos()
                puck.setX(mouse_position[0])

        pygame.display.update()

if __name__ == '__main__':
    main()
