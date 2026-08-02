# src/ui.py
import pygame
import numpy as np
from src import config

PRESETS = {
    "Food Chain": [
        [0.2, 0.8, -0.4, -0.2],
        [-0.2, 0.2, 0.8, -0.4],
        [-0.4, -0.2, 0.2, 0.8],
        [0.8, -0.4, -0.2, 0.2]
    ],
    "Swarms": [
        [0.8, -0.6, 0.2, -0.2],
        [-0.2, 0.8, -0.6, 0.2],
        [0.2, -0.2, 0.8, -0.6],
        [-0.6, 0.2, -0.2, 0.8]
    ],
    "Gliding Worms": [
        [0.1, 0.9, -0.9, 0.3],
        [-0.3, 0.2, 0.8, -0.7],
        [0.6, -0.5, 0.1, 0.9],
        [-0.8, 0.4, -0.6, 0.2]
    ],
    "Symbiosis": [
        [0.6, 0.7, -0.8, -0.8],
        [0.7, 0.5, -0.8, -0.8],
        [-0.8, -0.8, 0.6, 0.7],
        [-0.8, -0.8, 0.7, 0.5]
    ]
}


class UISlider:
    """Minimalist slider widget for setting numerical parameters."""

    def __init__(self, x: int, y: int, w: int, h: int, min_val: float, max_val: float, initial_val: float, label: str, is_int: bool = False, color_accent: tuple = (58, 130, 246)):
        self.rect = pygame.Rect(x, y, w, h)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.label = label
        self.is_int = is_int
        self.color_accent = color_accent
        self.dragging = False

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.inflate(0, 12).collidepoint(event.pos):
                self.dragging = True
                self.update_val(event.pos[0])
                return True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.update_val(event.pos[0])
            return True
        return False

    def update_val(self, mouse_x: int) -> None:
        rel = max(0.0, min(1.0, (mouse_x - self.rect.x) / self.rect.width))
        val = self.min_val + rel * (self.max_val - self.min_val)
        self.value = int(round(val)) if self.is_int else round(val, 2)

    def draw(self, surface: pygame.Surface, font_label: pygame.font.Font, font_val: pygame.font.Font) -> None:
        lbl = font_label.render(self.label, True, (160, 174, 192))
        val_str = f"{int(self.value)}" if self.is_int else f"{self.value:.2f}"
        val_txt = font_val.render(val_str, True, (226, 232, 240))

        surface.blit(lbl, (self.rect.x, self.rect.y - 17))
        surface.blit(val_txt, (self.rect.x + self.rect.width - val_txt.get_width(), self.rect.y - 17))

        pygame.draw.rect(surface, (30, 41, 59), self.rect, border_radius=3)
        rel = (self.value - self.min_val) / (self.max_val - self.min_val)
        fill_w = int(self.rect.width * rel)
        if fill_w > 0:
            fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_w, self.rect.height)
            pygame.draw.rect(surface, self.color_accent, fill_rect, border_radius=3)

        handle_x = self.rect.x + fill_w
        pygame.draw.circle(surface, (241, 245, 249), (handle_x, self.rect.centery), 5)


