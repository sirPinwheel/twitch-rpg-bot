from util import *

class Class:
    """
    The (hero) class any character has
    """

    def __init__(self, name, gender):
        self.Name = name
        self.Gender = gender

    def __str__(self):
        return "Hero"

class Viking(Class):
    """
    A mighty viking
    """

    def __init__(self, gender):
        Class.__init__(self, "viking", gender)

    def __str__(self):
        if self.Gender == "female":
            return "female viking"
        elif self.Gender == "male":
            return "male viking"
        return "viking"

class Priest(Class):
    """
    A monk or nun, depending on gender
    """

    def __init__(self, gender):
        Class.__init__(self, "priest", gender)

    def __str__(self):
        if self.Gender == "female":
            return "nun"
        elif self.Gender == "male":
            return "monk"
        return "priest"

class Character:
    """
    The Character class is what defines a specific user's hero (character)
    """

    def __init__(self, name, class_name, gender):
        self.Level = 1
        self.Name = name
        if class_name == "viking":
            self.Class = Viking(gender)
        elif class_name == "priest" or "nun" or "monk":
            self.Class = Priest(gender)

    def __str__(self):
        return "%s %s (level %i)" % (first_char_upper(str(self.Class)), self.Name, self.Level)
