from .node_factory import NodeFactory
from .nodes.node_result import NodeResult

class Pipeline:

    def __init__(self, root_node):
        self.root_node = root_node
        self.series = None

    def execute(self, series):
        self.series = series
        result = self.execute_node(self.root_node)
        return result

    def execute_node(self, node):
        # If we have no sources we inject original series
        if len(node.sources) == 0:
            return node.execute([NodeResult(None, series=self.series)])
        # Else we calculate recursively all inputs
        else:
            node_inputs = []
            for node_source in node.sources:
                node_inputs.append(self.execute_node(node_source))    
        return node.execute(node_inputs)

    @staticmethod
    def from_json(obj):
        reference_table = {}
        root_node = None
        nodes = obj['nodes']
        for node in nodes:
            actual_node = NodeFactory.from_json(node)
            reference_table[actual_node.id] = actual_node
            # First node is root node!
            if root_node == None:
                root_node = actual_node
        if root_node is None:
            raise Exception("Must have root node")

        Pipeline.replace_node_references(reference_table, root_node)
        return Pipeline(root_node)

    @staticmethod
    def replace_node_references(refs, node):
        node.sources = [refs[source] for source in node.sources]
        for source in node.sources:
            Pipeline.replace_node_references(refs, source)