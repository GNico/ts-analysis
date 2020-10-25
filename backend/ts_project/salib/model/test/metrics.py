from model.utils import timestamp_to_epoch


class Metrics:

    def __init__(self, tp, fp, tn, fn):
        self.tp = tp
        self.fp = fp
        self.tn = tn
        self.fn = fn

    def tp_count(self):
        return len(self.tp)

    def fp_count(self):
        return len(self.fp)

    def tn_count(self):
        return len(self.tn)

    def fn_count(self):
        return len(self.fn)

    def precision(self):
        try:
            return self.tp_count() / (self.tp_count() + self.fp_count())
        except ZeroDivisionError:
            return 0

    def recall(self):
        try:
            return self.tp_count() / (self.tp_count() + self.fn_count())
        except ZeroDivisionError:
            return 0

    def f1(self):
        p = self.precision()
        r = self.recall()
        return 2 * p * r / (p + r)

    def output_format(self):
        output = {}
        output['values'] = []
        tp_ranges, fp_ranges, fn_ranges = self.build_error_ranges()
        output['values'].extend(Metrics.format_errors(tp_ranges, 'tp'))
        output['values'].extend(Metrics.format_errors(fp_ranges, 'fp'))
        output['values'].extend(Metrics.format_errors(fn_ranges, 'fn'))
        output['fp'] = self.fp_count()
        output['tp'] = self.tp_count()
        output['fn'] = self.fn_count()
        output['precision'] = self.precision()
        output['recall'] = self.recall()
        return output

    # TODO
    def build_error_ranges(self):
        tp_ranges = []
        fp_ranges = []
        fn_ranges = []
        return (tp_ranges, fp_ranges, fn_ranges)

    @staticmethod
    def format_errors(errors, type):
        return [Metrics.format_error(error, type) for error in errors]

    @staticmethod
    def format_error(error, type):
        print(error)
        return {
            'from': timestamp_to_epoch(error[0]),
            'to': timestamp_to_epoch(error[1]),
            'type': type
        }
