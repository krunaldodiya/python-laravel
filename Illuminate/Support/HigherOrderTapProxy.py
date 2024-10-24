class HigherOrderTapProxy:
    def __init__(self, target):
        self.target = target

    def __getattr__(cls, attribute, *args, **kwargs):
        pass
