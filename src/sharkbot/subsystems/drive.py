# Definitely changes w hardware, but rarely after build (?)
from sharkbot.util.ntloggerutility import NTLoggerUtility


class DriveSubsystem(commands2.SubsystemBase):
    def __init__(self):
        self.logger = NTLoggerUtility("DriveLogs")
        self.logger.info("SubsystemStatus", "Initialized")

    def drive(self, speed: float, rotation: float):
        self.logger.info("FnCall", f"drive({speed}, {rotation})")
        self.driver.arcadeDrive(speed, rotation)

    def logPeriodic(self):
        self.logger.info("FnCall", "logPeriodic")