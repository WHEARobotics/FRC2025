import unittest
from unittest.mock import MagicMock, patch
from commands2 import CommandScheduler, CommandBase
from commands2.button import JoystickButton
from sharkbot.robotsystems import RobotSystems
from sharkbot.constants.operatorinterfaceconstants import OperatorInterfaceConstants
from commands.shooter.stopshooter import StopShooter


class TestRobotSystems(unittest.TestCase):
    def setUp(self):
        # Patch the XboxController to mock its behavior
        self.controller_patch = patch("sharkbot.robotsystems.XboxController", autospec=True)
        self.MockXboxController = self.controller_patch.start()

        # Mock the controller instance
        self.mock_controller = self.MockXboxController.return_value
        self.mock_controller.getRawButton = MagicMock()

        # Initialize the RobotSystems class
        self.robot_systems = RobotSystems()

        # Replace gunner_controller with the mocked controller
        self.robot_systems.gunner_controller = self.mock_controller

        # Initialize the CommandScheduler
        self.scheduler = CommandScheduler.getInstance()

    def tearDown(self):
        # Stop the XboxController patch after each test
        self.controller_patch.stop()

    @patch("commands.shooter.stopshooter.StopShooter")
    def test_robot_systems_button_binding(self, mock_stop_shooter):
        # Mock command instance
        mock_command_instance = mock_stop_shooter.return_value

        # Set up initial button state (not pressed)
        self.mock_controller.getRawButton.side_effect = lambda button: False

        # Create a JoystickButton for BUTTON_A
        button = JoystickButton(self.robot_systems.gunner_controller, OperatorInterfaceConstants.BUTTON_A)
        button.onTrue(mock_command_instance)

        # Verify initial state: no commands scheduled
        self.scheduler.run()
        print(f"Scheduled commands after no press: {self.scheduler._scheduledCommands}")

        # Simulate button press
        self.mock_controller.getRawButton.side_effect = lambda button: button == OperatorInterfaceConstants.BUTTON_A
        self.scheduler.run()

        # Verify the mock command was scheduled
        mock_command_instance.schedule.assert_called_once()
        print(f"Scheduled commands after button press: {self.scheduler._scheduledCommands}")
