# src/config.py

# Window and Canvas Dimensions
WINDOW_WIDTH = 1500
WINDOW_HEIGHT = 900
SIDEBAR_WIDTH = 420
SIM_WIDTH = WINDOW_WIDTH - SIDEBAR_WIDTH
SIM_HEIGHT = WINDOW_HEIGHT

# Particles
TYPES = [0, 1, 2, 3]
COLOR_NAMES = ["Red", "Blue", "Green", "White"]

# Color Palette (RGB)
COLORS = [
    (235, 55, 55),    # Red
    (55, 140, 255),   # Blue
    (40, 205, 110),   # Green
    (255, 255, 255)   # White
]

# Initial Particle Count
DEFAULT_SPECIES_COUNTS = [120, 120, 120, 120]

# Physics Engine Defaults
DEFAULT_FRICTION = 0.15
DEFAULT_R_MAX = 100.0
DEFAULT_R_REPEL = 20.0
FORCE_FACTOR = 1