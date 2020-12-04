# class that keeps track of the stats for each character
class Dial:
    def __init__(self, pointValue: int, lightningBolt: int):
        self.speed = []  # how fast the character is
        self.attack = []
        self.defence = []
        self.damage = []  # how much damage the character deals in a single attack
        self.clickLevel = 1
        self.pointValue = pointValue
        self.lightningBolt = lightningBolt

    # return the movement distance of the character
    def currentSpeed(self):
        return self.speed[0]

    # returns the current attack strength of the character
    def currentAttack(self):
        return self.attack[0]

    # returns the current defence strength of the character
    def currentDefence(self):
        return self.defence[0]

    # returns the current damage of the character
    def currentDamage(self):
        return self.damage[0]

    # acts like a click in the game, advances the characters dial one click forward
    def click(self):
        self.speed.pop(0)
        self.attack.pop(0)
        self.defence.pop(0)
        self.damage.pop(0)
        self.clickLevel += 1

    # return if the character is alive or dead. Characters become KO's when the dial advances far enough
    def isKod(self):
        return self.speed[0] == 0

    # print the dial to the console
    def printDial(self, id: str):
        print("-------------------------------------------")
        print("player id: " + id)
        print("click level: " + str(self.clickLevel))
        print("speed:\t\t" + " ".join(map(str, self.speed)))
        print("attack:\t\t" + " ".join(map(str, self.attack)))
        print("defence:\t" + " ".join(map(str, self.defence)))
        print("damage:\t\t" + " ".join(map(str, self.damage)))
        print("point value: " + str(self.pointValue))
        print("lightning bolt: " + str(self.lightningBolt))
        print("-------------------------------------------")
