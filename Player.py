from Dial import Dial
import copy

# class to keep track of the player states
class Player:
    def __init__(self, position=-1, health=-1, name="steve", dial=None, team=-1):
        self.position = position
        self.health = health
        self.name = name
        self.dial = dial
        self.team = team
        self.id = self.name[0] + str(self.team)
        self.isKOd = False

    # returns a copy of the players speed, or maximum movement distance
    def currentSpeed(self):
        return copy.deepcopy(self.dial.currentSpeed())

    # updates a players position to the position passed in. should be 0 - 255
    def move(self, position: int):
        self.position = position

    # prints the players dial to the console
    def printDial(self):
        self.dial.printDial(self.id)

    # determines if the player needs to click their dial, and clicks it accordingly.
    # sets the player to KO's if they KO from the damage
    # damage is the attacking players Damage stat from their dial
    def takeDamage(self, attack_total: int, damage: int):
        if attack_total < self.dial.currentDefence():
            return
        for click in range(damage):
            self.dial.click()
            if self.dial.isKod():
                self.isKOd = True
                break
