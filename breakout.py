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

PUCK_SIZE = (170, 50)


class Brick(object):
    """docstring for Brick"""
    def __init__(self, i, j):
        super(Brick, self).__init__()
        self.i = i
        self.j = j

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.getRect())
        pygame.draw.rect(screen, GREY, self.getInsideRect())

    def getInsideRect(self):
        return pygame.Rect(self.i + 2, self.j + 2, BRICK_SIZE[0] - 4, BRICK_SIZE[1] - 4)

    def getRect(self):
        return pygame.Rect(self.i, self.j, BRICK_SIZE[0], BRICK_SIZE[1])


class Ball(object):
    """docstring for Ball"""
    def __init__(self, puck, bricks):
        super(Ball, self).__init__()
        self.bricks = bricks
        self.puck = puck
        self.direction = math.radians(270)
        self.speed = BALL_SPEED
        self.i = 400
        self.j = 300

    def getRect(self):
        return pygame.Rect((self.i, self.j), BALL_SIZE)

    def move(self):
        # If it hits a side of the screen, flip angle vertically
        if self.i < 0 or self.i > 800:
            self.direction = math.radians(180 - math.degrees(self.direction))

        # If it hits top/bottom of the screen, flip angle horizontally
        if self.j < 0 or self.j > SCREEN_SIZE[1]:
            self.direction = math.radians(360 - math.degrees(self.direction))

        self.check_puck_collision()
        self.check_bricks_collision()

        # Set new position based on speed and angle
        self.i += self.speed * math.cos(self.direction)
        self.j -= self.speed * math.sin(self.direction)

    def check_bricks_collision(self):
        for brick in self.bricks:
            did_hit_brick = self.getRect().colliderect(brick.getRect())

            # If did hit a brick go up mirror direction horizontally
            if did_hit_brick:
                print (f"collision @ { self.i } { self.j }")
                self.bricks.remove(brick)
                self.direction = math.radians(360 - math.degrees(self.direction))

    def check_puck_collision(self):
        was_hit = self.getRect().colliderect(self.puck.getRect())
        with_the_top = self.getRect().bottom - 1 <= self.puck.getRect().top

        # If hit by the puck go up and apply angle depending on which part of
        # the puck it was hit by
        if was_hit and with_the_top:
            collision_x = self.i - self.puck.get_i() + BALL_SIZE[0]
            collision_x *= PUCK_SIZE[0] / 180
            self.direction = math.radians(180 - collision_x)
            print (f"collision degrees: { collision_x }, new direction: { 180 - collision_x }")

    def draw(self, screen):
        self.move()
        pygame.draw.rect(screen, BLACK, self.getRect())


class Puck(object):
    """docstring for Puck"""
    def __init__(self):
        super(Puck, self).__init__()
        self.i = 0
        self.j = 500

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, self.getRect())

    def getRect(self):
        return pygame.Rect(self.i, self.j, PUCK_SIZE[0], 50)

    def get_i(self):
        return self.i

    def set_i(self, i):
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
                puck.set_i(mouse_position[0])

        pygame.display.update()

if __name__ == '__main__':
    main()
