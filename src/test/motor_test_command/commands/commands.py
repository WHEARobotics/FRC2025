import commands2

class NeutralRequest(CommandBase):
    def __init__(self, drive):
        super().__init__()
        self.drive = drive
        self.addRequirements(self.drive)

    def execute(self):
        self.drive.set_to_neutral()


    def isFinished(self):
        return True
    
class PositionRequest(CommandBase):
    def __init__(self, drive, position):
        super().__init__()
        self.drive = drive
        self.position = position
        self.addRequirements(self.drive)

    def execute(self):
        self.drive.set_position(self.position)

    def isFinished(self):
        return True
    
class MotionMagicPositionRequest(CommandBase):
    def __init__(self, drive, position):
        super().__init__()
        self.drive = drive
        self.position = position
        self.addRequirements(self.drive)

    def execute(self):
        self.drive.set_position(self.position)
        
  
    def isFinished(self):
        return True
