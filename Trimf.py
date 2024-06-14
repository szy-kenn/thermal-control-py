from Point import Point

class Trimf :

    def __init__(self, p1, p2, p3):
        
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    def calculate(self, x):

        # x <= a
        if x <= self.p1.x:
            return 0

        # a <= x <= b
        if self.p1.x <= x <= self.p2.x: 
            m = Point.get_slope(self.p1, self.p2)
            b = Point.get_intercept(self.p1, self.p2)
            return m * x + b

        # b <= x <= c
        if self.p2.x <= x <= self.p3.x:
            m = Point.get_slope(self.p2, self.p3)
            b = Point.get_intercept(self.p2, self.p3)
            return m * x + b

        # x >= c
        if x >= self.p3.x:
            return 0