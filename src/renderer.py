"""High-performance flat particle renderer for Heyne Life — Emergence."""

import pygame
from src import config


class Renderer:
    """Renders crisp, flat particle dots using batched surface blitting."""

    def __init__(self, surface: pygame.Surface):
        self.surface = surface
        self.particle_textures = self._create_particle_textures()

    def _create_particle_textures(self) -> list[pygame.Surface]:
        """Pre-renders particle surfaces for optimal performance."""
        textures = []
        size = 8
        center = size // 2

        for color in config.COLORS:
            surf = pygame.Surface((size, size), pygame.SRCALPHA)

            # Faint 1px outer contrast ring for high-DPI clarity
            pygame.draw.circle(surf, (*color, 35), (center, center), 3)

            # Solid, sharp 2px particle core
            pygame.draw.circle(surf, color, (center, center), 2)

            textures.append(surf)

        return textures

    def render(self, physics_engine) -> None:
        """Clear canvas and batch-blit particle textures."""
        sim_rect = pygame.Rect(0, 0, config.SIM_WIDTH, config.SIM_HEIGHT)
        pygame.draw.rect(self.surface, (10, 12, 16), sim_rect)

        pos = physics_engine.pos
        types = physics_engine.types
        offset = 4  # Center 8x8 surface offset

        # Batch blitting passes the entire sequence to Pygame's C-engine at once
        blit_list = [
            (
                self.particle_textures[types[i]],
                (int(pos[i, 0]) - offset, int(pos[i, 1]) - offset),
            )
            for i in range(physics_engine.num_particles)
        ]
        self.surface.blits(blit_list)