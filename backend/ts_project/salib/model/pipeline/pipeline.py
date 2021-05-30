from .node_factory import NodeFactory
from .nodes.node_result import NodeResult
from .nodes.aggregators.root import Root
from .nodes.node_source import NodeReference, InputReference

class Pipeline:

    def __init__(self, nodes):
        self.nodes = nodes
        self.node_reference_table = Pipeline.build_node_reference_table(nodes)
        self.root_node = Pipeline.build_root_node(nodes)

    def execute(self, inputs):
        result = self.execute_node(self.root_node, inputs)
        return result

    def execute_node(self, node, inputs):
        if len(node.sources) == 0:
            raise ValueError("Invalid node %s with no sources" % node.id)
        else:
            node_input_results = []
            for node_source_ref in node.sources:
                if isinstance(node_source_ref, NodeReference):
                    source = self.node_reference_table[node_source_ref.reference]
                    node_input_results.append(self.execute_node(source, inputs))
                elif isinstance(node_source_ref, InputReference):
                    series = inputs[node_source_ref.reference]
                    node_input_results.append(NodeResult(None, [], series=series))
                else:
                    raise ValueError("Invalid node %s source %s" % (node.id, node_source_ref))
                
        node.validate_inputs(node_input_results)
        return node.execute(node_input_results, inputs)

    @staticmethod
    def from_json(obj):
        nodes = obj['nodes']
        all_nodes = [NodeFactory.from_json(node) for node in nodes]
        return Pipeline(all_nodes)

    @staticmethod
    def build_root_node(nodes):
        all_source_references = set()
        for node in nodes:
            all_source_references.update([source.reference for source in node.sources])
        
        root = Root()
        for node in nodes:
            if node.id not in all_source_references:
                root.add_source(NodeReference(node.id))

        return root

    @staticmethod
    def build_node_reference_table(nodes):
        node_reference_table = {}
        for node in nodes:
            node_reference_table[node.id] = node
        return node_reference_table