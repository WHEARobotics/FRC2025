class IdleShooter(CommandBase):
    def __init__(self, shooter: Shooter):
        self.shooter = shooter
        self.addRequirements(shooter)

    def initialize(self):
        self.shooter.stop()

    def isFinished(self):
        return False