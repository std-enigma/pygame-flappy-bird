import pygame
from pygame import Surface


class DisplayManager:
    """
    Handles drawing to an off-screen surface ("game surface") and scaling/blitting it to the main window,
    automatically adding black bars (letterboxing) if needed to preserve aspect ratio.
    """

    def __init__(
        self, title: str, width: int, height: int, icon: Surface | None = None
    ) -> None:
        """
        Creates a new display manager with a window (that can be resized) and a fixed-size drawing surface.

        Args:
            title (str): Window title shown at the top.
            width (int): Game surface width (internal "design" resolution).
            height (int): Game surface height (internal "design" resolution).
            icon (pygame.Surface | None): Optional window icon.
        """
        # Window is created double-size for better upscaling and classroom demos
        self.window = pygame.display.set_mode((width * 2, height * 2), pygame.RESIZABLE)
        pygame.display.set_caption(title)
        if icon:
            pygame.display.set_icon(icon)
        # The internal surface all game logic draws to
        self.surface = pygame.Surface((width, height))

    def present(self) -> None:
        """
        Scales the contents of the game surface up to fit the current window,
        preserving aspect ratio and adding black bars where needed.
        Then blits the result to the window and updates the display.
        """
        # Get current window and surface sizes
        win_w, win_h = self.window.get_size()
        surf_w, surf_h = self.surface.get_size()

        # Find integer scale that fits while maintaining aspect ratio
        scale = min(win_w / surf_w, win_h / surf_h)
        scaled_w = int(surf_w * scale)
        scaled_h = int(surf_h * scale)

        # Center the scaled surface
        x = (win_w - scaled_w) // 2
        y = (win_h - scaled_h) // 2

        # Smoothly scale the surface for better quality
        scaled_surf = pygame.transform.smoothscale(self.surface, (scaled_w, scaled_h))

        # Fill window with black (letterboxing bars)
        self.window.fill((0, 0, 0))

        # Blit (copy) the scaled surface onto the window at the centered position
        self.window.blit(scaled_surf, (x, y))
        pygame.display.flip()
