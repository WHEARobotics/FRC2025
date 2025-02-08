import commands2
import wpilib
from commands2.button import CommandXboxController
from wpimath import applyDeadband
from commands2 import RepeatCommand


from commands.print_something_command import PrintSomethingCommand
from constants.operatorinterfaceconstants import OperatorInterfaceConstants
from subsystems.drive_subsystem import DriveSubsystem
from commands.drive_forward_command import DriveForwardCommand
from commands.drive_with_joystick_command import DriveWithJoystickCommand
from commands.turn_to_angle_command import TurnToAngleCommand

# The `RobotContainer` class is where the robot's structure and behavior are defined.
# It is the glue that holds the robot together.
# Hardware-wise:
# * The `RobotContainer` has group of Subsystems. When you add or delete a complete
#   subsystem, you will need to update the `RobotContainer`.
# * The `RobotContainer` has one or more input controllers (e.g. Xbox controllers, joysticks).
#
# Command-wise:
# * The `RobotContainer` instantiates the Commands and CommandGroups that make
#   up the robot's behavior. These commands are created and wired together here
#  in the `RobotContainer`. If you ever want to review the robot's behavior, the
#  `RobotContainer` is the proper place to look. Even the autonomous and default commands
#   should be instantiated here.
#* The `RobotContainer` maps between the input devices and the Commands that operate on the Subsystems.
class RobotContainer:
    def __init__(self):
        self.drive_subsystem = DriveSubsystem() #Update the array when ready
        self.controller = CommandXboxController(OperatorInterfaceConstants.DRIVER_CONTROLLER_PORT)
        self.autonomous_command = DriveForwardCommand(self.drive_subsystem, duration=5)

        self.teleop_command = DriveWithJoystickCommand(self.drive_subsystem, self.get_drive_value_from_joystick)

        self.controller.a().onTrue(PrintSomethingCommand("WHEA A Button Pressed"))
        self.controller.b().whileTrue(TurnToAngleCommand(self.drive_subsystem, lambda: True)) #for quick test 

        self.drive_subsystem.setDefaultCommand(self.teleop_command) #Set the teleop command as the default for drive subsystem
    
    def get_auto_command(self) -> commands2.Command:
        return self.autonomous_command
    
    def get_drive_value_from_joystick(self) -> tuple[float, float, float]:
        x_percent = applyDeadband(value=self.controller.getLeftX(), deadband=0.1) #Apply deadband to the values above
        y_percent = applyDeadband(value=self.controller.getLeftY(), deadband=0.1)
        rot_percent = applyDeadband(value=self.controller.getRightX(), deadband=0.1)

        return x_percent, y_percent, rot_percent  #Gives us these variables when we call this function
    

