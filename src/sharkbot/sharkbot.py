import logging

import wpilib
import wpilib.drive
import commands2

import ntcore

from sharkbot.robotsystems import RobotSystems
from sharkbot.commands.autonomous_command import AutonomousCommand

# This is the "entry point" for the robot code. It's the first thing that runs.
# This file should rarely, if ever, change
class Sharkbot(wpilib.TimedRobot):
    def robotInit(self):
        self.systems = RobotSystems()
        self.autonomous_command = AutonomousCommand(self.systems.drive)

    # Every 20ms in all modes
    def robotPeriodic(self):
        logging.debug("robotPeriodic")

        # Flush NetworkTables
        ntcore.flush()

        # Log all subsystems
        for system in self.systems:
            system.log_periodic()

        # Run whatever command is next in the queue
        commands2.CommandScheduler.getInstance().run()

    def autonomousInit(self):
        if self.autonomous_command:
            self.autonomous_command.schedule()

    def teleopInit(self):
        if self.autonomous_command:
            self.autonomous_command.cancel()

    def testInit(self):
        commands2.CommandScheduler.getInstance().cancelAll()

