sys.path.append("/Users/eugenemarkin/Projects/scoredot")

voc = FileSynthDef("vsample")
voc.add()

p1 >> voc(degree = 2, dur = 4, bnum = 2)
