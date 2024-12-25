from commands2 import CommandBase
from datetime import datetime

from sharkbot.util.ntloggerutility import NTLoggerUtility

class StopShooter(CommandBase):
    def __init__(self, shooter):
        """
               Command to stop the shooter subsystem.
        """
        super().__init__()
        self.shooter = shooter
        self.logger = NTLoggerUtility("ShooterLogs")
        self.addRequirements(shooter)

    def getTimestamp(self):
        return datetime.now().strftime("%H:%M:%S")

    def initialize(self):
        timestamp = self.getTimestamp()
        msg = f"[%{timestamp}] StopShooterCommand: Stopping shooter"
        self.logger.info("Command", msg)
        self.shooter.stop()

    def execute(self):
        timestamp = self.getTimestamp()
        msg = f"[%{timestamp}] Shooter flywheel RPM: {self.shooter.getFlywheelRpm()} \
        Gate status: {self.shooter.getGateStatus()}"
        self.logger.debug("Command", msg)

    def isFinished(self):
        flywheelRpm = self.shooter.getFlywheelRpm()
        gateStatus = self.shooter.getGateStatus()
        if flywheelRpm == 0 and gateStatus == "closed":
            return True
        else:
            return False

    def end(self):
        timestamp = self.getTimestamp()
        msg = f"[%{timestamp}] StopShooterCommand: Shooter stopped"
        self.logger.info("Command", msg)