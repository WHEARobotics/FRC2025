import commands2
import phoenix6
from phoenix6.controls import DutyCycleOut
import wpilib

from commands import NeutralRequest

class DriveSubsystem(commands2.SubsystemBase):
    def __init__(self):
        #----------------------------------------------------------------------
        # Motor controllers

        # MAKO's left-side motor controllers, SparkMaxes
        # self.motor2 = rev.CANSparkMax(2, rev.CANSparkMax.MotorType.kBrushless)
        # self.motor4 = rev.CANSparkMax(4, rev.CANSparkMax.MotorType.kBrushless)

        # Test a Kraken
        self.kraken = phoenix6.hardware.TalonFX(0)

        # Note that "set_position" does not _command_ a position, it tells
        # the Kraken that its encoder should read the given position at
        # its present location.
        self.kraken.set_position(0)

        #----------------------------------------------------------------------
        # Set up Kraken's configuration by first getting a default 
        # configuration object.
        configuration = phoenix6.configs.TalonFXConfiguration()
        # Motor direction and neutral mode
        # Counterclockwise is positive when facing the motor shaft.
        configuration.motor_output.inverted = phoenix6.signals.InvertedValue.COUNTER_CLOCKWISE_POSITIVE
        configuration.motor_output.neutral_mode = phoenix6.signals.NeutralModeValue.BRAKE
        # Set control loop parameters for "slot 0", the profile we'll use for position control.
        configuration.slot0.k_p = 1.0 # An error of one rotation results in 1.0V to the motor.
        configuration.slot0.k_i = 0.0 # No integral control
        configuration.slot0.k_d = 0.0 # No differential component
        # Voltage control mode peak outputs.  I'm only using a reduced voltage
        # for this test because it is an unloaded and barely secured motor.
        # Ordinarily, we would not change the default value, which is 16V.
        configuration.voltage.peak_forward_voltage = 6 # Peak output voltage of 6V.
        configuration.voltage.peak_reverse_voltage = -6 # And likewise for reverse.

        # Set control loop parameters for slot 1, which we'll use with motion magic position control
        configuration.slot1.k_p = 1.0 # An error of one rotation results in 1.0V to the motor.
        configuration.slot1.k_i = 0.0 # No integral control
        configuration.slot1.k_d = 0.0 # No differential component
        # And set the motion magic parameters.
        configuration.motion_magic.motion_magic_cruise_velocity = 1 # 1 rotation/sec
        configuration.motion_magic.motion_magic_acceleration = 1 # Take approximately 1 sec (vel/accel) to get to full speed
        configuration.motion_magic.motion_magic_jerk = 10 # Take approx. 0.1 sec (accel/jerk) to reach max accel.

        #----------------------------------------------------------------------
        # Apply the configuration. Interestingly, CTRE's example has code that
        # attempts configuration 5 times.  This suggests that configuration
        # doesn't always take, which is kind of dismaying.
        status: phoenix6.StatusCode = phoenix6.StatusCode.STATUS_CODE_NOT_INITIALIZED
        for _ in range(0, 5):
            # Apply configuration and check its status.
            status = self.kraken.configurator.apply(configuration)
            if status.is_ok():
                break
        if not status.is_ok():
            print(f'Could not apply configs, error code: {status.name}')

        # Because original code output every *200*ms and loop runs every *20*ms...
        self.output_every_n_seconds = 0.2
        # ... we keep this counter that runs from 1 to 10 (see periodic_output() below)
        self.periodic_has_run_n_times = 0


        # Not sure if this needs to be sent again and again
        self.setDefaultCommand(NeutralRequest(self))

    def periodic(self):
        self.output_periodic()
        # Add more periodic functions here

    def output_periodic(self):
        # This fn is called every 20ms in all modes, but outputs every 200ms
        times_to_run = self.output_every_n_seconds // 0.02 #(20ms)

        # Have we looped enough times to update the dashboard?
        if self.periodic_has_run_n_times % times_to_run == 0:
            self.output_rotations_and_position()
            # Reset the counter
            self.periodic_has_run_n_times = 0
        else:
            self.periodic_has_run_n_times += 1
        
    def output_rotations_and_position(self):
        wpilib.SmartDashboard.putString('DB/String 0', 'rotations: {:5.1f}'.format(self.kraken.get_position().value))

    # Not sure!
    def set_to_neutral(self):
        request = phoenix6.controls.NeutralOut()
        self.kraken.set_neutral_mode(request)
        
    # Not sure!
    def set_voltage_position(self, position):
        request = phoenix6.controls.PositionVoltage(position).with_slot(0)
        self.kraken.set_control(request)
        
    #  Not sure!
    def set_motion_magic_position(self, position):
        request = phoenix6.controls.MotionMagicPosition(position).with_slot(1)
        self.kraken.set_control(request)
