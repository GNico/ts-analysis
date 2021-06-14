class SalibModelAdapter:

    @staticmethod
    def toSalib(model):
        input_nodes = set()
        for node in model:
            if (node['type'] == 'input'): 
                input_nodes.add(node['id'])

        nodes = []
        for node in model:
            if node['type'] == 'input':
                continue
            new_node = node.copy()
            formatted_params = []
            paramsdata = node.get('paramsData', {})
            for param in paramsdata:
                formatted_params.append({'id': param, 'value': paramsdata[param] })
            formatted_sources = []
            for source in node['sources']:
                formatted_sources.append({'type': 'input' if (source in input_nodes) else 'node',
                    'ref': source})

            new_node.pop('paramsData', None)
            new_node.pop('sources', None)
            new_node['params'] = formatted_params
            new_node['sources'] = formatted_sources
            nodes.append(new_node)

        return {'nodes': nodes}

