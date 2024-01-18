class Action:
    def __init__(self, vx, vy, omega, kick, dribble):
        self.vx = float(vx)       # vx (m/s)
        self.vy = float(vy)       # vy (m/2)
        self.omega = float(omega) # angular velocity (rad/s)
        self.kick = bool(kick)    # activate kicker
        self.dribble = float(dribble) # -1 .. 1

    def __repr__(self):
        return f"Action(vx={self.vx}, vy={self.vy}, omega={self.omega}, kick={self.kick}, dribble={self.dribble})"

