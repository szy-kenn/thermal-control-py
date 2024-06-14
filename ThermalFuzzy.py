class ThermalFuzzy:

    def __init__(self, error_neg, error_zero, error_pos,
                 error_dot_neg, error_dot_zero, error_dot_pos,
                 cooler, no_change, heater):
        self.error_neg = error_neg
        self.error_zero = error_zero
        self.error_pos = error_pos
        self.error_dot_neg = error_dot_neg
        self.error_dot_zero = error_dot_zero
        self.error_dot_pos = error_dot_pos
        self.cooler = cooler
        self.no_change = no_change
        self.heater = heater

    def process_input(self, error, error_dot):
        fuzzy_error, fuzzy_error_dot = self.fuzzify(error, error_dot)
        cooler, no_change, heater = self.apply_rules(fuzzy_error, fuzzy_error_dot)
        aggregated_values = self.aggregate(cooler, no_change, heater)
        output = self.defuzzify(aggregated_values, no_change)
        return output

    def fuzzify(self, error_val, error_dot_val):
        error_fuzzified = [
            self.error_neg.calculate(error_val),
            self.error_zero.calculate(error_val),
            self.error_pos.calculate(error_val)
        ]

        error_dot_fuzzified = [
            self.error_dot_neg.calculate(error_dot_val),
            self.error_dot_zero.calculate(error_dot_val),
            self.error_dot_pos.calculate(error_dot_val)
        ]

        return [error_fuzzified, error_dot_fuzzified]

    def apply_rules(self, error_fuzzified, error_dot_fuzzified):

        pp = min(error_fuzzified[2], error_dot_fuzzified[2])
        pz = min(error_fuzzified[2], error_dot_fuzzified[1])
        pn = min(error_fuzzified[2], error_dot_fuzzified[0])

        zp = min(error_fuzzified[1], error_dot_fuzzified[2])
        zz = min(error_fuzzified[1], error_dot_fuzzified[1])
        zn = min(error_fuzzified[1], error_dot_fuzzified[0])

        np = min(error_fuzzified[0], error_dot_fuzzified[2])
        nz = min(error_fuzzified[0], error_dot_fuzzified[1])
        nn = min(error_fuzzified[0], error_dot_fuzzified[0])

        applied_rules = [pp, pz, pn, zn, zp, np, nz, nn, zz]

        heater =  max(applied_rules[0:4])
        cooler =  max(applied_rules[4:8])
        no_change = applied_rules[8]

        return [cooler, no_change, heater]

    def aggregate(self, cooler, no_change, heater):
        return list(
            max(min(self.cooler.calculate(i - 100), cooler),
                 min(self.no_change.calculate(i - 100), no_change), 
                 min(self.heater.calculate(i - 100), heater))
                for i in range(201)
        )

    def defuzzify(self, aggregated_values, no_change):
        sum_y = 0
        sum_xy = 0

        for i in range(len(aggregated_values)):
            sum_y += aggregated_values[i]
            sum_xy += (i - 100) * aggregated_values[i]

        cog = sum_xy / sum_y
        output_type =  "NC" if no_change == 1 else "C" if cog <= 0 else "H"
        return output_type

