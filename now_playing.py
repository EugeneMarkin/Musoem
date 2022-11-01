class NowPlaying:

    playing = {}
    callback = None

    @classmethod
    def reset(self):
        for item in list(self.playing.values()).copy():
            item.stop()
        self.playing = {}

    @classmethod
    def play(self, playable):
        playable(playable._times)
        self.playing[playable.keyword] = playable
        self.callback()

    @classmethod
    def apply_operation(self, operation, section):
        operation.apply_to(section)
        self.callback()

    @classmethod
    def remove(self, keyword):
        if keyword in self.playing:
            if self.playing[keyword]._next is not None:
                playable = self.playing[keyword]._next
                self.playing[playable.keyword] = playable
            self.playing.pop(keyword)
            self.callback()

    @classmethod
    def stop(self, keyword):
        if keyword in self.playing:
            self.playing[keyword].stop()
            return

        for p in self.playing.values():
            p.stop(keyword)



    @classmethod
    def display(self):
        res = ""
        for playable in list(self.playing.values()):
            res += playable.display() + "\n"
        return res

    @classmethod
    def all(self):
        return list(self.playing.values())

    @classmethod
    def update(self):
        self.callback()

    @classmethod
    def last(self):
        durs = list(map(lambda x: x.time_till_end, self.playing.values()))
        if None in durs:
            return list(self.playing.values())[durs.index(None)]
        else:
            return list(self.playing.values())[durs.index(max(durs))]

    @classmethod
    def bind_callback(self, callback):
        self.callback = callback
