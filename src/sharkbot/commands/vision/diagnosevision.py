from commands2 import Command
from util.ntloggerutility import NTLoggerUtility
import datetime

class diagnoseVision(Command):
    """ Command to diagnose the vision subsystem. Basically just checks if the Limelight is connected and the last update time"""
    def __init__(self, vision):           # <- Replace here
        """
        Get status of the vision subsystem.
        Args:
            vision: A variable holding a reference to the robot's vision subsystem
        """
        super().__init__()
        self.vision = vision
        self.logger = NTLoggerUtility("VisionSubsystem")
        self.addRequirements(vision)

    def getTimestamp(self):
        return datetime.now().strftime("%H:%M:%S")

    def initialize(self) -> None:
        """
        Called once when the Command is scheduled.

        Write's a timestamped message to the "Command" log in the `VisionSubystem` table that the command has been created.

        { Calls method in the subsystem to perform the action. } # < Replace here ("Calls shooter.stop() to stop the shooter subsystem.")
        """
        timestamp = self.getTimestamp()
        msg = f"[%{timestamp}] diagnoseVision: Get vision status"
        self.logger.info("Command", msg)


    def execute(self) -> None:
        """ Called repeatedly when this Command is running.

           Gets the limelight status
        """
        timestamp = self.getTimestamp()
        status = self.vision.diagnose()
        msg = f"[%{timestamp}] Vision: {status}"
        self.logger.debug("Command", msg)

    def isFinished(self) -> bool:
        """
        Called repeatedly when this Command is running.

        :return: `True` if the Command should end, `False` otherwise.
        """
        # This command should only run once
        return True

    def end(self, interrupted: bool) -> None:
        """
        Called once when the Command ends (because `isFinished()` returned `True`) or is interrupted.
        :param self: This Command instance.
        :param interrupted: `True` if the Command was interrupted, `False` otherwise.
        :return:
        """
        timestamp = self.getTimestamp()
        if interrupted:
            msg = f"[%{timestamp}] DiagnoseVision command was interrupted"
        else:
            msg = f"[%{timestamp}] DiagnoseVision command completed"
        self.logger.info("Command", msg)