import random

import pygame

# Particles that are behind main character when he is running
class Particle:
    def __init__(self, vx, vy, radius, initial_position=(150, 150), color=(255, 255, 255)):
        self.vx = vx
        self.vy = vy
        self.radius = radius
        self.x = initial_position[0]
        self.y = initial_position[1]
        self.color = color

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.radius -= 0.15

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, [int(self.x), int(self.y)], self.radius)


def get_random_speed(opposite1=False, opposite2=False):  # Default go upstairs
    v1 = random.choice([-1, 1]) * random.random() / 2
    v2 = -1 * (0.3 + random.random())
    if opposite1:
        v1 = -v1
    if opposite2:
        v2 = -v2
    return v1, v2


class ParticleSystem:
    def __init__(self):
        self.particles = []
        self.counter = 0
        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = 0

    def set_v(self, vx, vy):
        self.vx = vx
        self.vy = vy

    def update(self):
        self.counter += 1
        if self.counter > 25:
            self.particles.append(Particle(self.vx, self.vy, 7, initial_position=(self.x, self.y),
                                           color=(50, 150, 100)))
            self.counter = 0
        for p in self.particles:
            p.update()
        if len(self.particles) > 500:
            del self.particles[0]

    def draw(self, screen):
        for p in self.particles:
            p.draw(screen)

    def empty(self):
        self.particles = []


if __name__ == '__main__':
    clock = pygame.time.Clock()
    res=(300, 300)
    screen = pygame.display.set_mode(res)
    count = 0
    particles = []
    ps = ParticleSystem()
    move = False
    while True:
        clock.tick(1500)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    move = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    move = False
        screen.fill((0, 0, 0))
        if move:
            ps.update()
            ps.draw(screen)
        pygame.display.update()

