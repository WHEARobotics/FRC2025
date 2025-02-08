import wpilib
import commands2

from constants.operatorinterfaceconstants import OperatorInterfaceConstants
from subsystems.drive_subsystem import DriveSubsystem

class DriveWithJoystickCommand(commands2.Command): #Class type command from the libary command2
    def __init__(self, drive: DriveSubsystem, drive_percent_fn:callable): #What value this needs to run
        super().__init__()
        self.drive_subsystem = drive #Varible drive_subsystem is drive from __init__()
        self.drive_percent_fn = drive_percent_fn #Same concept as above

        self.addRequirements(drive) #Requires this subsystem

    def execute(self):  # What actions it does        
        turn_speed, drive_speed, rot_speed = self.drive_percent_fn() #Set turn and drive speed to values got from function
        self.drive_subsystem.drive(x_speed_inches_per_second=turn_speed, y_speed_inches_per_second=drive_speed, rot_speed_degrees_per_second=rot_speed) #Give these values to drive function

    def isFinished(self): #When something else happends then this is done, cause this is a default command
        return True

