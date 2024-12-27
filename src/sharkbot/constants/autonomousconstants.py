from dataclasses import dataclass

@dataclass(frozen=True)
class AutoPlan:
    TEST = 4
    ONE_NOTE = 3
    ONE_NOTE_PORT = 2
    ONE_NOTE_STARBOARD = 1
    TWO_NOTE_CENTER = 0
