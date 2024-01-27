
class Action:
    def __init__(self, vx: float, vy: float, omega: float, kick: bool, dribble: float):
        """_summary_
            Object for initialise action commands, encode / decode strings for UDP transportation.
        Args:
            vx (float): wanted velocity for x direction
            vy (float): wanted velocity for y direction
            omega (float): wanted angular velocity (radians)
            kick (bool): wanted kicker to kick (Yes/No)
            dribble (float): dribbling speed ? 
        """
        self.vx = vx
        self.vy = vy
        self.omega = omega
        self.kick = kick
        self.dribble = dribble

    @classmethod
    def decode(cls): 
        pass
    
    @classmethod
    def encode(cls):
        pass

    def __repr__(self):
        return f"Action: (vx: {self.vx}, vy: {self.vy}, theta: {self.omega}, kick: {self.kick}, dribble: {self.dribble})"
    