from wpimath.geometry import Translation2d
from dataclasses import dataclass

@dataclass(frozen=True)
class DriveConstants:
    # Motor IDs
    FRONT_LEFT_DRIVE_ID: int = 1
    FRONT_LEFT_TURN_ID: int = 2
    FRONT_RIGHT_DRIVE_ID: int = 3
    FRONT_RIGHT_TURN_ID: int = 4
    BACK_LEFT_DRIVE_ID: int = 5
    BACK_LEFT_TURN_ID: int = 6
    BACK_RIGHT_DRIVE_ID: int = 7
    BACK_RIGHT_TURN_ID: int = 8

    # Module locations (inches)
    FRONT_LEFT_LOCATION: Translation2d = Translation2d(20, 20)
    FRONT_RIGHT_LOCATION: Translation2d = Translation2d(20, -20)
    BACK_LEFT_LOCATION: Translation2d = Translation2d(-20, 20)
    BACK_RIGHT_LOCATION: Translation2d = Translation2d(-20, -20)

    # Maximum speeds (inches per second)
    MAX_SPEED: float = 3.0
