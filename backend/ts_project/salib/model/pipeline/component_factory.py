from .components.ema import EMA

# ToDo: rename to node factory, split into transformers, detectors, aggregators
class ComponentFactory:

    COMPONENT_NAMES = {
        'EMA': EMA
    }

    @staticmethod
    def base_component(name):
        if name in ComponentFactory.COMPONENT_NAMES.keys():
            return ComponentFactory.COMPONENT_NAMES[name]()
        else:
            raise Exception('Invalid component ' + name)

    @staticmethod
    def components_description():
        output = {}
        for name in ComponentFactory.COMPONENT_NAMES:
            output[name] = ComponentFactory.base_component(name).params_definition()
        return output

    def __init__(self, component_name):
        self.component = ComponentFactory.base_component(component_name)

    def set_param_value(self, id, value):
        self.component.set_param_value(id, value)
        return self

    def build(self):
        self.component.validate()
        return self.component