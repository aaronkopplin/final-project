class Dial:
    def __init__(self, pointValue: int, lightningBolt: int):
        self.speed = []  # how fast the character is
        self.attack = []
        self.defence = []
        self.damage = []  # how much damage the character deals in a single attack
        self.clickLevel = 1
        self.pointValue = pointValue
        self.lightningBolt = lightningBolt

    def click(self):
        self.speed.pop(0)
        self.attack.pop(0)
        self.defence.pop(0)
        self.damage.pop(0)
        self.clickLevel += 1

    def printDial(self):
        print("click level: " + str(self.clickLevel))
        print("speed:\t\t" + " ".join(map(str, self.speed)))
        print("attack:\t\t" + " ".join(map(str, self.attack)))
        print("defence:\t" + " ".join(map(str, self.defence)))
        print("damage:\t" + " ".join(map(str, self.damage)))
        print("point value: " + str(self.pointValue))
        print("lightning bolt: " + str(self.lightningBolt))