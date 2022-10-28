class NowPlaying:

    sections = {}
    control = {}
    callback = None

    @classmethod
    def reset(self):
        for item in (list(self.sections.values()) + list(self.control.values())):
            item.stop()
            item.reset()
        self.sections = {}
        self.control = {}

    @classmethod
    def add_section(self, section):
        section.play(section._times)
        self.sections[section.keyword] = section

    @classmethod
    def add_operation(self, operation):
        operation.play()
        self.control[operation.keyword] = operation

    @classmethod
    def remove(self, keyword):
        if keyword in self.sections:
            section = self.sections[keyword]
            if section._next is not None:
                self.sections[section._next.keyword] = section._next
            self.sections.pop(keyword)
        elif keyword in self.control:
            self.control.pop(keyword)
        if self.callback is not None:
            self.callback()

    @classmethod
    def stop(self, keyword):
        print("trying to remove keyword", keyword)
        print("sections are", self.sections)
        if keyword in self.sections:
            section = self.sections[keyword]
            section.stop()
        elif keyword in self.control:
            control_item = self.control[keyword]
            control_item.stop()
        else:
            # look for keyword in section operations
            for section in list(self.sections.values()):
                current = section
                while current._next is not None:
                    NowPlaying.stop_operation(current, keyword)
                    if current._next.keyword == keyword:
                        current._next = None
                        break
                    current = current._next

    @classmethod
    def stop_operation(self, section, keyword):
        if keyword in section.operations:
            section.reset(keyword)

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
