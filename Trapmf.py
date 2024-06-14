from Point import Point

class Trapmf :

    def __init__(self, p1, p2, p3, p4):
        
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4

    def calculate(self, x):

        # x <= a
        if x <= self.p1.x:
            if self.p1.x == self.p2.x: 
                return 1
            else:
                return 0

        # a <= x <= b
        if self.p1.x <= x <= self.p2.x: 
            m = Point.get_slope(self.p1, self.p2)
            b = Point.get_intercept(self.p1, self.p2)
            return m * x + b

        # b <= x <= c
        if self.p2.x <= x <= self.p3.x: 
            return 1

        # c <= x <= d
        if self.p3.x <= x <= self.p4.x:
            m = Point.get_slope(self.p3, self.p4)
            b = Point.get_intercept(self.p3, self.p4)
            return m * x + b

        # x >= d
        if x >= self.p4.x:
            if self.p3.x == self.p4.x:
                return 1
            else:
                return 0