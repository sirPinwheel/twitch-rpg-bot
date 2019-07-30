from actions import *

class BaseClass:
    pass

class HeroClass(BaseClass):
    """
    The hero class any hero has
    """

    def __init__(self, char, name, gender, hp):
        self.char = char
        self.name = name
        self.gender = gender
        self.char.max_hp = hp
        self.char.hp = self.char.max_hp
        self.actions = { "run": Action(char, "run", "runs") }

    def __str__(self):
        if self.gender == "female":
            return "female " + self.name
        elif self.gender == "male":
            return "male " + self.name
        return self.name

    def do(self, what):
        if what == None or len(what) == 0:
            if len(self.actions) == 0:
                return "%s cannot do any actions right now!" % (self.char.name)
            else:
                return "%s can do the following actions: %s" % (self.char.name, " ".join(self.actions))
        elif what[0] in self.actions:
            return self.actions[what[0]].do(what[1:])
        else:
            raise RuntimeError("%s cannot %s!", (self.char.name, what[0]))

class Viking(HeroClass):
    """
    A mighty viking
    Strength Warrior
    """

    def __init__(self, char, gender):
        HeroClass.__init__(self, char, "viking", gender, 13)

class Priest(HeroClass):
    """
    A monk or nun, depending on gender
    Healer/Antimage
    """

    def __init__(self, char, gender):
        HeroClass.__init__(self, char, "priest", gender, 8)

    def __str__(self):
        if self.gender == "female":
            return "nun"
        elif self.gender == "male":
            return "monk"
        return "priest"

class Druid(HeroClass):
    """
    A druid, one with nature
    Healer/Supporter
    """

    def __init__(self, char, gender):
        HeroClass.__init__(self, char, "priest", gender, 9)

class Samurai(HeroClass):
    """
    A proud warrior from the far east
    Agility Warrior
    """

    def __init__(self, char, gender):
        HeroClass.__init__(self, char, "samurai", gender, 11)

class Amazon(HeroClass):
    """
    A warrior woman
    Archer
    """

    def __init__(self, char, gender):
        if gender != "female":
            raise RuntimeError("An Amazon can only be female!")
        HeroClass.__init__(self, char, "amazon", gender, 9)
