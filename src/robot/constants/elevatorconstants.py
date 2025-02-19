from dataclasses import dataclass

@dataclass(frozen=True)
class ElevatorConstants: 
    ELEVATOR_MOTOR = 14 # Motor ID

    #TODO: Update height offset, and positions

    # Mechanical constants
    GEAR_RATIO: float = 1.0 
    HEIGHT_OFFSET: float = 10.5 # Height of the second stage's lower crosspiece (top surface), in inches.
    SCREW_INCHES_PER_ROT = 0.25 

    # Heights in inches (lowest is 10.5, highest is ~55.5)  #Change names of the different heights when writing the offical code
    HOME: float = 10.5 # Elevator at its lowest position.
    MID: float  = 34.5