import wpilib
from wpilib.buttons import JoystickButton
import phoenix6

from subsystems.drivesubsystem import DriveSubsystem
from constants.operatorinterfaceconstants import OperatorInterfaceConstants

from commands.commands import PositionRequest, MotionMagicPositionRequest, BrakeRequest

class RobotSystems:
    def __init__(self):
        self.xbox = wpilib.XboxController(2)
        # Eventually this would include Elevator, Intake, etc. subsystems
        self.subsystems = [DriveSubsystem()]

      
        # Configure joystick buttons
        JoystickButton(self.xbox, OperatorInterfaceConstants.RIGHT_BUMPER).onTrue(
            PositionRequest(self.drive, self.desired_rotations).schedule())
        JoystickButton(self.xbox, OperatorInterfaceConstants.LEFT_BUMPER).onTrue(
            MotionMagicPositionRequest(self.drive, self.desired_rotations).schedule())
    
    def periodic(self):
        # Get control values and set desired rotations
        right = self.xbox.getRightY()
        self.desired_rotations = self.rotations_from_control(right)
        
        for subsystem in self.subsystems:
            subsystem.periodic()
        self.periodic_output()

    

    @staticmethod
    def rotations_from_control(control):
        desired_rotations = control * 5
        if abs(desired_rotations) <= 0.1:
            desired_rotations = 0
        return desired_rotations
