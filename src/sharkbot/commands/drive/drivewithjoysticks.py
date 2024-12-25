import commands2
from wpilib import XboxController

from sharkbot.subsystems.drive import DriveSubsystem
from sharkbot.util.ntloggerutility import NTLoggerUtility


class DriveWithJoysticks(commands2.CommandBase):
    def __init__(self, drive: DriveSubsystem, controller: XboxController) -> None:
        super().__init__()
        self.drive = drive
        self.controller = controller
        self.addRequirements(drive)

        self.logger = NTLoggerUtility("DriveLogs")

    def execute(self) -> None:
        self.logger.info("Command", "DriveWithJoysticks executing")
        x_speed = -self.controller.getLeftY()
        y_speed = self.controller.getLeftX()
        rotation = self.controller.getRightX()

        self.drive.drive(x_speed, y_speed, rotation, field_relative=False)