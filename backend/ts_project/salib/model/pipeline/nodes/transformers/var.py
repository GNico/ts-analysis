import pandas as pd
import numpy as np

import statsmodels.tsa.vector_ar.var_model as var_model
import statsmodels.tsa.stattools as stattools

from ..node_transformer import NodeTransformer
from ...params.boolean import Boolean
from ...params.condition.param_equals_value import ParamEqualsValue
from ...params.int import BoundedInt
from ...params.select import Select, SelectOption
from ...params.string import String
from ....utils import timedelta_to_period

class VAR(NodeTransformer):

    def __init__(self, id):
        super().__init__(id)
        self.set_input_names(['fst', 'snd'])
        self.add_params()

    def add_params(self):
        self.add_required_param(String('p', 'p', 'AR order', '1'))
        output_options = [
            SelectOption("resid", "Residual"),
            SelectOption("predicted", "Predicted"),
        ]
        self.add_required_param(Select('output', 'Output', 'Model output', output_options, output_options[0].code))


    def get_params(self):
        p = self.get_param('p').value
        output = self.get_param('output').value
        return (p, output)

    def transform(self, seriess, debug):
        lhs, rhs = seriess[0], seriess[1]
        NodeTransformer.validate_input_steps_spans(lhs, rhs)
        if(lhs.span() != rhs.span()):
            raise ValueError("Inputs must have same span")

        endog = np.transpose([s.pdseries.tolist() for s in seriess])

        p, output = self.get_params()
        calc_p = timedelta_to_period(p, seriess[0].step())

        model = var_model.VAR(endog)
        model_fit = model.fit(calc_p)

        result = None
        if output == 'predicted':
            result = model_fit.fittedvalues
        elif output == 'resid':
            result = model_fit.resid
        else:
            raise ValueError('Invalid output: ' + output)

        # Drop offset_start elements
        offset_start = len(seriess[0].pdseries.index) - len(result)
        # Debug info
        if debug:
            debug_info = {
                "summary": str(model_fit.summary()),
                "offset_start": offset_start,
            }
        else:
            debug_info = {}
        result = pd.Series([np.sum(np.abs(r)) for r in result], index=seriess[0].pdseries.index[offset_start:])
        return (result, debug_info)

    def __str__(self):
        return "VAR" + str(self.get_params()) + "[" + self.id + "]"

    def display(self):
        return 'VAR'

    def desc(self):
        return 'Vector AutoRegression with lags'
