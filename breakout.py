import pygame
import math

WHITE = (255, 255, 255)
GREY = (100, 100, 100)
BLACK = (30, 30, 30)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

BALL_SIZE = [20, 20]
BALL_SPEED = 5

BRICK_SIZE = (40, 20)

PADDLE_SIZE = (120, 20)

SCREEN_SIZE = (BRICK_SIZE[0] * 14, BRICK_SIZE[1] * 8 * 5)

DEGREE_NORMALIZATION_FACTOR = 20

class Brick(pygame.sprite.Sprite):
    """docstring for Brick"""
    def __init__(self, x, y):
        super(Brick, self).__init__()
        x = x + 2
        y = y + 2

        # Variables to draw the brick
        self.image = pygame.Surface((BRICK_SIZE[0] - 4, BRICK_SIZE[1] - 4))
        self.image.fill(GREY)
        self.rect = self.image.get_rect()

        # Variables that make movement possible
        self.rect.x = x
        self.rect.y = y

    def collide_points(self, points):
        for point in points:
            if self.rect.collidepoint(point):
                return True
        return False


class Player(pygame.sprite.Sprite):
    """docstring for Ball"""
    def __init__(self, paddle, bricks):
        super(Player, self).__init__()
        # Player
        self.lives = 3

        # Objects that the ball interacts with
        self.bricks = bricks
        self.paddle = paddle
        self.x = 400
        self.y = 600

        # Variables to draw the ball
        self.image = pygame.Surface(BALL_SIZE)
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        # Variables that make movement possible
        self.direction = 91
        self.speed = BALL_SPEED

        radius = int(BALL_SIZE[0] / 2)
        self.rect = pygame.draw.circle(self.image, RED, [radius, radius], radius)

    def move(self):
        # If it hits a side of the screen, flip angle vertically
        if self.rect.x < 0 or self.rect.x > SCREEN_SIZE[0] - BALL_SIZE[0]:
            self.direction = (540 - self.direction) % 360

        # If it hits top of the screen, flip angle horizontally
        if self.rect.y < 0:
            self.direction = 360 - self.direction

        # If it hits bottom of the screen, loose a life
        if self.rect.bottom > SCREEN_SIZE[1]:
            self.lives -= 1
            self.direction = 360 - self.direction

        self.check_paddle_collision()
        self.check_bricks_collision()

        # Set new position based on speed and angle
        self.x += self.speed * math.cos(math.radians(self.direction))
        self.y -= self.speed * math.sin(math.radians(self.direction))
        self.rect.x = self.x
        self.rect.y = self.y

    def collidable_points(self):
        if self.direction > 270:
            return [self.rect.midbottom, self.rect.bottomright, self.rect.midright]
        elif self.direction > 180:
            return [self.rect.midleft, self.rect.bottomleft, self.rect.midbottom]
        elif self.direction > 90:
            return [self.rect.midleft, self.rect.topleft, self.rect.midtop]
        else:
            return [self.rect.midtop, self.rect.topright, self.rect.midright]

    def check_bricks_collision(self):
        for brick in self.bricks:
            collided = False
            collided = brick.collide_points(self.collidable_points())

            if not collided:
                continue

            brick.kill()
            self.direction = (360 - self.direction)

    def calculate_direction(self):
        max_angle = 180 - 2 * DEGREE_NORMALIZATION_FACTOR
        collision_area = PADDLE_SIZE[0] + BALL_SIZE[0]
        collision_x = self.rect.x - self.paddle.rect.x + BALL_SIZE[0]
        new_angle = collision_x * max_angle / collision_area + DEGREE_NORMALIZATION_FACTOR

        return new_angle

    def check_paddle_collision(self):
        was_hit = self.rect.colliderect(self.paddle.rect)

        # If hit by the paddle go up and apply angle depending on which part of
        # the paddle it was hit by
        if was_hit:
            new_angle = self.calculate_direction()
            self.direction = (540 - new_angle) % 360


class Paddle(pygame.sprite.Sprite):
    """docstring for Paddle"""
    def __init__(self):
        super(Paddle, self).__init__()

        # Variables to draw the ball
        self.image = pygame.Surface(PADDLE_SIZE)
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()

        self.rect.x = 0
        self.rect.y = SCREEN_SIZE[1] - PADDLE_SIZE[1] - 20

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

def reresh_score(screen, player):
    score_font = pygame.font.SysFont('Courier New', 30)
    textsurface = score_font.render(f'Lives {player.lives}', True, BLACK)
    screen.blit(textsurface, (20, 20))

def main():
    pygame.init()
    pygame.font.init()

    pygame.display.set_caption('Breakout')
    pygame.mouse.set_visible(0)
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_SIZE[0], SCREEN_SIZE[1]), 0, 32)

    paddle = Paddle()
    bricks = generate_grid()
    player = Player(paddle, bricks)

    sprites = pygame.sprite.Group()
    sprites.add(bricks)
    sprites.add(player)
    sprites.add(paddle)

    running = True

    while running:
        screen.fill(WHITE)
        player.move()
        sprites.draw(screen)
        reresh_score(screen, player)

        for event in pygame.event.get():
            # Stop running when the user clicks close window button
            if event.type == pygame.QUIT:
                running = False

            # React to the user moving the mouse
            if event.type == pygame.MOUSEMOTION:
                mouse_position = pygame.mouse.get_pos()
                paddle.set_x(mouse_position[0])

        pygame.display.update()
        clock.tick(120)

if __name__ == '__main__':
    main()
