from dataclasses import dataclass

from constants.new_types import inches


@dataclass(frozen=True)
class ElevatorConstants:
    ELEVATOR_MOTOR = 14  # Motor ID

    STOP_CURRENT = 70 #TODO: Update

    # TODO: Update height offset, and positions

    # Mechanical constants
    GEAR_RATIO: float = 1.0
    SCREW_INCHES_PER_ROT = 0.25

    # All heights are the upper elevator bolt spacer
    HEIGHT_OFFSET: float = (
        12.75  # Height of the lowest part and hitting the hardstop
    )

    # Heights in inches (lowest is 10.5, highest is ~55.5)  #Change names of the different heights when writing the official code
    HOME: inches = 12.25  # Elevator at its lowest position. 
    LEVEL_ONE: inches = 12.25
    LEVEL_TWO: inches = 12.25
    LEVEL_THREE: inches = 28.75     
    FEEDER: inches = 16.75
    TOP: inches = 29.75  #Elevator at its Highest position

   