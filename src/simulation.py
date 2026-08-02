# src/simulation.py
import pygame
import sys
from src import config
from src.physics import PhysicsEngine
from src.renderer import Renderer
from src.ui import UIManager


class Simulation:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("HEYNE - Life Emergence")

        self.surface = pygame.display.set_mode(
            (config.WINDOW_WIDTH, config.WINDOW_HEIGHT),
            pygame.SCALED
        )
        self.clock = pygame.time.Clock()

        self.physics = PhysicsEngine()
        self.renderer = Renderer(self.surface)
        self.ui = UIManager(self.physics)
        self.running = True

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0

            self.handle_events()
            self.physics.update(dt=1.0)

            self.renderer.render(self.physics)
            self.ui.draw(self.surface)

            pygame.display.flip()

        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

            self.ui.handle_event(event)