class NodeRef:

    def __init__(self, ref):
        self.ref = ref

    def is_node_ref(self):
        return True

    def is_input_ref(self):
        return False

    def __str__(self):
        return "Node[%s]" % self.ref

class InputRef:

    def __init__(self, ref):
        self.ref = ref

    def is_node_ref(self):
        return False

    def is_input_ref(self):
        return True

    def __str__(self):
        return "Input[%s]" % self.ref

class NodeSourceParser:

    @staticmethod
    def parse(obj):
        type = obj['type']
        ref = obj['ref']
        if type == 'input':
            return InputRef(ref)
        elif type == 'node':
            return NodeRef(ref)
        else:
            raise ValueError("Invalid node source type %s, with ref %s" % (type,ref))