import unittest
from unittest.mock import MagicMock, patch
from commands2 import CommandScheduler
from commands2.button import JoystickButton
from sharkbot.robotsystems import RobotSystems
from sharkbot.constants.operatorinterfaceconstants import OperatorInterfaceConstants


class TestRobotSystems(unittest.TestCase):
    def setUp(self):
        # Patch the XboxController to mock its behavior
        self.controller_patch = patch("sharkbot.robotsystems.XboxController", autospec=True)
        self.MockXboxController = self.controller_patch.start()

        # Mock the controllers
        self.mock_driver_controller = self.MockXboxController.return_value
        self.mock_gunner_controller = self.MockXboxController.return_value

        # Initialize the RobotSystems class
        self.robot_systems = RobotSystems()

        # Replace controllers with mocks
        self.robot_systems.driver_controller = self.mock_driver_controller
        self.robot_systems.gunner_controller = self.mock_gunner_controller

        # Initialize the CommandScheduler
        self.scheduler = CommandScheduler.getInstance()

    def tearDown(self):
        # Stop the XboxController patch after each test
        self.controller_patch.stop()

    def simulate_button_press(self, controller, button, command_mock):
        """
        Simulates a button press and checks if the corresponding command is scheduled.
        """
        # Mock command instance
        command_instance = command_mock.return_value

        # Set up initial button state (not pressed)
        controller.getRawButton.side_effect = lambda b: b == button and False

        # Create a JoystickButton for the given button
        joystick_button = JoystickButton(controller, button)
        joystick_button.onTrue(command_instance)

        # Verify initial state: no commands scheduled
        self.scheduler.run()
        print(f"Scheduled commands after no press: {self.scheduler._scheduledCommands}")

        # Simulate button press
        controller.getRawButton.side_effect = lambda b: b == button and True
        self.scheduler.run()

        # Verify the mock command was scheduled
        command_instance.schedule.assert_called_once()
        print(f"Scheduled commands after button press: {self.scheduler._scheduledCommands}")

    @patch("commands.shooter.stopshooter.StopShooter")
    def test_gunner_controller_button_a_binding(self, mock_stop_shooter):
        """
        Test that BUTTON_A on the gunner_controller schedules StopShooter.
        """
        self.simulate_button_press(
            controller=self.robot_systems.gunner_controller,
            button=OperatorInterfaceConstants.BUTTON_A,
            command_mock=mock_stop_shooter
        )

