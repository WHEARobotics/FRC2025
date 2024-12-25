import commands2

from sharkbot.util.ntloggerutility import NTLoggerUtility


class Vision(commands2.SubsystemBase):
    def __init__(self):
        self.logger = NTLoggerUtility("VisionLogs")
        self.logger.info("SubsystemStatus", "Initialized")

    def logPeriodic(self):
        self.logger.info("FnCall", "logPeriodic")