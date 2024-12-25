from wpilib import Gyro
from wpimath.geometry import Rotation2d
from wpimath.kinematics import SwerveDriveKinematics, SwerveDriveOdometry, ChassisSpeeds, SwerveModuleState
from sharkbot.components.swervemodule import SwerveModule
from sharkbot.constants.driveconstants import DriveConstants

from sharkbot.util.ntloggerutility import NTLoggerUtility


class DriveSubsystem:
    def __init__(self, gyro: Gyro) -> None:
        """
        Initialize the swerve drive subsystem.

        Parameters:
        - gyro: Gyro - A gyro object to provide the robot's heading.
        """
        # Gyro for field-relative control
        self.gyro = gyro
        self.gyro.reset()

        # Swerve modules
        self.front_left = SwerveModule(DriveConstants.FRONT_LEFT_DRIVE_ID, DriveConstants.FRONT_LEFT_TURN_ID)
        self.front_right = SwerveModule(DriveConstants.FRONT_RIGHT_DRIVE_ID, DriveConstants.FRONT_RIGHT_TURN_ID)
        self.back_left = SwerveModule(DriveConstants.BACK_LEFT_DRIVE_ID, DriveConstants.BACK_LEFT_TURN_ID)
        self.back_right = SwerveModule(DriveConstants.BACK_RIGHT_DRIVE_ID, DriveConstants.BACK_RIGHT_TURN_ID)

        # Swerve kinematics (robot-relative positions of the modules)
        self.kinematics = SwerveDriveKinematics(
            DriveConstants.FRONT_LEFT_LOCATION,
            DriveConstants.FRONT_RIGHT_LOCATION,
            DriveConstants.BACK_LEFT_LOCATION,
            DriveConstants.BACK_RIGHT_LOCATION
        )

        # Odometry for tracking robot position on the field
        self.odometry = SwerveDriveOdometry(self.kinematics, self.getHeading())

        self.logger = NTLoggerUtility("DriveSubsystemLogs")

    def drive(self, x_speed: float, y_speed: float, rotation: float, field_relative: bool) -> None:
        """
        Drive the robot using swerve drive kinematics.

        Parameters:
        - x_speed: float - Forward/backward speed in meters per second.
        - y_speed: float - Left/right speed in meters per second.
        - rotation: float - Angular speed in radians per second.
        - field_relative: bool - Whether to use field-relative control.
        """
        self.logger.info("FnCall", f"drive({x_speed:.2f}, {y_speed:.2f}, {rotation: .2f}, {field_relative})")
        if field_relative:
            chassis_speeds = ChassisSpeeds.fromFieldRelativeSpeeds(
                x_speed, y_speed, rotation, self.getHeading()
            )
        else:
            chassis_speeds = ChassisSpeeds(x_speed, y_speed, rotation)

        # Convert chassis speeds to swerve module states
        states = self.kinematics.toSwerveModuleStates(chassis_speeds)

        # Normalize speeds to ensure they do not exceed maximum speed
        SwerveDriveKinematics.desaturateWheelSpeeds(states, DriveConstants.MAX_SPEED)

        # Apply states to each module
        self.front_left.setDesiredState(states[0])
        self.front_right.setDesiredState(states[1])
        self.back_left.setDesiredState(states[2])
        self.back_right.setDesiredState(states[3])

    def updateOdometry(self) -> None:
        """
        Update the robot's position on the field using odometry.
        """
        self.odometry.update(
            self.getHeading(),
            self.front_left.getState(),
            self.front_right.getState(),
            self.back_left.getState(),
            self.back_right.getState()
        )

    def getHeading(self) -> Rotation2d:
        """
        Get the robot's current heading as a Rotation2d object.
        """
        return Rotation2d.fromDegrees(-self.gyro.getAngle())  # Negate to correct for gyro direction

    def resetOdometry(self, pose) -> None:
        """
        Reset the robot's odometry to a specific pose.

        Parameters:
        - pose: Pose2d - The new robot pose on the field.
        """
        self.odometry.resetPosition(pose, self.getHeading())

    def stop(self) -> None:
        """
        Stop all swerve modules.
        """
        self.front_left.stop()
        self.front_right.stop()
        self.back_left.stop()
        self.back_right.stop()
