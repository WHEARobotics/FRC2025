import commands2

from sharkbot.util.ntloggerutility import NTLoggerUtility


class Shooter(commands2.SubsystemBase):
    def __init__(self):
        self.logger = NTLoggerUtility("ShooterLogs")
        self.logger.info("SubsystemStatus", "Initialized")

    def logPeriodic(self):
        self.logger.info("FnCall", "logPeriodic")