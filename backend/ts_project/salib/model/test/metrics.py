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
        return self.tp_count() / (self.tp_count() + self.fp_count())

    def recall(self):
        return self.tp_count() / (self.tp_count() + self.fn_count())

    def f1(self):
        p = self.precision()
        r = self.recall()
        return 2 * p * r / (p + r)