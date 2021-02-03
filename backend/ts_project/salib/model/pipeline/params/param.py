class Param:

    def __init__(self, id, klass, display, desc, value=None):
        self.id = id
        self.type = klass
        self.desc = desc
        self.display = display
        self.value = value

    def is_set(self):
        return self.value is not None

    def definition(self):
        output = {
            'id': self.id,
            'type': self.type,
            'display': self.display,
            'desc': self.desc,
            'value': self.value
        }
        return output

    def validate(self):
        pass