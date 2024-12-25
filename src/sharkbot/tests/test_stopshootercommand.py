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
