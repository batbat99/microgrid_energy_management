from modules import *


class microgrid_management_system:

    def __init__(self, pv_system: pv_system, wind_turbine: wind_turbine, diesel_engine: diesel_engine, battery: battery, cbp: dict):
        self.pv_system = pv_system
        self.wind_turbine = wind_turbine
        self.diesel_engine = diesel_engine
        self.battery = battery
        self.cbp = cbp

    def _breaker_action(self, power_diff, loads):
        breakers = sorted(self.cbp, key=self.cbp.get, reverse=True)
        cbp_activation = {key: 1 for key in self.cbp.keys()}
        for breaker in breakers:
            cbp_activation[breaker] = 0
            power_diff -= loads[breaker]
            if power_diff <= 0:
                break
        return power_diff, cbp_activation

    def drive(self, loads: dict, ambient_temp, radiation, wind_speed, grid: bool, diesel: bool):
        cbp_activation = {key: 1 for key in self.cbp.keys()}
        power_bus = {"pv": 0, "wind": 0, "diesel": 0, "battery": 0, "grid": 0}
        total_load = sum(loads.values())

        pv_power = self.pv_system.power_out(ambient_temp, radiation)
        power_bus["pv"] = pv_power
        wind_power = self.wind_turbine.power_out(wind_speed)
        power_bus["wind"] = wind_power
        renewable_power = pv_power + wind_power

        power_diff = total_load - renewable_power

        if renewable_power >= total_load:
            est = power_diff
            power_exchanged = self.battery.power_exchange(est)
            power_bus["battery"] = power_exchanged
            excess = power_diff - power_exchanged
            power_bus["grid"] = excess
        elif not grid:
            if diesel:
                diesel_power = self.diesel_engine.power_out(power_diff)
                power_bus["diesel"] = diesel_power
                power_diff -= diesel_power
                if power_diff > 0:
                    power_exchanged = self.battery.power_exchange(power_diff)
                    power_bus["battery"] = power_exchanged
                    power_diff -= power_exchanged
                    if power_diff > 0:
                        power_diff, cbp_activation = self._breaker_action(
                            power_diff, loads)
        else:
            power_bus["grid"] = power_diff
        return cbp_activation, power_bus
