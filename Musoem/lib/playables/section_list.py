class SectionList:

    def __init__(self, list, kw):
        self.list = list
        self.keyword = kw
        self.index = 0

    @property
    def next(self):
        res = self.list[self.index]
        if self.index < len(self.list) - 1:
            self.index += 1
        else:
            self.index = 0
        return res

    def __iter__(self):
        return iter(self.list)
