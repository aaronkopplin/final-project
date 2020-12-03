from Dial import Dial
import copy

class Player:
    def __init__(self, position=-1, health=-1, name="steve", dial=None, team=-1):
        self.position = position
        self.health = health
        self.name = name
        self.dial = dial
        self.team = team
        self.id = self.name[0] + str(self.team)
        self.isKOd = False

    def currentSpeed(self):
        return copy.deepcopy(self.dial.currentSpeed())

    def move(self, position: int):
        self.position = position

    def printDial(self):
        self.dial.printDial(self.id)

    def takeDamage(self, attack_total: int, damage: int):
        if attack_total < self.dial.currentDefence():
            return
        for click in range(damage):
            self.dial.click()
            if self.dial.isKod():
                self.isKOd = True
                break
