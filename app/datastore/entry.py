class Entry:
    __slots__ = ("type", "value")

    def __init__(self, type_: str, value: object):
        self.type = type_
        self.value = value
