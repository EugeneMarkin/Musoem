from operations import Section, SectionGroup, ControlOperation


class NowPlaying:

    sections = {}
    control = {}

    @classmethod
    def reset(self):
        for item in (list(self.sections.values()) + list(self.control.values())):
            item.stop()
            item.reset()
        self.sections = {}
        self.control = {}

    @classmethod
    def add(self, obj, reps = None):
        print("adding ", obj)
        if isinstance(obj, Section) or isinstance(obj, SectionGroup):
            obj.play(obj._times)
            self.sections[obj.keyword] = obj
        elif isinstance(obj, ControlOperation):
            obj.play()
            self.control[obj.keyword] = obj

    @classmethod
    def remove(self, keyword):
        if keyword in self.sections:
            section = self.sections[keyword]
            section.stop()
            self.sections.pop(keyword)
        elif keyword in self.control:
            control_item = self.control[keyword]
            control_item.stop()
            self.control.pop(keyword)
        else:
            # look for keyword in section operations
            for section in list(self.sections.values()):
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
