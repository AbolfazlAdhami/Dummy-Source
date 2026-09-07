from abc import ABC, abstractmethod


class Device(ABC):
    @abstractmethod
    def is_enabled(self) -> bool: ...
    @abstractmethod
    def enable(self): ...
    @abstractmethod
    def disable(self): ...
    @abstractmethod
    def get_volume(self) -> int: ...
    @abstractmethod
    def set_volume(self, percent: int): ...
    @abstractmethod
    def get_channel(self) -> int: ...
    @abstractmethod
    def set_channel(self, channel: int): ...


class TV(Device):
    def __init__(self):
        self._on = False
        self._volume = 30
        self._channel = 1

    def is_enabled(self): return self._on
    def enable(self): self._on = True; print("TV is on")
    def disable(self): self._on = False; print("TV is off")
    def get_volume(self): return self._volume
    def set_volume(self, percent): self._volume = percent; print(
        f"TV volume: {percent}")

    def get_channel(self): return self._channel
    def set_channel(self, channel): self._channel = channel; print(
        f"TV channel: {channel}")


class Radio(Device):
    def __init__(self):
        self._on = False
        self._volume = 20
        self._channel = 88.5

    def is_enabled(self): return self._on
    def enable(self): self._on = True; print("Radio is on")
    def disable(self): self._on = False; print("Radio is off")
    def get_volume(self): return self._volume
    def set_volume(self, percent): self._volume = percent; print(
        f"Radio volume: {percent}")

    def get_channel(self): return self._channel
    def set_channel(self, channel): self._channel = channel; print(
        f"Radio frequency: {channel}")


class RemoteControl:
    def __init__(self, device: Device):
        self.device = device

    def toggle_power(self):
        if self.device.is_enabled():
            self.device.disable()
        else:
            self.device.enable()

    def volume_up(self):
        self.device.set_volume(self.device.get_volume() + 10)

    def volume_down(self):
        self.device.set_volume(self.device.get_volume() - 10)

    def channel_up(self):
        self.device.set_channel(self.device.get_channel() + 1)

    def channel_down(self):
        self.device.set_channel(self.device.get_channel() - 1)


class AdvancedRemoteControl(RemoteControl):
    def mute(self):
        self.device.set_volume(0)
