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


if __name__ == "__main__":
    pv = pv_system(rated_capacity=8, pv_derating_factor=0.6, noct_ops_temp=45,
                   noct_temp=20, ap=0.48, noct_radiation=0.8, stc_radiation=1, stc_temp=25)
    wt = wind_turbine(cut_in=3, cut_off=25, rated_power=70, rated_speed=11)
    de = diesel_engine(min_power=80, max_power=300)
    b = battery(capacity=15, efficiency=0.9, soc_min=3,
                soc_max=13.5, es_min=0, es_max=3, init_state=0)
    circuitb = {1: 1, 2: 2, 3: 3, 4: 4}
    mms = microgrid_management_system(pv, wt, de, b, circuitb)
    loads = {1: 10, 2: 30, 3: 40, 4: 40}
    print(mms.drive(loads, 30, radiation=1.369,
          wind_speed=14, grid=False, diesel=True))
