from dataclasses import dataclass
from wpilib import XboxController

@dataclass(frozen=True)
class OperatorInterfaceConstants:
    BUTTON_A: int = XboxController.Button.kA
    BUTTON_B: int = XboxController.Button.kB
    BUTTON_X: int = XboxController.Button.kX
    BUTTON_Y: int = XboxController.Button.kY

    BUMPER_RIGHT: int = XboxController.Button.kRightBumper
    BUMPER_LEFT: int = XboxController.Button.kLeftBumper

    DRIVER_CONTROLLER_PORT: int = 0 # USB port number for the Xbox controller on Rod's computer.
    OPERATOR_CONTROLLER_PORT: int = 1

    DRIVE_SLOWER: float = 4 # Factor to divide the drive commands to slow things down for safety.