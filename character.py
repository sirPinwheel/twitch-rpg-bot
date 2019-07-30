from util import first_char_upper
from classes import Viking, Priest, Druid, Samurai, Amazon

class Character:
    """
    The Character class is what defines a specific user's hero (character)
    """

    def __init__(self, name, class_name, gender):
        self.level = 1
        # default max hp might be overwritten by class
        self.max_hp = 10
        self.hp = self.max_hp
        self.name = name
        if class_name == "viking":
            self.Class = Viking(self, gender)
        elif class_name == "priest" or class_name == "nun" or class_name == "monk":
            self.Class = Priest(self, gender)
        elif class_name == "druid":
            self.Class = Druid(self, gender)
        elif class_name == "samurai":
            self.Class = Samurai(self, gender)
        elif class_name == "amazon":
            self.Class = Amazon(self, gender)
        else:
            raise RuntimeError("There is no class %s!" % (class_name))

    def __str__(self, stats=False):
        return "%s %s" % (first_char_upper(str(self.Class)), self.name)
            
    @property
    def summary(self):
        """
        A short string respresenting all important stats
        """
        return "%s (level %i, %i/%i HP)" % (str(self), self.level, self.hp, self.max_hp)

    def do(self, what):
        return self.Class.do(what)
