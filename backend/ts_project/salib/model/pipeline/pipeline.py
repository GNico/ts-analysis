from .nodes.node_result import NodeResult

class Pipeline:

    def __init__(self, terminal_node):
        self.terminal_node = terminal_node
        self.series = None

    def execute(self, series):
        self.series = series
        result = self.execute_node(self.terminal_node)
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