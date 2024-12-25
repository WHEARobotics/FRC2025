from sharkbot.util.ntloggerutility import NTLoggerUtility


class Climber(commands2.SubsystemBase):
    def __init__(self):
        self.logger = NTLoggerUtility("ClimberLogs")
        self.logger.info("SubsystemStatus", "Initialized")

   def logPeriodic(self):
        self.logger.info("FnCall", "logPeriodic")