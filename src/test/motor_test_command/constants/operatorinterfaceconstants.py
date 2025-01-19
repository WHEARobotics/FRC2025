import wpilib

from dataclasses import dataclass

@dataclass(frozen=True)
class OperatorInterfaceConstants:
    BUTTON_A: int = XboxController.Button.kA
    BUTTON_B: int = XboxController.Button.kB
    BUTTON_X: int = XboxController.Button.kX
    BUTTON_Y: int = XboxController.Button.kY

    LEFT_BUMPER: int = XboxController.Button.kBumperLeft
    RIGHT_BUMPER: int = XboxController.Button.kBumperRight
