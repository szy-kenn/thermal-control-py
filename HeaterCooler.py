import random

class Heater_Cooler:
    def __init__(self):
        self.type = None

    def update_temp(self, actual_temp, output_type):
        self.type = output_type

        if self.type == "H":
            # return actual_temp + 0.5
            return round(actual_temp + random.randrange(20, 100, 20) / 100, 2)

        if self.type == "C":
            # return actual_temp - 0.5
            return round(actual_temp - random.randrange(20, 100, 20) / 100, 2)

        return actual_temp