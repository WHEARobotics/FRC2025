import commands2

from sharkbot.util.ntloggerutility import NTLoggerUtility


class Shooter(commands2.SubsystemBase):
    def __init__(self):
        self.logger = NTLoggerUtility("ShooterLogs")
        self.logger.info("SubsystemStatus", "Initialized")
        self.flywheelMotor = None # Say
        self.gate = None    # Say

    def logPeriodic(self):
        self.logger.info("FnCall", "logPeriodic")

    def stop(self):
        self.flywheelMotor.stop()
        self.gate.close()

    def getFlywheelRpm(self):
        return self.flywheelMotor.getRpm()

    def getGateStatus(self):
        return self.gate.getStatus()