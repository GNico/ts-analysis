from .node_factory import NodeFactory
from .nodes.node_result import NodeResult
from .nodes.aggregators.root import Root

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
            return node.execute([NodeResult(None, [], series=self.series)])
        # Else we calculate recursively all inputs
        else:
            node_inputs = []
            for node_source in node.sources:
                node_inputs.append(self.execute_node(node_source))
        node.validate_inputs(node_inputs)
        return node.execute(node_inputs)

    @staticmethod
    def from_json(obj):
        reference_table = {}
        nodes = obj['nodes']
        all_source_references = set()
        for node in nodes:
            actual_node = NodeFactory.from_json(node)
            reference_table[actual_node.id] = actual_node
            all_source_references.update(actual_node.sources)
        root_node = Pipeline.build_root_node(reference_table.values(), all_source_references)
        Pipeline.replace_node_references(reference_table, root_node)
        return Pipeline(root_node)

    @staticmethod
    def replace_node_references(refs, node):
        node.sources = [refs[source] for source in node.sources]
        for source in node.sources:
            Pipeline.replace_node_references(refs, source)

    @staticmethod
    def build_root_node(all_nodes, all_source_references):
        root = Root()
        for node in all_nodes:
            if node.id not in all_source_references:
                root.add_source(node.id)
        return root