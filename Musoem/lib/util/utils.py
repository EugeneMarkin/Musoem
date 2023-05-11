import re, os, random
import datetime as dt

def get_bpm_from_path(path):
    dir_name = os.path.basename(path)
    return re.findall(r'bpm=([0-9]+)', dir_name)


def r(s, e, div):
    seed = dt.datetime.now().time().second
    random.seed(seed)

    print("returning ", l)
    return l

class R(list):

    def __init__(self, size, s, e, div):
        seed = dt.datetime.now().time().second
        self.size = size
        self.s = s
        self.e = e
        self.div = div
        random.seed(seed)
        l = []
        for i in range(0, size):
            l.append(random.randrange(s, e+1, 1)/float(div))
        super().__init__(l)


    def __copy__(self):
        print("calling the overriden copy")
        return self.__class__.__init__(self.size, self.s, self.e, self.div)

    def __deepcopy__(self, memo):
        print("calling the overriden deep copy")
        return R(self.size, self.s, self.e, self.div)

    @classmethod
    def minus1_to_1(self, size):
        return R(size, -10, 10, 10)
