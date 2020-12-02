class Dial:
    def __init__(self, pointValue: int):
        self.speed = []
        self.attack = []
        self.defence = []
        self.explosion = []
        self.clickLevel = 1
        self.pointValue = pointValue

    def click(self):
        self.speed.pop(0)
        self.attack.pop(0)
        self.defence.pop(0)
        self.explosion.pop(0)
        self.clickLevel += 1

    def printDial(self):
        print("click level: " + str(self.clickLevel))
        print("speed:\t\t" + " ".join(map(str, self.speed)))
        print("attack:\t\t" + " ".join(map(str, self.attack)))
        print("defence:\t" + " ".join(map(str, self.defence)))
        print("explosion:\t" + " ".join(map(str, self.explosion)))
        print("point value: " + str(self.pointValue))