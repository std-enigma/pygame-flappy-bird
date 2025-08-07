from abc import ABC, abstractmethod

from pygame import Surface
from pygame.event import Event
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.game import Game

class Scene(ABC):
    """
    Abstract base class for all scenes (game states/screens).
    Any subclass must implement all abstract methods.
    """

    def __init__(self, game: "Game") -> None:
        self.game = game

    @abstractmethod
    def handle_events(self, events: list[Event]) -> None:
        """
        Handle input/events for the scene.
        """
        pass

    @abstractmethod
    def update(self, dt: float) -> None:
        """
        Update game logic for the scene.

        Args:
            dt (float): Time in seconds since the last frame.
        """
        pass

    @abstractmethod
    def draw(self, surface: Surface) -> None:
        """
        Draw everything to the provided surface.
        """
        pass

    def on_enter(self) -> None:
        """
        Optional: runs when this scene becomes active.
        """
        pass

    def on_exit(self) -> None:
        """
        Optional: runs when this scene loses focus or is deactivated.
        """
        pass


class SceneManager:
    """
    Manages game scenes ("screens" or "states"), such as title, menu, gameplay, etc.
    Handles switching, stacking (pause, overlays), and passing game loop phases.
    """

    def __init__(self):
        """
        Initializes the scene manager with no scenes.
        """
        self.scenes: list[Scene] = []  # Stack of active scenes (last = current)
        self.current: Scene | None = None  # The scene currently in control

    def push(self, scene: Scene):
        """
        Adds a scene on top of the current one.
        Useful for modals like Pause, overlays, or nested menus.

        Args:
            scene: Instance of a Scene subclass to activate.
        """
        if self.current:
            self.current.on_exit()
        self.scenes.append(scene)
        self.current = scene
        self.current.on_enter()

    def pop(self):
        """
        Removes the current scene (like closing a pause menu).
        Returns to the previous scene if there is one.
        """
        if self.current:
            self.current.on_exit()
            self.scenes.pop()
        self.current = self.scenes[-1] if self.scenes else None
        if self.current:
            self.current.on_enter()

    def switch(self, scene: Scene):
        """
        Replaces the current scene with a new one.
        Like going from title screen to gameplay.

        Args:
            scene: Instance of a Scene subclass to be the new active scene.
        """
        if self.current:
            self.current.on_exit()
            self.scenes.pop()
        self.scenes.append(scene)
        self.current = scene
        self.current.on_enter()

    def handle_events(self, events: list[Event]):
        """
        Passes input or system events to the current scene.

        Args:
            events: List of events (typically from pygame.event.get())
        """
        if self.current:
            self.current.handle_events(events)

    def update(self, delta_time: float):
        """
        Updates the logic of the current scene.

        Args:
            delta_time (float): Time in seconds since the last frame, for smooth movement/animation.
        """
        if self.current:
            self.current.update(delta_time)

    def draw(self, surface: Surface):
        """
        Draws the current scene to the given surface (usually your game surface).

        Args:
            surface (pygame.Surface): Target surface to draw on.
        """
        if self.current:
            self.current.draw(surface)
