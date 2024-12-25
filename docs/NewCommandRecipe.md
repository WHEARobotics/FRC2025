# Recipe for creating new Commands

## Overview

Commands are the building blocks of the robot's behavior. They are small pieces of code that perform a specific task. 
For example, an `IdleShooterCommand` class might be responsible for putting the flywheel in it's resting state
(perhaps stopped or perhaps spinning slowly). 

## Steps

1. Determine which subsystem the new command primarily works on. When you send this command, what is it logically doing?
Which subsystem do you think about? For example, if you think "I want to stop the shooter", then the command belongs to 
the `Shooter` subsystem." If you can't think of a subsystem that the command belongs to, then maybe the behavior should 
be a utility function in the `utilities` directory rather than a command.
2. Create a new Python file in the `commands/{subsystem}` directory. The file name should be the name of the command, with the word 
`Command` appended to the end. For example, `commands/shooter/IdleShooterCommand.py`.
2. Create a new class in the file. The class should inherit from the `CommandBase` class.
3. In the class, implement the `__init__` method. In this method, you should call the `requires` method and pass in the
3. Implement the `initialize`, `execute`, `isFinished`, and `end` methods. 
4. If the new command is a default command for a subsystem, add it to the subsystem's `default_command` attribute in the
`RobotSystems` class.

## Example

1. Q: To which subsystem should we send this Command? "We want to fully stop the **shooter**."  A: (The `Shooter` subsystem)
2. Design the Command's state machine for the desired behavior "We want this command to wait
until the shooter is fully stopped. Only then is the command truly over. We want to track the shooter's RPM as it 
slows.":
   - **Initialize**: When the command is first called, it should start stopping the shooter.
   - **Execute**: The command should log the current RPM of the shooter's motors as it slows.
   - **IsFinished**: Are all the shooter's motors fully stopped?
   - **End**: The command should log that the shooter has stopped.

3. In the `commands/shooter` directory, create a new file called `stopshootercommand.py` This file should be named using lower-
case, not SnakeCase.
3. In the file, create a new class called `StopShooterCommand` that inherits from `CommandBase`. Import any modules that
you need. (For example, `datetime` for logging the current time.)

4. In the class, implement the `__init__` method. In this method, you should call the `requires` method and pass in the
   `Shooter` subsystem. You should also create a logger object using the `NTLoggerUtility` class.
```python
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
```

5. Implement the `initialize`, `execute`, `isFinished`, and `end` methods that we designed earlier. Implement any 
additional methods that you might need. For example, if you want to add timestamps to your log messages, you might want
to create a `getTimestamp` method that returns the current time in a specific format. (Would this method be better 
located in a utility class? Probably!) (Notice that we use different log levels for different messages. We probably 
always to log when the command starts and ends, but we only want to log the shooter's RPM when we're debugging the )
```python
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
```

6. If necessary, add the relevant hardware-related methods to the `Shooter` subsystem. For example, you might need to add
a `stop` method to the `Shooter` class. 
```python
    def stop(self):
        self.flywheelMotor.stop()
        self.gate.close()

    def getFlywheelRpm(self):
        return self.flywheelMotor.getRpm()

    def getGateStatus(self):
        return self.gate.getStatus()
```
7. Implement tests for the new command in the `tests` directory (See the `NewTestRecipe.md`). For example, this is 
complex, but you might want:

```python
import unittest
from unittest.mock import MagicMock
import re
from commands.shooter.stopshooter import StopShooter


class TestStopShooterCommand(unittest.TestCase):
    def setUp(self):
        # Mock the shooter subsystem
        self.shooter = MagicMock()
        self.shooter.getFlywheelRpm.return_value = 1234  # Example RPM value
        self.shooter.getGateStatus.return_value = "open"  # Example gate status

        # Mock logger
        self.logger = MagicMock()

        # Create StopShooter instance
        self.command = StopShooter(self.shooter)
        self.command.logger = self.logger  # Replace with mocked logger

    def assert_log_message(self, actual_message, expected_pattern):
        """
        Assert that a log message matches the expected regex pattern.

        Parameters:
        - actual_message: The actual log message.
        - expected_pattern: A regex pattern to match the log message.
        """
        match = re.match(expected_pattern, actual_message)
        self.assertIsNotNone(
            match,
            msg=f"Log message '{actual_message}' does not match pattern '{expected_pattern}'",
        )

    def test_initialize(self):
        # Call the initialize method
        self.command.initialize()

        # Verify the shooter stop method is called
        self.shooter.stop.assert_called_once()

        # Verify the logger logs the correct message
        expected_pattern = r"\[%\d{2}:\d{2}:\d{2}\] StopShooterCommand: Stopping shooter"
        actual_message = self.logger.info.call_args[0][1]  # Extract logged message
        self.assert_log_message(actual_message, expected_pattern)

    def test_execute(self):
        # Call the execute method
        self.command.execute()

        # Verify the logger logs the correct message
        expected_pattern = (
            r"\[%\d{2}:\d{2}:\d{2}\] Shooter flywheel RPM: 1234\s+"
            r"Gate status: open"
        )
        actual_message = self.logger.debug.call_args[0][1]  # Extract logged message
        self.assert_log_message(actual_message, expected_pattern)

    def test_end(self):
        # Call the end method
        self.command.end()

        # Verify the logger logs the correct message
        expected_pattern = r"\[%\d{2}:\d{2}:\d{2}\] StopShooterCommand: Shooter stopped"
        actual_message = self.logger.info.call_args[0][1]  # Extract logged message
        self.assert_log_message(actual_message, expected_pattern)
```

8. Implement the test for the binding of the command to the control system. For example:

```python
import unittest

from sharkbot.commands.shooter.stopshooter import StopShooter
from robot import RobotSystems

