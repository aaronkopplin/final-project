from Dial import  Dial

class Player:
    def __init__(self, position: int, health: int, name: str, dial: Dial, team: int):
        self.position = position
        self.health = health
        self.name = name
        self.dial = dial
        self.team = team
        self.id = self.name[0] + str(self.team)

    def move(self, position: int):
        self.position = position

    def printDial(self):
        self.dial.printDial()