from wpimath.geometry import Rotation2d
from wpimath.kinematics import SwerveModuleState


class SwerveModule:
    def __init__(self, drive_motor_id: int, turn_motor_id: int) -> None:
        """
        Initialize the swerve module.

        Parameters:
        - drive_motor_id: int - Motor controller ID for driving.
        - turn_motor_id: int - Motor controller ID for turning.
        """
        self.drive_motor = KrakenMotorController(drive_motor_id)
        self.turn_motor = KrakenMotorController(turn_motor_id)
        self.current_state = SwerveModuleState()

    def setDesiredState(self, state: SwerveModuleState) -> None:
        """
        Set the desired state for the swerve module.

        Parameters:
        - state: SwerveModuleState - Desired speed and angle.
        """
        # Optimize module state for minimal turning
        optimized_state = SwerveModuleState.optimize(state, self.getCurrentAngle())

        # Set motor speeds
        self.drive_motor.set(optimized_state.speed)
        self.turn_motor.setAngle(optimized_state.angle)

        # Update current state
        self.current_state = optimized_state

    def getState(self) -> SwerveModuleState:
        """
        Get the current state of the swerve module.

        Returns:
        - SwerveModuleState: Current speed and angle of the module.
        """
        return self.current_state

    def getCurrentAngle(self) -> Rotation2d:
        """
        Get the current angle of the swerve module **in degrees**.

        Returns:
        - Rotation2d: The module's current angle in degrees.
        """
        return self.turn_motor.getAngle()

    def stop(self) -> None:
        """
        Stop the swerve module.
        """
        self.drive_motor.stop()
        self.turn_motor.stop()
