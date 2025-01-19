import wpilib
import commands2
from wpilib.buttons import JoystickButton

from robotsystems import RobotSystems

class Myrobot(wpilib.CommandRobot):
    '''Simple robot to drive motors for testing.
       Initially written for MAKO, but could easily be changed.
    '''
    def robotInit(self):
        self.systems = RobotSystems()
       
    # Every 20ms in all modes
    def robotPeriodic(self):
        # Run whatever command is next in the queue
        commands2.CommandScheduler.getInstance().run()

    def testInit(self):
        commands2.CommandScheduler.getInstance().cancelAll()

    def robotInit(self):
        pass

    def robotPeriodic(self):
        self.systems.periodic()

    def disabledPeriodic(self):
        if self.print_timer.advanceIfElapsed(0.2):
            wpilib.SmartDashboard.putString('DB/String 0', 'rotations: {:5.1f}'.format(self.kraken.get_position().value))

    def disabledExit(self):
        pass

    def autonomousInit(self):
        pass

    def autonomousPeriodic(self):
        pass

    def autonomousExit(self):
        pass

    def teleopInit(self):
        pass

    def teleopPeriodic(self):
        pass

    def teleopExit(self):
        pass


if __name__ == '__main__':
    wpilib.run(Myrobot)