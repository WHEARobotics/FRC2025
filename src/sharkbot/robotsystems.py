# This class is a container for all the robot's subsystems. This class will change only occasionally, when you
# add new subsystems or commands.
from commands2.button import JoystickButton
from wpilib import XboxController

from commands.shooter.stopshooter import StopShooter
from sharkbot.commands.autonomous_command import AutonomousCommand
from sharkbot.commands.climber.holdclimberposition import HoldClimber
from sharkbot.commands.drive.drivewithjoysticks import DriveWithJoysticks
from sharkbot.commands.shooter.idleshooter import IdleShooter
from sharkbot.commands.vision.passivevision import PassiveVision

from sharkbot.constants.operatorinterfaceconstants import OperatorInterfaceConstants

from sharkbot.subsystems.drive import DriveSubsystem
from sharkbot.subsystems.shooter import Shooter
from sharkbot.subsystems.driverstation import DriverStationSubsystem
from sharkbot.subsystems.climber import Climber
from sharkbot.subsystems.vision import Vision

import ntcore

# This class is a container for all the robot's subsystems. This class will change as new subsystems are added or removed.
class RobotSystems:
    def __init__(self):
        self.drive = DriveSubsystem()
        self.shooter = Shooter()
        self.driver_station = DriverStationSubsystem()
        self.climber = Climber()
        self.vision = Vision()

        # Initialize Controllers (These aren't subsystems because they're single pieces of hardware)
        self.driver_controller = XboxController(OperatorInterfaceConstants.DRIVER_CONTROLLER_PORT)
        self.gunner_controller = XboxController(OperatorInterfaceConstants.GUNNER_CONTROLLER_PORT)

        # Set Default Commands
        self.setDefaultCommands()

        # Configure Button Bindings
        self.configureButtonBindings()

    def setDefaultCommands(self) -> None:
        """
        Set default commands for each subsystem.
        """
        self.drive.setDefaultCommand(DriveWithJoysticks(self.drive, self.driver_controller))
        self.shooter.setDefaultCommand(IdleShooter(self.shooter))
        self.climber.setDefaultCommand(HoldClimber(self.climber))
        self.vision.setDefaultCommand(PassiveVision(self.vision))

    def configureButtonBindings(self) -> None:
        """
        Map controller buttons to specific commands.
        """
        # Driver Controller Bindings

        # Gunner Controller Bindings
        JoystickButton(self.gunner_controller, OperatorInterfaceConstants.BUTTON_A).onTrue(StopShooter(self.shooter))

    def getAutonomousCommand(self):
        """
        Returns the autonomous command to be scheduled during autonomous mode.
        """
        return AutonomousCommand(self.drive)

    def cancelAutonomousCommand(self) -> None:
        """
        Cancels the autonomous command if it is still running.
        """
        if self.getAutonomousCommand() and self.getAutonomousCommand().isScheduled():
            self.getAutonomousCommand().cancel()

    def setTeleopDefaultCommands(self) -> None:
        """
        Resets default commands during teleop mode (optional customization).
        """
        self.setDefaultCommands()
