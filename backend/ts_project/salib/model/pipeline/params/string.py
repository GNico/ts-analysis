from .param import Param

class String(Param):

    def __init__(self, id, display, desc, value=None):
        super().__init__(id, 'String', display, desc, value)