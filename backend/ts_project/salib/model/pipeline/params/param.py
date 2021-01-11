class Param:

    def __init__(self, id, klass, value):
        self.id = id
        self.type = klass
        self.value = value

    def definition(self):
        output = {
            'id': self.id,
            'type': self.klass,
            'value': self.value,
        }
        return output

    def validate(self):
        pass