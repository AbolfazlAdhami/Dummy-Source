
class FahrenheitSensor:
    def get_temperature(self):
        return 45

class CelsiusSensor:
    def get_temperature_celsius(self):
        raise NotImplementedError

# Adapter
class TemperatureAdapter(CelsiusSensor):
    def __init__(self, fahrenheit_sensor: FahrenheitSensor):
        self._sensor = fahrenheit_sensor

    def get_temperature_celsius(self):
        f = self._sensor.get_temperature()
        return (f - 32) * 5 / 9


sensor = FahrenheitSensor()
adapter = TemperatureAdapter(sensor)
print(f"دما: {adapter.get_temperature_celsius():.1f} درجه سانتی‌گراد")