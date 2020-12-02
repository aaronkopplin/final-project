from Dial import  Dial

class Player:
    def __init__(self, position: int, health: int, name: str, dial: Dial):
        self.position = position
        self.health = health
        self.name = name
        self.dial = dial

    def move(self, position: int):
        self.position = position