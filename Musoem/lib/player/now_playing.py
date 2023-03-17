class NowPlaying:

    playing = []
    callback = None

    @classmethod
    def reset(self):
        for item in self.playing.copy():
            item.stop()
        self.playing = []

    @classmethod
    def add(self, playable):
        self.playing.append(playable)
        self.update()

    @classmethod
    # called when a playable is finished
    def remove(self, playable):
        if playable in self.playing:
            self.playing.remove(playable)
            self.update()

    @classmethod
    def display(self):
        res = []
        for playable in self.playing:
            res.append(playable.display())
        return res

    @classmethod
    def all(self):
        return self.playing

    @classmethod
    def update(self):
        if self.callback:
            self.callback()

    @classmethod
    def last(self):
        durs = list(map(lambda x: x.time_till_end, self.playing))
        if None in durs:
            return self.playing[durs.index(None)]
        else:
            return self.playing[durs.index(max(durs))]

    @classmethod
    def bind_callback(self, callback):
        self.callback = callback

    @classmethod
    def find(self, kw):
        for p in NowPlaying.playing:
            if p.keyword == kw:
                return p
            else:
                for n in p:
                    if n.keyword == kw:
                        return n
                    elif n.is_compound:
                        for k in n:
                            if k.keyword == kw:
                                return k
        return None
