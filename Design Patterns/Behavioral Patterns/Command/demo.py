from abc import ABC, abstractmethod
from typing import List


# Receiver
class Light:
    def __init__(self, location: str) -> None:
        self.location = location
        self.is_on = False

    def on(self) -> None:
        self.is_on = True
        print(f"{self.location} light is ON")

    def off(self) -> None:
        self.is_on = False
        print(f"{self.location} light is OFF")


class Stereo:
    def __init__(self, location: str) -> None:
        self.location = location
        self.volume = 0

    def on(self) -> None:
        print(f"{self.location} stereo is ON")

    def off(self) -> None:
        print(f"{self.location} stereo is OFF")

    def set_volume(self, volume: int) -> None:
        self.volume = volume
        print(f"{self.location} stereo volume set to {volume}")


# Command interface
class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod
    def undo(self) -> None:
        pass


# Concrete Commands
class LightOnCommand(Command):
    def __init__(self, light: Light) -> None:
        self.light = light

    def execute(self) -> None:
        self.light.on()

    def undo(self) -> None:
        self.light.off()


class LightOffCommand(Command):
    def __init__(self, light: Light) -> None:
        self.light = light

    def execute(self) -> None:
        self.light.off()

    def undo(self) -> None:
        self.light.on()


class StereoOnWithCDCommand(Command):
    def __init__(self, stereo: Stereo) -> None:
        self.stereo = stereo

    def execute(self) -> None:
        self.stereo.on()
        self.stereo.set_volume(11)

    def undo(self) -> None:
        self.stereo.set_volume(0)
        self.stereo.off()


class NoCommand(Command):
    """Null Object – used when a slot has no command assigned."""

    def execute(self) -> None:
        pass

    def undo(self) -> None:
        pass


# Invoker
class RemoteControl:
    def __init__(self) -> None:
        self.on_commands: List[Command] = [NoCommand()] * 7
        self.off_commands: List[Command] = [NoCommand()] * 7
        self.undo_command: Command = NoCommand()

    def set_command(self, slot: int, on_command: Command, off_command: Command) -> None:
        self.on_commands[slot] = on_command
        self.off_commands[slot] = off_command

    def on_button_pressed(self, slot: int) -> None:
        self.on_commands[slot].execute()
        self.undo_command = self.on_commands[slot]

    def off_button_pressed(self, slot: int) -> None:
        self.off_commands[slot].execute()
        self.undo_command = self.off_commands[slot]

    def undo_button_pressed(self) -> None:
        self.undo_command.undo()


# Client
if __name__ == "__main__":
    remote = RemoteControl()

    living_room_light = Light("Living Room")
    kitchen_light = Light("Kitchen")
    stereo = Stereo("Living Room")

    living_room_light_on = LightOnCommand(living_room_light)
    living_room_light_off = LightOffCommand(living_room_light)
    kitchen_light_on = LightOnCommand(kitchen_light)
    kitchen_light_off = LightOffCommand(kitchen_light)
    stereo_on = StereoOnWithCDCommand(stereo)
    stereo_off = LightOffCommand(living_room_light)  # placeholder for demo

    # Assign commands to slots
    remote.set_command(0, living_room_light_on, living_room_light_off)
    remote.set_command(1, kitchen_light_on, kitchen_light_off)
    remote.set_command(2, stereo_on, stereo_off)

    print("--- Turning devices ON ---")
    remote.on_button_pressed(0)
    remote.on_button_pressed(1)
    remote.on_button_pressed(2)

    print("\n--- Turning devices OFF ---")
    remote.off_button_pressed(0)
    remote.off_button_pressed(1)

    print("\n--- Undo last command ---")
    remote.undo_button_pressed()
