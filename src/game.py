import pygame

from src.asset import AssetManager
from src.display import DisplayManager
from src.scene import SceneManager
from src.settings import *


class Game:
    """
    Main game controller. Handles setup, the game loop, and quitting.
    """

    def __init__(self) -> None:
        """
        Sets up game subsystems, asset manager, display, and timing.
        """
        pygame.init()
        pygame.mixer.init()
        self.assets = AssetManager(ASSETS_DIR)
        self.display = DisplayManager(GAME_TITLE, GAME_WIDTH, GAME_HEIGHT)
        self.scenes = SceneManager()
        self.clock = pygame.time.Clock()
        self.running = True

    def handle_events(self) -> None:
        """
        Handles system and input events (close, keyboard, etc).
        Sets self.running to False when the user requests to quit.
        """
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
        self.scenes.handle_events(events)

    def update(self) -> None:
        """
        Updates all game logic.
        (Placeholder: Fill this in with movement, collisions, etc)
        """
        dt = self.clock.get_time() / 1000.0
        self.scenes.update(dt)

    def draw(self) -> None:
        """
        Draws the current game state to the screen.
        (Placeholder: Fill this in with draw code)
        """
        self.display.surface.fill((255, 255, 255))
        self.scenes.draw(self.display.surface)

    def present(self) -> None:
        """
        Shows the latest drawn frame on the screen.
        (Usually just flips or updates the display)
        """
        self.display.present()

    def tick(self) -> None:
        """
        Limits the frame rate to the desired FPS.
        """
        self.clock.tick(GAME_FPS)

    def run(self) -> None:
        """
        Runs the main game loop (input, update, draw, present, tick).
        Exits cleanly and quits Pygame when finished.
        """
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.present()
            self.tick()
        pygame.quit()
