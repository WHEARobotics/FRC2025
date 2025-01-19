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

        # This is updated periodically from the joystick
        self.desired_rotations = 0

        # Because original code output every 200ms and loop runs every 20ms...
        self.output_every_n_seconds = 0.2
        # ... we keep this counter that runs from 1 to 10 (see periodic_output() below)
        self.periodic_has_run_n_times = 0

        # Configure joystick buttons
        JoystickButton(self.xbox, OperatorInterfaceConstants.RIGHT_BUMPER).onTrue(
            PositionRequest(self.drive, self.desired_rotations).schedule())
        JoystickButton(self.xbox, OperatorInterfaceConstants.LEFT_BUMPER).onTrue(
            MotionMagicPositionRequest(self.drive, self.desired_rotations).schedule())
    
    def periodic(self):
        # Get control values and set desired rotations
        right = self.xbox.getRightY()
        self.desired_rotations = self.rotations_from_control(right)
        
        self.periodic_output()

    def periodic_output(self):
        # This fn is called every 20ms in all modes
        times_to_run = self.output_every_n_seconds // 0.02 #(20ms)

        # Have we looped enough times to update the dashboard?
        if self.periodic_has_run_n_times % times_to_run == 0:
            wpilib.SmartDashboard.putString('DB/String 0', 'rotations: {:5.1f}'.format(self.kraken.get_position().value))
            # Reset the counter
            self.periodic_has_run_n_times = 0
        else:
            self.periodic_has_run_n_times += 1

    @staticmethod
    def rotations_from_control(control):
        desired_rotations = control * 5
        if abs(desired_rotations) <= 0.1:
            desired_rotations = 0
        return desired_rotations
