class NowPlaying:

    playing = {}
    callback = None

    @classmethod
    def reset(self):
        for item in self.playing.values():
            item.stop()
            item.reset()
        self.playing = {}

    @classmethod
    def play(self, playable):
        playable(playable._times)
        self.playing[playable.keyword] = playable
        if self.callback is not None:
            self.callback()

    @classmethod
    def apply_operation(self, operation, section):
        operation.apply_to(section)
        self.callback()

    @classmethod
    def remove(self, keyword):
        if keyword in self.playing:
            playable = self.playing[keyword]
            self.playing.pop(keyword)

        if self.callback is not None:
            self.callback()


    @classmethod
    def stop(self, keyword):
        if keyword in self.playing:
            self.playing[keyword].stop()
        else:
            map(lambda p: p.stop(keyword), self.playing)

    @classmethod
    def display(self):
        res = ""
        print(self.sections, self.control)
        for section in list(self.sections.values()):
            res += section.display() + "\n"
        for control_item in list(self.control.values()):
            res += control.keyword + " "
        return res


    @classmethod
    def last_section(self):
        return self.sections[list(self.sections.keys())[-1]]

    @classmethod
    def bind_callback(self, callback):
        self.callback = callback
