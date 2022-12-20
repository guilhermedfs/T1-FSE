class InOutModel:
    def __init__(self, type, tag, gpio, value = 0):
        self.type = type
        self.tag = tag
        self.gpio = gpio
        self.value = value
        self.key = None

    def getType(self):
        return self.type

    def getTag(self):
        return self.tag

    def getGpio(self):
        return self.gpio
    
    def getValue(self):
        return self.value

    def getKey(self):
        return self.key

    def setValue(self, value):
        self.value = value

    def setKey(self, key):
        self.key = key