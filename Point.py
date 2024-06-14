class Point:

    @classmethod
    def get_slope(cls, p1, p2):
        return (p2.y - p1.y) / (p2.x - p1.x)

    @classmethod
    def get_intercept(cls, p1, p2):
        return p1.y - (cls.get_slope(p1, p2) * p1.x)

    def __init__(self, x, y):
        self.x = x
        self.y = y
