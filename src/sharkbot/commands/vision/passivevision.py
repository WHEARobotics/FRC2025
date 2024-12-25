class PassiveVision(CommandBase):
    def __init__(self, vision: Vision):
        super().__init__()
        self.vision = vision
        self.addRequirements(vision)

    def initialize(self) -> None:
        pass

    def execute(self) -> None:
        pass

    def isFinished(self) -> bool:
        return False

    def end(self) -> None:
        pass

    def interrupted(self) -> None:
        pass