class Player:
    def __init__(self, position: int, health: int, name: str):
        self.position = position
        self.health = health
        self.name = name

    def move(self, position: int):
        self.position = position