import sys
from math import sqrt
from random import Random

from pygame.constants import QUIT
from pygame.surface import Surface

rand = Random()
SIZE = (400, 400)


def bounce_io(pygame, background_fill, player_color, target_color, surface_size, min_radius, max_radius):
    global SIZE
    SIZE = surface_size
    pygame.init()
    fps = 30
    fps_clock = pygame.time.Clock()
    player_speed = 3
    target_speed = 4
    display_surface: Surface = pygame.display.set_mode(surface_size, 0, 32)
    pygame.display.set_caption("Collision Test")
    player = Circle(
        (surface_size[0] // 2, surface_size[1] // 2),
        10,
        player_speed
    )
    target = Circle(
        random_location(),
        10,
        target_speed
    )
    is_shrinking = False
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        display_surface.fill(background_fill)
        pygame.draw.circle(display_surface, player_color, player.location, player.radius)
        if is_shrinking:
            player.radius -= 1
            if player.radius <= min_radius:
                is_shrinking = False
                target.location = random_location()
        else:
            pygame.draw.circle(display_surface, target_color, target.location, target.radius)
            bounce(target)
            chase(player, target)
            player.location = (player.location[0] + player.speed_vector[0], player.location[1] + player.speed_vector[1])
            if player.distance_to(target) > player.radius + target.radius:
                target.location = (
                    target.location[0] + target.speed_vector[0], target.location[1] + target.speed_vector[1]
                )
            else:  # We collided
                radius_gain = int(0.3 * target.radius)
                if player.radius + radius_gain < max_radius:
                    player.radius += radius_gain
                    target.location = random_location()
                else:
                    is_shrinking = True

        pygame.display.update()
        fps_clock.tick(fps)
        debug("player (x, y): (%d, %d)" % (player.x, player.y))


def bounce_io_debug(pygame, background_fill, player_color, target_color, surface_size, min_radius, max_radius, debugger):
    global debug
    debug = debugger
    bounce_io(pygame, background_fill, player_color, target_color, surface_size, min_radius, max_radius)


def random_location():
    return rand.randint(10, SIZE[0] - 10), rand.randint(10, SIZE[1] - 10)


class Circle:
    def __init__(self, location, radius, speed: int, speed_vector=None):
        self.location = location
        self.radius = radius
        self.speed = speed
        if speed_vector is None:
            self.speed_vector = (self.speed, self.speed)
        else:
            self.speed_vector = speed_vector

    @property
    def x(self):
        return self.location[0]

    @property
    def y(self):
        return self.location[1]

    @property
    def top(self):
        return self.y - self.radius

    @property
    def bottom(self):
        return self.y + self.radius

    @property
    def left(self):
        return self.x - self.radius

    @property
    def right(self):
        return self.x + self.radius

    def distance_to(self, other):
        horizontal_distance = self.x - other.x
        vertical_distance = self.y - other.y
        return sqrt(pow(horizontal_distance, 2) + pow(vertical_distance, 2))


def bounce(circle: Circle):
    if circle.left <= 0 or circle.right >= SIZE[0]:
        circle.speed_vector = (-circle.speed_vector[0], circle.speed_vector[1])
    if circle.top <= 0 or circle.bottom >= SIZE[1]:
        circle.speed_vector = (circle.speed_vector[0], -circle.speed_vector[1])


def chase(player: Circle, target: Circle):
    horizontal_speed = 0
    vertical_speed = 0
    if target.x > player.x:
        horizontal_speed = 1
    elif target.x < player.x:
        horizontal_speed = -1
    if target.y > player.y:
        vertical_speed = 1
    elif target.y < player.y:
        vertical_speed = -1
    if player.distance_to(target) < player.speed:
        speed = int(player.distance_to(target))
    else:
        speed = player.speed
    player.speed_vector = horizontal_speed * speed, vertical_speed * speed
