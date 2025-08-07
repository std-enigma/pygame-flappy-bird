import os

import pygame
from pygame import Surface
from pygame.mixer import Sound


class AssetManager:
    """
    Loads and stores all game assets (images and sounds).
    Ensures each asset is only loaded from disk once.
    """

    def __init__(self, dir: str) -> None:
        """
        Create a new AssetManager.

        Args:
            dir (str): Path to the assets folder.
        """
        self.assets_dir = dir
        self.images: dict[str, Surface] = {}  # Loaded images by name
        self.sounds: dict[str, Sound] = {}  # Loaded sounds by name

    def load_icon(self) -> Surface:
        """
        Loads and returns the game icon image as a Surface.
        Caches the icon so it is only loaded once.

        Returns:
            pygame.Surface: The icon surface.
        """
        if "icon" not in self.images:
            # Look for 'favicon.ico' in the assets directory
            path = os.path.join(self.assets_dir, "favicon.ico")
            icon = pygame.image.load(path).convert_alpha()
            self.images["icon"] = icon
        return self.images["icon"]

    def load_image(self, name: str) -> Surface:
        """
        Loads (if not already loaded) and returns an image by filename.

        Args:
            name (str): Filename of the image inside assets/textures/.

        Returns:
            pygame.Surface: The loaded image Surface.
        """
        if name not in self.images:
            path = os.path.join(self.assets_dir, "textures", name)
            image = pygame.image.load(path).convert_alpha()
            self.images[name] = image
        return self.images[name]

    def load_sound(self, name: str) -> Sound:
        """
        Loads (if not already loaded) and returns a sound by filename.

        Args:
            name (str): Filename of the sound inside assets/sounds/.

        Returns:
            pygame.mixer.Sound: The loaded sound object.
        """
        if name not in self.sounds:
            path = os.path.join(self.assets_dir, "sounds", name)
            sound = pygame.mixer.Sound(path)
            self.sounds[name] = sound
        return self.sounds[name]
