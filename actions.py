class Action:
    """
    The base action class. Every character has one or more possible actions
    """

    def __init__(self, char, name, names):
        self.char = char
        self.name = name
        self.names = names
    
    def __str__(self):
        return "%s" % (self.name)

    def do(self, what):
        return "%s %s" % (self.char.name, self.names)
