from .node_factory import NodeFactory
from .nodes.node_result import NodeResult
from .nodes.aggregators.root import Root
from .nodes.node_source import NodeRef

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
                if node_source_ref.is_node_ref():
                    source = self.resolve_node_reference(node_source_ref.ref)
                    node_input_results.append(self.execute_node(source, inputs))
                elif node_source_ref.is_input_ref():
                    series = inputs[node_source_ref.ref]
                    node_input_results.append(NodeResult(None, [], output_series=series))
                else:
                    raise ValueError("Invalid node %s source %s" % (node.id, node_source_ref))
                
        node.validate_inputs(node_input_results)
        return node.execute(node_input_results)

    def resolve_node_reference(self, reference):
        return self.node_reference_table[reference]

    @staticmethod
    def from_json(obj):
        nodes = obj['nodes']
        all_nodes = [NodeFactory.from_json(node) for node in nodes]
        return Pipeline(all_nodes)

    @staticmethod
    def build_root_node(nodes):
        all_node_references = set()
        for node in nodes:
            all_node_references.update([s.ref for s in node.node_sources()])
        
        root = Root()
        # Add nodes that are not referenced by anyone as source to root node
        for node in nodes:
            if node.id not in all_node_references:
                root.add_source(NodeRef(node.id))

        return root

    @staticmethod
    def build_node_reference_table(nodes):
        node_reference_table = {}
        for node in nodes:
            node_reference_table[node.id] = node
        return node_reference_table