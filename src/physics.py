# src/physics.py
import numpy as np
from src import config


class PhysicsEngine:
    """Manages particle mechanics, parameter presets, and interaction matrices."""

    def __init__(self):
        self.num_types = len(config.TYPES)
        self.species_counts = list(config.DEFAULT_SPECIES_COUNTS)

        # Dynamic physics parameters
        self.r_max = config.DEFAULT_R_MAX
        self.r_repel = config.DEFAULT_R_REPEL
        self.friction = config.DEFAULT_FRICTION
        self.force_factor = config.FORCE_FACTOR

        # Interaction matrix (-1.0 to +1.0)
        self.matrix = np.random.uniform(-0.8, 0.8, (self.num_types, self.num_types))
        self.reset_particles()

    def reset_physics_defaults(self) -> None:
        """Reset physics parameters back to initial base configuration values."""
        self.r_max = config.DEFAULT_R_MAX
        self.r_repel = config.DEFAULT_R_REPEL
        self.friction = config.DEFAULT_FRICTION
        self.force_factor = config.FORCE_FACTOR

    def apply_preset(self, preset_matrix: list[list[float]]) -> None:
        """Apply a predefined interaction matrix."""
        self.matrix = np.array(preset_matrix, dtype=np.float64)

    def set_species_count(self, species_idx: int, new_count: int) -> None:
        """Dynamically adjust particle count for a single species."""
        if self.species_counts[species_idx] == new_count:
            return
        self.species_counts[species_idx] = new_count
        self.reset_particles()

    def reset_particles(self) -> None:
        """Re-spawn particles uniformly across the canvas."""
        types_list = []
        for species_idx, count in enumerate(self.species_counts):
            types_list.extend([species_idx] * count)

        self.num_particles = len(types_list)
        if self.num_particles == 0:
            self.pos = np.empty((0, 2))
            self.vel = np.empty((0, 2))
            self.types = np.empty(0, dtype=np.int32)
            return

        self.types = np.array(types_list, dtype=np.int32)
        self.pos = np.random.rand(self.num_particles, 2) * [
            config.SIM_WIDTH,
            config.SIM_HEIGHT,
        ]
        self.vel = np.zeros((self.num_particles, 2))

    def randomize_matrix(self) -> None:
        """Generate a new random attraction/repulsion matrix."""
        self.matrix = np.random.uniform(-0.8, 0.8, (self.num_types, self.num_types))

    def update(self, dt: float = 1.0) -> None:
        """Calculate pairwise interaction forces and update particle positions."""
        if self.num_particles == 0:
            return

        x = self.pos[:, 0:1]
        y = self.pos[:, 1:2]

        dx = x.T - x
        dy = y.T - y

        dx = dx - np.round(dx / config.SIM_WIDTH) * config.SIM_WIDTH
        dy = dy - np.round(dy / config.SIM_HEIGHT) * config.SIM_HEIGHT

        r = np.sqrt(dx**2 + dy**2)
        r_safe = np.where(r == 0, 1e-5, r)

        mask = (r < self.r_max) & (r > 0)

        types_i = self.types[:, None]
        types_j = self.types[None, :]
        attraction_matrix = self.matrix[types_i, types_j]

        force = np.zeros_like(r)

        repel_mask = mask & (r < self.r_repel)
        force[repel_mask] = (r[repel_mask] / self.r_repel) - 1.0

        attract_mask = mask & (r >= self.r_repel)
        mid = 0.5 * (self.r_repel + self.r_max)
        half_width = max(0.1, 0.5 * (self.r_max - self.r_repel))
        scale = 1.0 - np.abs(r[attract_mask] - mid) / half_width
        force[attract_mask] = attraction_matrix[attract_mask] * scale

        fx = np.sum(np.where(mask, force * (dx / r_safe), 0), axis=1)
        fy = np.sum(np.where(mask, force * (dy / r_safe), 0), axis=1)

        acc = np.column_stack((fx, fy)) * self.force_factor

        self.vel = (self.vel + acc * dt) * (1.0 - self.friction)
        self.pos += self.vel * dt

        self.pos[:, 0] %= config.SIM_WIDTH
        self.pos[:, 1] %= config.SIM_HEIGHT