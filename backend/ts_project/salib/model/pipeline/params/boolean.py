from .param import Param

class Boolean(Param):

    def __init__(self, id, display, desc, value=None):
        super().__init__(id, 'Boolean', display, desc, value)