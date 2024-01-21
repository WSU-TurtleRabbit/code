class Action:
    def __init__(self, vx: float, vy: float, omega: float, kick: bool, dribble: float):
        self.vx = float(vx)       # vx (m/s)
        self.vy = float(vy)       # vy (m/2)
        self.omega = float(omega) # angular velocity (rad/s)
        self.kick = bool(kick)    # activate kicker
        self.dribble = float(dribble) # -1 .. 1

    def calculate(self):
        self.v1 = self.v2 = self.v3 = self.v4 = 0

    def __call__(self):
        self.calculate()
        return self.v1, self.v2, self.v3, self.v4

    def __repr__(self):
        return f"Action={__class__}(vx={self.vx}, vy={self.vy}, omega={self.omega}, kick={self.kick}, dribble={self.dribble})"