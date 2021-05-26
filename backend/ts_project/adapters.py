class SalibModelAdapter:

    @staticmethod
    def toSalib(model):
        nodes = []
        for node in model:
            params = []
            for param in node['paramsData']:
                params.append({'id': param, 'value': node['paramsData'][param] })
            new_node = node.copy()
            del new_node['paramsData']    
            new_node['params'] = params
            nodes.append(new_node)
        return {'nodes': nodes}

