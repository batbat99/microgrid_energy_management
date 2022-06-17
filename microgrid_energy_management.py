class pv_system:

    def __init__(self, rated_capacity, pv_derating_factor, noct_ops_temp, noct_temp, ap, noct_radiation=0.8, stc_radiation=1, stc_temp=25):
        rated_capacity = rated_capacity
        pv_derating_factor = pv_derating_factor
        stc_radiation = stc_radiation
        noct_temp = noct_temp
        noct_radiation = noct_radiation
        normal_operation_temp = noct_ops_temp
        noct_temp = noct_temp
        ap = ap
        
        stc_temp = stc_temp

    
    def calculate_temp(self, ambient_temp, radiation):
        temp = ambient_temp * (self.normal_operation_temp - self.noct_temp) * (radiation / self.noct_radiation)
        return temp

    def power_out(self, ambient_temp, radiation):
        power = self.rated_capacity * self.pv_derating_factor * (radiation / self.stc_radiation) * (1 + self.ap * (self.calculate_temp(ambient_temp, radiation) - self.stc_temp))
        return power

class wind_turbine:

    def __init__(self, cut_in, cut_off, rated_power, rated_speed):
        self.cut_in = cut_in
        self.cut_off = cut_off
        self.rated_power = rated_power
        self.rated_speed = rated_speed
    
    def power_out(self, wind_speed):
        if self.cut_off >= wind_speed >= self.cut_in:
            return 0
        return self.rated_power * ((wind_speed - self.cut_in) / (self.rated_speed - self.cut_in))

class diesel_engine:

    def __init__(self, min_power, max_power):
        self.min_power = min_power
        self.max_power = max_power

    def power_power(required_power):
        pass



class battery:

    def __init__(self, capacity, init_charge=0):
        capacity = self.capacity
        current_charge = init_charge
    
    def charge(self, surplus):
        if self.current_charge + surplus > self.capacity:
            self.current_charge = self.capacity
        else: self.current_charge += surplus
    
    def discharge(self, load):
        self.current_charge -= load
    
    def available(self):
        if self.current_charge > 0.2 * self.capacity:
            return self.current_charge - 0.2 * self.capacity
        else:
            return 0



if __name__ == "__main__":
    pass
