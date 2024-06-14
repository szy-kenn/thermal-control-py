from ThermalFuzzy import ThermalFuzzy
from HeaterCooler import Heater_Cooler
from Trapmf import Trapmf
from Trimf import Trimf
from Point import Point
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline, BSpline
import numpy as np

class ThermalControl:

    def __init__(self, error_neg, error_zero, error_pos, 
                 error_dot_neg, error_dot_zero, error_dot_pos, 
                 cooler, no_change, heater) -> None:
        self.thermal_fuzzy = ThermalFuzzy(error_neg, error_zero, error_pos, 
                                          error_dot_neg, error_dot_zero, error_dot_pos, 
                                          cooler, no_change, heater)
        self.heater_cooler = Heater_Cooler()

        self.prev_error = None
        self.current_error = None
        self.error_dot = None
        self.actual_temp = None
        self.desired_temp = None
        self.plots = []

    def start(self):

        self.actual_temp = float(input("Enter the actual temperature: "))
        self.desired_temp = float(input("Enter your desired temperature: "))
        output_type = None

        while self.actual_temp != self.desired_temp:

            self.current_error = self.desired_temp - self.actual_temp

            if self.prev_error is None:
                self.prev_error = self.current_error

            self.error_dot = self.prev_error - self.current_error
            output_type = self.thermal_fuzzy.process_input(self.current_error, self.error_dot)
            self.actual_temp = self.heater_cooler.update_temp(self.actual_temp, output_type)
            print(f"Output: {output_type} | Actual Temp: {self.actual_temp}")
            self.prev_error = self.current_error
            self.plots.append(self.current_error)

        self.plots.append(self.desired_temp - self.actual_temp)
        self.show_plot()

    def show_plot(self):
        x = np.array(range(len(self.plots)))
        y = self.plots

        xnew = np.linspace(x.min(), x.max(), 300)
        spl = make_interp_spline(x, y, k=3) # type: BSpline
        y_smooth = spl(xnew)

        plt.plot([0, len(self.plots)], [0, 0], marker = 'o', linestyle="dashed")
        plt.plot(xnew, y_smooth)
        plt.xlabel("Time")
        plt.ylabel("Error")
        plt.ylim(max(abs(plot) for plot in self.plots), max(abs(plot) for plot in self.plots) * -1)
        plt.show()


# membership functions
error_neg = Trapmf(Point(-4, 0), Point(-4, 1), Point(-2, 1), Point(0, 0))
error_zero = Trimf(Point(-2, 0), Point(0, 1), Point(2, 0))
error_pos = Trapmf(Point(0, 0), Point(2, 1), Point(4, 1), Point(4, 0))

error_dot_neg = Trapmf(Point(-10, 0), Point(-10, 1), Point(-5, 1), Point(0, 0))
error_dot_zero = Trimf(Point(-5, 0), Point(0, 1), Point(5, 0))
error_dot_pos = Trapmf(Point(0, 0), Point(5, 1), Point(10, 1), Point(10, 0))

cooler = Trapmf(Point(-100, 0), Point(-100, 1), Point(-50, 1), Point(0, 0))
no_change = Trimf(Point(-50, 0), Point(0, 1), Point(50, 0))
heater = Trapmf(Point(0, 0), Point(50, 1), Point(100, 1), Point(100, 0))


thermal_control = ThermalControl(error_neg, error_zero, error_pos, 
                                 error_dot_neg, error_dot_zero, error_dot_pos, 
                                 cooler, no_change, heater)
thermal_control.start()