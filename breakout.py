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
        self.direction = math.radians(315)
        self.speed = 0.5
        self.x = 400
        self.y = 300

    def move(self):
        if self.x < 0 or self.x > 800:
            self.direction = math.radians(180 - math.degrees(self.direction))
        if self.y < 0 or self.y > 600:
            self.direction = math.radians(360 - math.degrees(self.direction))

        was_hit_by_puck = self.getRect().colliderect(self.puck.getRect())
        was_hit_with_the_top_of_puck = self.getRect().bottom - 1 <= self.puck.getRect().top
        
        if was_hit_by_puck and was_hit_with_the_top_of_puck:
            self.direction = math.radians(math.degrees(self.direction) + 180)

        self.x += self.speed * math.cos(self.direction)
        self.y -= self.speed * math.sin(self.direction)

        print (f"mouse @ {self.x} {self.y} @ {math.degrees(self.direction)}")

    def draw(self, screen):
        self.move()
        pygame.draw.rect(screen, BLACK, self.getRect())

    def getRect(self):
        return pygame.Rect(self.x, self.y, 10, 10)


class Puck(object):
    """docstring for Puck"""
    def __init__(self):
        super(Puck, self).__init__()
        self.x = 0
        self.y = 500

    def move(self, mouse):
        self.x = pygame.mouse.get_pos()[0]

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, self.getRect())

    def getRect(self):
        return pygame.Rect(self.x, self.y, 150, 50)

    def updateSpeed(self):
        current_mouse_velocity = pygame.mouse.get_rel()
        max_speed = current_mouse_velocity[0]


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
