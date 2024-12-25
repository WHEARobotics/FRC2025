class DriverStationSubsystem(commands2.SubsystemBase):
    def __init__(self):
        self.logger = NTLoggerUtility("DriverStationLogs")
        self.logger.info("SubsystemStatus", "Initialized")

    def logPeriodic(self):
        self.logger.info("FnCall", "logPeriodic")