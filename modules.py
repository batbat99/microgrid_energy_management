from matplotlib.style import available


class pv_system:

    def __init__(self, rated_capacity, pv_derating_factor, noct_ops_temp, noct_temp, ap, noct_radiation=0.8, stc_radiation=1, stc_temp=25, efficiency=0.2):
        self.rated_capacity = rated_capacity
        self.pv_derating_factor = pv_derating_factor
        self.stc_radiation = stc_radiation
        self.noct_temp = noct_temp
        self.noct_radiation = noct_radiation
        self.normal_operation_temp = noct_ops_temp
        self.noct_temp = noct_temp
        self.ap = ap
        self.efficiency = efficiency
        self.stc_temp = stc_temp

    def calculate_temp(self, ambient_temp, radiation):
        temp = ambient_temp + (self.normal_operation_temp -
                               self.noct_temp) * (radiation / self.noct_radiation) * (1 - self.efficiency / 0.9)
        return temp

    def power_out(self, ambient_temp, radiation):
        power = self.rated_capacity * self.pv_derating_factor * (radiation / self.stc_radiation) * (
            1 + self.ap * (self.calculate_temp(ambient_temp, radiation) - self.stc_temp))
        return power


class wind_turbine:

    def __init__(self, cut_in, cut_off, rated_power, rated_speed):
        self.cut_in = cut_in
        self.cut_off = cut_off
        self.rated_power = rated_power
        self.rated_speed = rated_speed

    def power_out(self, wind_speed):
        if self.cut_off <= wind_speed <= self.cut_in:
            return 0
        return self.rated_power * ((wind_speed - self.cut_in) / (self.rated_speed - self.cut_in))


class diesel_engine:

    def __init__(self, min_power, max_power, efficiency, fuel_tank):
        self.min_power = min_power
        self.max_power = max_power
        self.efficiency = efficiency
        self.fuel_tank = fuel_tank

    def power_out(self, required_power):
        available = self.fuel_tank * 10 * self.efficiency
        if available >= self.min_power:
            power = required_power
            if required_power < self.min_power:
                power = self.min_power
            elif required_power > self.max_power:
                power = self.max_power
            available -= power
            self.fuel_tank -= available / (10 * self.efficiency)
            return power


class battery:

    def __init__(self, capacity, efficiency, soc_min, soc_max, es_min, es_max, init_state=0):
        self.capacity = capacity
        self.soc = init_state
        self.efficiency = efficiency
        self.soc_min = soc_min
        self.soc_max = soc_max
        self.es_min = es_min
        self.es_max = es_max

    def power_exchange(self, est):
        es = est
        if abs(est) > self.es_max:
            es = self.es_max * es / abs(es)
        elif abs(est) < self.es_min:
            pass
        soct1 = self.soc - (self.efficiency * es) / self.capacity
        if not ((self.soc_min > soct1 and es > 0) or (soct1 > self.soc_max and es < 0)):
            self.soc -= soct1

            return es
        return 0


if __name__ == "__main__":
    pass
