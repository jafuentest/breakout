import pygame
import math

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

BALL_SIZE = (10, 10)

class Ball(object):
    """docstring for Ball"""
    def __init__(self, puck):
        super(Ball, self).__init__()
        self.puck = puck
        self.direction = math.radians(270)
        self.speed = 1
        self.x = 400
        self.y = 300

    def move(self):
        # If it hits a side of the screen, flip angle vertically
        if self.x < 0 or self.x > 800:
            self.direction = math.radians(180 - math.degrees(self.direction))
        
        # If it hits top/bottom of the screen, flip angle horizontally
        if self.y < 0 or self.y > 600:
            self.direction = math.radians(360 - math.degrees(self.direction))

        was_hit_by_puck = self.getRect().colliderect(self.puck.getRect())
        was_hit_with_the_top_of_puck = self.getRect().bottom - 1 <= self.puck.getRect().top

        # If hit by the puck go up and apply angle depending on which part of
        # the puck it was hit by
        if was_hit_by_puck and was_hit_with_the_top_of_puck:
            collision_x = self.x - self.puck.getX() + BALL_SIZE[0]
            collision_x *= 150 / 180
            self.direction = math.radians(180 - collision_x)
            print (f"mouse @ { collision_x }")

        # Set new position base on speed and angle
        self.x += self.speed * math.cos(self.direction)
        self.y -= self.speed * math.sin(self.direction)

    def draw(self, screen):
        self.move()
        pygame.draw.rect(screen, BLACK, self.getRect())

    def getRect(self):
        return pygame.Rect((self.x, self.y), BALL_SIZE)


class Puck(object):
    """docstring for Puck"""
    def __init__(self):
        super(Puck, self).__init__()
        self.x = 0
        self.y = 500

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, self.getRect())

    def getRect(self):
        return pygame.Rect(self.x, self.y, 170, 50)

    def getX(self):
        return self.x

    def setX(self, x):
        self.x = x

def main():
    pygame.init()
    pygame.display.set_caption('Breakout')

    screen = pygame.display.set_mode((800,600), 0, 32)

    running = True

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

            # React to the user moving the mouse
            if event.type == pygame.MOUSEMOTION:
                mouse_position = pygame.mouse.get_pos()
                puck.setX(mouse_position[0])

        pygame.display.update()

if __name__ == '__main__':
    main()
