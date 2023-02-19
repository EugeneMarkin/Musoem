from enum import Enum

class TextMark:


    def __init__(self, text, measure_num):
        p = text.split(":")
        if len(p) == 1:
            self.text = text.strip()
            self.length = 1
        elif len(p) == 2:
            self.text = p[0].strip()
            self.length = int(p[1].strip())

        self.measure_num = measure_num
