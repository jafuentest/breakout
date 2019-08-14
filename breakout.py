import pygame
import math

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREY = (100, 100, 100)

BALL_SIZE = [20, 20]
BALL_SPEED = 0.75

BRICK_SIZE = (40, 20)

SCREEN_SIZE = (BRICK_SIZE[0]*14, BRICK_SIZE[1]*8*5)

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
        self.direction = 270
        self.speed = BALL_SPEED
        # rect.x/y are treated as int, i/j on the other hand, we can treat as floats
        self.rect.x = self.i = 400
        self.rect.y = self.j = 300

        pygame.draw.ellipse(self.image, (255,0,0), self.rect)

    def move(self):
        # If it hits a side of the screen, flip angle vertically
        if self.rect.x < 0 or self.rect.x > SCREEN_SIZE[0] - BALL_SIZE[0]:
            self.direction = 180 - self.direction % 360

        # If it hits top/bottom of the screen, flip angle horizontally
        if self.rect.y < 0 or self.rect.y > SCREEN_SIZE[1]:
            self.direction = 360 - self.direction % 360

        self.check_paddle_collision()
        self.check_bricks_collision()

        # Set new position based on speed and angle
        self.i += self.speed * math.cos(math.radians(self.direction))
        self.j -= self.speed * math.sin(math.radians(self.direction))
        self.rect.x = self.i
        self.rect.y = self.j

    def distance_h(self, y, p):
        return math.hypot(p[0], p[1] - y)

    def distance_v(self, x, p):
        return math.hypot(p[0] - x, p[1])

    def get_brick_collision_side(self, brick):
        if self.direction == 90:
            return 'bottom'

        distances = {}

        if self.direction >= 270:
            distances['top'] = abs(brick.rect.top - self.rect.y)
            distances['left'] = abs(brick.rect.left - self.rect.x)
        elif self.direction >= 180:
            distances['top'] = abs(brick.rect.top - self.rect.y)
            distances['right'] = abs(brick.rect.right - self.rect.x)
        elif self.direction >= 90:
            distances['bottom'] = abs(brick.rect.bottom - self.rect.y)
            distances['right'] = abs(brick.rect.right - self.rect.x)
        else:
            distances['bottom'] = abs(brick.rect.bottom - self.rect.y)
            distances['left'] = abs(brick.rect.left - self.rect.x)

        return min(distances, key=distances.get)


    def check_bricks_collision(self):
        for brick in self.bricks:
            collided = pygame.sprite.collide_rect(self, brick)

            if not collided:
                continue

            collided_side = self.get_brick_collision_side(brick)

            brick.kill()
            if collided_side == 'left' or collided_side == 'right':
                self.direction = 180 - self.direction % 360
            else:
                self.direction = 360 - self.direction % 360

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

            self.direction = 180 - new_angle % 360


class Paddle(pygame.sprite.Sprite):
    """docstring for Paddle"""
    def __init__(self):
        super(Paddle, self).__init__()

        # Variables to draw the ball
        self.image = pygame.Surface(PADDLE_SIZE)
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()

        self.rect.x = 0
        self.rect.y = SCREEN_SIZE[1] - PADDLE_SIZE[1]

    def set_x(self, x):
        if x > SCREEN_SIZE[0] - PADDLE_SIZE[0]:
            x = SCREEN_SIZE[0] - PADDLE_SIZE[0]
        self.rect.x = x


def generate_grid():
    rows = 8 * BRICK_SIZE[1]
    cols = 14 * BRICK_SIZE[0]
    bricks = pygame.sprite.Group()
    for i in range(0, cols - 1, BRICK_SIZE[0]):
        for j in range(rows, rows * 2 - 1, BRICK_SIZE[1]):
            bricks.add(Brick(i, j))

    return bricks

def main():
    pygame.init()

    pygame.display.set_caption('Breakout')

    pygame.mouse.set_visible(0)

    screen = pygame.display.set_mode((SCREEN_SIZE[0], SCREEN_SIZE[1]), 0, 32)

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
