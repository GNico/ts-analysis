class Param:

    def __init__(self, id, klass, display, desc, value=None):
        self.id = id
        self.type = klass
        self.desc = desc
        self.display = display
        self.conditions = []
        self.value = value

    def is_set(self):
        return self.value is not None

    def add_condition(self, condition):
        self.conditions.append(condition)

    def definition(self):
        output = {
            'id': self.id,
            'type': self.type,
            'display': self.display,
            'desc': self.desc,
            'conditions': list([c.to_json() for c in self.conditions]),
            'value': self.value
        }
        return output

    def validate(self):
        pass