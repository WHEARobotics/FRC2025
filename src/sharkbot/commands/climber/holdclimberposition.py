import commands2

from sharkbot.subsystems.climber import Climber
from sharkbot.util.ntloggerutility import NTLoggerUtility


# The default command for the climber subsystem. This is the command that should be run when no other command is using the climber subsystem.
class HoldClimber(commands2.CommandBase):
    def __init__(self, climber: Climber):
        self.climber = climber
        self.addRequirements([self.climber])

        self.logger = NTLoggerUtility("ClimberLogs")

    def initialize(self):
        self.logger.info("Command", "HoldClimber initializing")

    def execute(self):
        # This should probably lock the climber in place, but we don't have any hardware to work with.
        self.logger.info("Command", "HoldClimber executing")
        pass

    def isFinished(self):
        self.logger.info("Command", "HoldClimber isFinished")
        return False

    def end(self):
        self.logger.info("Command", "HoldClimber ending")