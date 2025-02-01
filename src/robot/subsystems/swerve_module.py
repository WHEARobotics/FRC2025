import math

import wpimath
from phoenix6.controls import PositionVoltage, NeutralOut
from phoenix6.hardware import CANcoder
from phoenix6.hardware.talon_fx import TalonFX
from phoenix6.configs import TalonFXConfiguration, CANcoderConfiguration
from phoenix6.signals import InvertedValue, NeutralModeValue
from wpimath.geometry import Rotation2d
from wpimath.kinematics import SwerveModulePosition, SwerveModuleState
from wpimath.units import degrees, radians, meters, inches
from wpimath.units import degreesToRadians, radiansToDegrees, metersToInches, inchesToMeters, degreesToRotations, rotationsToDegrees

import wpilib

from constants.driveconstants import DriveConstants

class SwerveModule:
    def __init__(self, drive_motor_bus_id:int, turn_motor_bus_id:int, cancoder_bus_id:int, offset:float):
        self.drive_motor = TalonFX(drive_motor_bus_id)
        self.turn_motor = TalonFX(turn_motor_bus_id)
        self.can_coder = CANcoder(cancoder_bus_id)  # ID number

        self.turn_motor.configurator.apply(self._configure_turn_motor())
        self.drive_motor.configurator.apply(self._configure_drive_motor())
        # self.can_coder.configurator.apply(self._configure_cancoder(offset=offset)) #give the offset values to the function to config

        # Either brake or coast, depending on motor configuration; we chose brake above.
        self.brake_request = NeutralOut()

        # Position request starts at position 0, but can be modified later.
        self.position_request = PositionVoltage(0).with_slot(0)

    # Sets the drive to the given speed, expressed as a percentage of full speed (range -1 to 1).
    def set_drive_effort(self, speed_pct):
        self.drive_motor.set(speed_pct)

    # Returns percentage of full driving speed (range -1 to 1)
    def get_drive_effort(self):
        return self.drive_motor.get()

    # Sets the turn to the given speed, expressed as a percentage of full speed (range -1 to 1).
    def set_turn_effort(self, speed_pct):
        self.turn_motor.set(speed_pct)

    # Returns percentage of full turning speed (range -1 to 1)
    def get_turn_effort(self):
        return self.turn_motor.get()

    def velocity_from_effort(self, effort_pct):
        effort = max(min(effort_pct, 1.0), -1.0)

        # Conversion using feed forward
        kS = 0.0  # Static friction compensation
        kV = 1.0  # Velocity feed forward

        # Convert effort to desired velocity
        desired_velocity = effort * self._max_velocity_inches_per_second()

        # Apply feed forward
        if abs(desired_velocity) > 0:
            voltage_forward = math.copysign(kS, desired_velocity) + kV * desired_velocity
            # Convert back to velocity
            return (voltage_forward / kV) if kV != 0 else desired_velocity
        return 0.0

    # TODO: Is this correct?
    def set_turn_angle(self, angle_degrees : float):
        motor_rotation = degreesToRotations(angle_degrees) #translate from degree to rotation for motor

        # Position request starts at position 0, but can be modified later.
        self.turn_motor.set_control(self.position_request.with_position(motor_rotation)) # ???

    # Returns the current angle of the module in degrees.
    def get_turn_angle_degrees(self) -> float:
        rotations = self.turn_motor.get_position().value
        return rotationsToDegrees(rotations)

    def get_state(self) -> SwerveModuleState:
        """
        Get the current state of the module
        Returns:
            Current state (speed and angle)
        """
        speed : meters = self.get_drive_effort()  # Replace with actual drive velocity in m/s
        angle = wpimath.geometry.Rotation2d()  # Replace with actual module angle
        return wpimath.kinematics.SwerveModuleState(speed, angle)

    # Returns the current position of the module. This is needed by the drive subsystem's kinematics.
    def get_position(self) -> SwerveModulePosition:
        can_coder_rotations = self._get_can_coder_pos_rotations()
        distance : meters = inchesToMeters(can_coder_rotations * self._inches_per_rotation())
        angle : Rotation2d = Rotation2d.fromDegrees(self.get_turn_angle_degrees())
        # Argument units per https://robotpy.readthedocs.io/projects/wpimath/en/latest/wpimath.kinematics/SwerveModulePosition.html
        return SwerveModulePosition(distance, angle)

    def _inches_per_rotation(self) -> inches:
        return DriveConstants.WHEEL_RADIUS * 2 * 3.14159

    def _configure_turn_motor(self):
        configuration = TalonFXConfiguration()

        configuration.motor_output.inverted = InvertedValue.COUNTER_CLOCKWISE_POSITIVE
        configuration.motor_output.neutral_mode = NeutralModeValue.COAST

        # Set control loop parameters for "slot 0", the profile we'll use for position control.
        configuration.slot0.k_p = 1.0  # An error of one rotation results in 1.0V to the motor.
        configuration.slot0.k_i = 0.0  # No integral control
        configuration.slot0.k_d = 0.0  # No differential component
        # Voltage control mode peak outputs.  I'm only using a reduced voltage
        # for this test because it is an unloaded and barely secured motor.
        # Ordinarily, we would not change the default value, which is 16V.

        return configuration

    def _configure_drive_motor(self):
        configuration = TalonFXConfiguration()

        configuration.motor_output.inverted = InvertedValue.CLOCKWISE_POSITIVE
        configuration.motor_output.neutral_mode = NeutralModeValue.BRAKE

        # Set control loop parameters for "slot 0", the profile we'll use for position control.
        configuration.slot0.k_p = 1.0  # An error of one rotation results in 1.0V to the motor.
        configuration.slot0.k_i = 0.0  # No integral control
        configuration.slot0.k_d = 0.0  # No differential component
        # Voltage control mode peak outputs.  I'm only using a reduced voltage
        # for this test because it is an unloaded and barely secured motor.
        # Ordinarily, we would not change the default value, which is 16V.
        return configuration

    def _configure_cancoder(self, offset:float):  #Mostly for configuring offsets
        configuration = CANcoderConfiguration()

        # configuration.magnet_sensor(offset)

        return configuration

    # Returns the CANCoder's current position as a percentage of full rotation (range [-1,1]).
    def _get_can_coder_pos_rotations(self) -> float: # the _ in front of a function is indicating that this is only should be used in this class NOT ANYWHERE ELSE
        return self.can_coder.get_absolute_position().value   #the .value property doesn't seem to have () at the end

    # Per
    def _max_velocity_inches_per_second(self) -> inches:
        free_speed_inches_per_second = metersToInches(DriveConstants.FREE_SPEED)

