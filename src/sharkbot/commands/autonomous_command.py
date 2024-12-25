
# See `MyContainer.getAutonomousCommand`
def AutonomousCommand(drive: DriveSubsystem):
    return (CircleCWForward(drive)
            .andThen(CircleCWBack(drive)))

# Behavior in commands. Simple states.
class CircleCWForward(commands2.CommandBase):
    def __init__(self, drive: DriveSubsystem):
        self.drive_system = drive
        self.addRequirements(drive)

        # Maybe you don't need this: can't you schedule a command to run for n seconds?
        self.timer = wpilib.Timer()

    def initialize(self):
        self.timer.start()
        self.drive_system.io.setLed(True)

    def execute(self):
        self.drive_system.drive(1.0, -0.5)

    def isFinished(self):
        return self.timer.get() > 2.0

    def end(self, interrupted: bool):
        self.drive_system.io.setLed(False)
        self.drive_system.drive(0, 0)


class CircleCWBack(commands2.CommandBase):
    def __init__(self, drive: DriveSubsystem):
        self.drive_system = drive
        self.addRequirements(drive)

        # Maybe you don't need this: can't you schedule a command to run for n seconds?
        self.timer = wpilib.Timer()

    def initialize(self):
        self.timer.start()
        self.drive_system.io.setLed(True)

    def execute(self):
        self.drive_system.drive(-1.0, -0.5)

    def isFinished(self):
        return self.timer.get() > 2.0

    def end(self, interrupted: bool):
        self.drive_system.io.setLed(False)
        self.drive_system.drive(0, 0)
