from wpimath.geometry import Translation2d
from dataclasses import dataclass, field

# Regrettably, this cannot be a frozen dataclass because it contains mutable fields
class DriveConstants:
    # Motor IDs
    FRONT_LEFT_DRIVE_ID = 1
    FRONT_LEFT_TURN_ID = 2
    FRONT_RIGHT_DRIVE_ID = 3
    FRONT_RIGHT_TURN_ID = 4
    BACK_LEFT_DRIVE_ID = 5
    BACK_LEFT_TURN_ID = 6
    BACK_RIGHT_DRIVE_ID = 7
    BACK_RIGHT_TURN_ID = 8

    # Module locations (inches)
    FRONT_LEFT_LOCATION = Translation2d(20, 20)
    FRONT_RIGHT_LOCATION = Translation2d(20, -20)
    BACK_LEFT_LOCATION = Translation2d(-20, 20)
    BACK_RIGHT_LOCATION = Translation2d(-20, -20)

    # Maximum speeds (inches per second)
    MAX_SPEED = 3.0