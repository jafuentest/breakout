import pygame
import math

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREY = (100, 100, 100)

SCREEN_SIZE = (800, 600)

BALL_SIZE = [20, 20]
BALL_SPEED = 0.75

BRICK_SIZE = (40, 25)

PADDLE_SIZE = (170, 50)

DEGREE_NORMALIZATION_FACTOR = 20

class Brick(pygame.sprite.Sprite):
    """docstring for Brick"""
    def __init__(self, x, y):
        super(Brick, self).__init__()

        # Variables to draw the brick
        self.image = pygame.Surface(BRICK_SIZE)
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()

        inside_rect = [self.rect.x + 2, self.rect.y + 2, self.rect.w - 4, self.rect.h - 4]
        pygame.draw.rect(self.image, GREY, inside_rect)

        # Variables that make movement possible
        self.rect.x = x
        self.rect.y = y


class Ball(pygame.sprite.Sprite):
    """docstring for Ball"""
    def __init__(self, paddle, bricks):
        super(Ball, self).__init__()
        # Objects that the ball interacts with
        self.bricks = bricks
        self.paddle = paddle

        # Variables to draw the ball
        self.image = pygame.Surface(BALL_SIZE)
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()

        # Variables that make movement possible
        self.direction = math.radians(270)
        self.speed = BALL_SPEED
        self.rect.x = self.i = 400
        self.rect.y = self.j = 300

        pygame.draw.ellipse(self.image, (255,0,0), self.rect)

    def move(self):
        # If it hits a side of the screen, flip angle vertically
        if self.rect.x < 0 or self.rect.x > 800:
            self.direction = math.radians(180 - math.degrees(self.direction))

        # If it hits top/bottom of the screen, flip angle horizontally
        if self.rect.y < 0 or self.rect.y > SCREEN_SIZE[1]:
            self.direction = math.radians(360 - math.degrees(self.direction))

        self.check_paddle_collision()
        self.check_bricks_collision()

        # Set new position based on speed and angle
        self.i += self.speed * math.cos(self.direction)
        self.j -= self.speed * math.sin(self.direction)
        self.rect.x = self.i
        self.rect.y = self.j

    def check_bricks_collision(self):
        for brick in self.bricks:
            did_hit_brick = pygame.sprite.collide_rect(self, brick)
            from_top = self.rect.bottom - 1 <= self.paddle.rect.top

            # If did hit a brick go up mirror direction horizontally
            if did_hit_brick:
                brick.kill()
                self.direction = math.radians(360 - math.degrees(self.direction))

    def calculate_direction(self):
        max_angle = 180 - 2 * DEGREE_NORMALIZATION_FACTOR
        collision_area = PADDLE_SIZE[0] + BALL_SIZE[0]
        collision_x = self.rect.x - self.paddle.rect.x + BALL_SIZE[0]
        new_angle = collision_x * max_angle / collision_area + DEGREE_NORMALIZATION_FACTOR

        return new_angle

    def check_paddle_collision(self):
        was_hit = self.rect.colliderect(self.paddle.rect)
        with_the_top = self.rect.bottom - 1 <= self.paddle.rect.top

        # If hit by the paddle go up and apply angle depending on which part of
        # the paddle it was hit by
        if was_hit and with_the_top:
            new_angle = self.calculate_direction()

            self.direction = math.radians(180 - new_angle)


class Paddle(pygame.sprite.Sprite):
    """docstring for Paddle"""
    def __init__(self):
        super(Paddle, self).__init__()

        # Variables to draw the ball
        self.image = pygame.Surface(PADDLE_SIZE)
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()

        self.rect.x = 0
        self.rect.y = 500

    def set_x(self, x):
        if x > SCREEN_SIZE[0] - PADDLE_SIZE[0]:
            x = SCREEN_SIZE[0] - PADDLE_SIZE[0]
        self.rect.x = x


def generate_grid():
    rows = 3 * BRICK_SIZE[1]
    bricks = pygame.sprite.Group()
    for i in range(0, SCREEN_SIZE[0] - 1, BRICK_SIZE[0]):
        for j in range(0, rows - 1, BRICK_SIZE[1]):
            bricks.add(Brick(i, j))

    return bricks


def main():
    pygame.init()

    pygame.display.set_caption('Breakout')

    pygame.mouse.set_visible(0)

    screen = pygame.display.set_mode((800, SCREEN_SIZE[1]), 0, 32)

    running = True

    sprites = pygame.sprite.Group()

    paddle = Paddle()
    bricks = generate_grid()
    ball = Ball(paddle, bricks)

    sprites.add(bricks)
    sprites.add(ball)
    sprites.add(paddle)

    while running:
        screen.fill(WHITE)
        ball.move()
        sprites.draw(screen)

        for event in pygame.event.get():
            # Stop running when the user clicks close window button
            if event.type == pygame.QUIT:
                running = False

            # React to the user moving the mouse
            if event.type == pygame.MOUSEMOTION:
                mouse_position = pygame.mouse.get_pos()
                paddle.set_x(mouse_position[0])

        pygame.display.update()

if __name__ == '__main__':
    main()