class UIManager:
    """Manages sidebar panel layout, fixed positions, buttons, and presets."""

    def __init__(self, physics_engine):
        self.physics = physics_engine

        # Core Typography
        self.title_font = pygame.font.SysFont("Helvetica Neue, Arial", 16, bold=True)
        self.section_font = pygame.font.SysFont("Helvetica Neue, Arial", 11, bold=True)
        self.label_font = pygame.font.SysFont("Helvetica Neue, Arial", 12)
        self.mono_font = pygame.font.SysFont("Menlo, Monaco, Consolas", 11)

        self.sidebar_rect = pygame.Rect(
            config.SIM_WIDTH, 0, config.SIDEBAR_WIDTH, config.WINDOW_HEIGHT
        )

        # Baseline layout coordinates
        sx = config.SIM_WIDTH + 30
        sw = 360

        # Matrix Configuration
        self.matrix_rects = {}
        self.setup_matrix_ui()

        # Section 1: Species Population Sliders
        self.species_sliders = []
        pop_y = 290
        for idx in range(len(config.TYPES)):
            slider = UISlider(
                sx, pop_y + idx * 36, sw, 4, 0, 300,
                self.physics.species_counts[idx],
                f"{config.COLOR_NAMES[idx]} Population",
                is_int=True,
                color_accent=config.COLORS[idx]
            )
            self.species_sliders.append(slider)

        # Section 2: Physics Engine Sliders
        phys_y = 485
        self.physics_sliders = {
            "friction": UISlider(sx, phys_y, sw, 4, 0.05, 0.40, self.physics.friction, "Friction Damping"),
            "r_max": UISlider(sx, phys_y + 36, sw, 4, 30.0, 180.0, self.physics.r_max, "Interaction Radius (r_max)"),
            "r_repel": UISlider(sx, phys_y + 72, sw, 4, 5.0, 50.0, self.physics.r_repel, "Repulsion Radius (r_repel)"),
            "force": UISlider(sx, phys_y + 108, sw, 4, 0.5, 8.0, self.physics.force_factor, "Simulation Speed"),
        }

        # Reset Physics Button
        self.btn_reset_physics = pygame.Rect(sx + 260, 442, 100, 22)

        # Section 3: Interaction Presets
        preset_y = 650
        self.preset_btns = {}
        preset_names = list(PRESETS.keys())
        for idx, name in enumerate(preset_names):
            bx = sx if idx % 2 == 0 else sx + 185
            by = preset_y + (idx // 2) * 38
            self.preset_btns[name] = pygame.Rect(bx, by, 175, 32)

        # Global Action Buttons (Bottom)
        self.btn_randomize = pygame.Rect(sx, config.WINDOW_HEIGHT - 55, 175, 36)
        self.btn_reset = pygame.Rect(sx + 185, config.WINDOW_HEIGHT - 55, 175, 36)

    def setup_matrix_ui(self) -> None:
        start_x = config.SIM_WIDTH + 110
        start_y = 75
        cell_size = 42

        for i in range(self.physics.num_types):
            for j in range(self.physics.num_types):
                rect = pygame.Rect(start_x + j * cell_size, start_y + i * cell_size, cell_size - 4, cell_size - 4)
                self.matrix_rects[(i, j)] = rect

    def handle_event(self, event: pygame.event.Event) -> None:
        # Evaluate Slider Events
        for idx, slider in enumerate(self.species_sliders):
            if slider.handle_event(event):
                self.physics.set_species_count(idx, int(slider.value))

        for key, slider in self.physics_sliders.items():
            if slider.handle_event(event):
                if key == "friction":
                    self.physics.friction = slider.value
                elif key == "r_max":
                    self.physics.r_max = slider.value
                elif key == "r_repel":
                    self.physics.r_repel = slider.value
                elif key == "force":
                    self.physics.force_factor = slider.value

        # Evaluate Click Events
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            
            if self.btn_reset_physics.collidepoint(pos):
                self.physics.reset_physics_defaults()
                self.physics_sliders["friction"].value = self.physics.friction
                self.physics_sliders["r_max"].value = self.physics.r_max
                self.physics_sliders["r_repel"].value = self.physics.r_repel
                self.physics_sliders["force"].value = self.physics.force_factor

            elif self.btn_randomize.collidepoint(pos):
                self.physics.randomize_matrix()
            elif self.btn_reset.collidepoint(pos):
                self.physics.reset_particles()

            for name, btn in self.preset_btns.items():
                if btn.collidepoint(pos):
                    self.physics.apply_preset(PRESETS[name])

            for (i, j), rect in self.matrix_rects.items():
                if rect.collidepoint(pos):
                    delta = 0.1
                    new_val = np.clip(self.physics.matrix[i, j] + delta, -1.0, 1.0)
                    self.physics.matrix[i, j] = round(new_val, 1)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            pos = event.pos
            for (i, j), rect in self.matrix_rects.items():
                if rect.collidepoint(pos):
                    delta = -0.1
                    new_val = np.clip(self.physics.matrix[i, j] + delta, -1.0, 1.0)
                    self.physics.matrix[i, j] = round(new_val, 1)

    def draw(self, surface: pygame.Surface) -> None:
        # Base Sidebar Background
        pygame.draw.rect(surface, (13, 17, 23), self.sidebar_rect)
        pygame.draw.line(surface, (48, 54, 61), (config.SIM_WIDTH, 0), (config.SIM_WIDTH, config.WINDOW_HEIGHT), 1)

        # Header Titles
        title = self.title_font.render("HEYNE - Life Emergence", True, (240, 246, 252))
        surface.blit(title, (config.SIM_WIDTH + 30, 20))

        sub = self.label_font.render("Attraction / Repulsion Matrix", True, (139, 148, 158))
        surface.blit(sub, (config.SIM_WIDTH + 30, 45))

        # Interaction Matrix
        start_x = config.SIM_WIDTH + 110
        start_y = 75
        cell_size = 42

        for k in range(self.physics.num_types):
            pygame.draw.circle(surface, config.COLORS[k], (start_x + k * cell_size + 19, start_y - 12), 4)
            pygame.draw.circle(surface, config.COLORS[k], (start_x - 14, start_y + k * cell_size + 19), 4)

        for (i, j), rect in self.matrix_rects.items():
            val = self.physics.matrix[i, j]
            if val >= 0:
                bg = (16, int(30 + val * 120), 40)
                border_col = (34, int(80 + val * 120), 70)
            else:
                bg = (int(35 + abs(val) * 120), 18, 28)
                border_col = (int(90 + abs(val) * 120), 40, 50)

            pygame.draw.rect(surface, bg, rect, border_radius=5)
            pygame.draw.rect(surface, border_col, rect, 1, border_radius=5)

            txt = self.mono_font.render(f"{val:+.1f}", True, (240, 246, 252))
            surface.blit(txt, txt.get_rect(center=rect.center))

        # --- Section 1: Population ---
        pygame.draw.line(surface, (33, 38, 45), (config.SIM_WIDTH + 30, 255), (config.SIM_WIDTH + 390, 255), 1)
        head_pop = self.section_font.render("POPULATION CONTROL", True, (139, 148, 158))
        surface.blit(head_pop, (config.SIM_WIDTH + 30, 262))

        for slider in self.species_sliders:
            slider.draw(surface, self.label_font, self.mono_font)

        # --- Section 2: Physics Engine ---
        pygame.draw.line(surface, (33, 38, 45), (config.SIM_WIDTH + 30, 440), (config.SIM_WIDTH + 390, 440), 1)
        head_phys = self.section_font.render("PHYSICS ENGINE", True, (139, 148, 158))
        surface.blit(head_phys, (config.SIM_WIDTH + 30, 448))

        pygame.draw.rect(surface, (30, 41, 59), self.btn_reset_physics, border_radius=4)
        pygame.draw.rect(surface, (51, 65, 85), self.btn_reset_physics, 1, border_radius=4)
        lbl_reset_p = self.mono_font.render("Reset Defaults", True, (203, 213, 225))
        surface.blit(lbl_reset_p, lbl_reset_p.get_rect(center=self.btn_reset_physics.center))

        for slider in self.physics_sliders.values():
            slider.draw(surface, self.label_font, self.mono_font)

        # --- Section 3: Presets ---
        pygame.draw.line(surface, (33, 38, 45), (config.SIM_WIDTH + 30, 615), (config.SIM_WIDTH + 390, 615), 1)
        head_preset = self.section_font.render("INTERACTION PRESETS", True, (139, 148, 158))
        surface.blit(head_preset, (config.SIM_WIDTH + 30, 623))

        for name, btn in self.preset_btns.items():
            pygame.draw.rect(surface, (30, 41, 59), btn, border_radius=5)
            pygame.draw.rect(surface, (51, 65, 85), btn, 1, border_radius=5)
            lbl_p = self.label_font.render(name, True, (226, 232, 240))
            surface.blit(lbl_p, lbl_p.get_rect(center=btn.center))

        # --- Global Buttons ---
        pygame.draw.rect(surface, (37, 99, 235), self.btn_randomize, border_radius=6)
        pygame.draw.rect(surface, (220, 38, 38), self.btn_reset, border_radius=6)

        lbl_rand = self.label_font.render("Randomize Matrix", True, (255, 255, 255))
        lbl_reset = self.label_font.render("Reset Particles", True, (255, 255, 255))

        surface.blit(lbl_rand, lbl_rand.get_rect(center=self.btn_randomize.center))
        surface.blit(lbl_reset, lbl_reset.get_rect(center=self.btn_reset.center))