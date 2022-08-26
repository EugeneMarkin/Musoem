# initial setup for scoredot to run with FoxDot
sys.path.append("/Users/eugenemarkin/Projects/scoredot")
from score import Score
from music21.stream.base import Score as M21Score
from music21 import converter
# score file path
fp = "~/Documents/time_files_full.musicxml"
# load the score into musc21
m21_score = converter.parse(fp, format = "musicxml")
instr_map = {"Sine Bass" : "midi 1", "Sine Mid" : "midi 2",
             "Sine Sub" : "midi 3", "Sine Hi" : "midi 4",
             "FB Mid" : "midi 5", "FB Hi" : "midi 6",
             "Voice Low" : "midi 7", "Voice Hi" : "midi 8"}
# parse the score and assign instruments to play parts
score = Score(m21_score, instr_map)
# this gives the parts in the score
print(score.parts.keys())

sb1 = score.section(1, 4, "Sine Bass") # loop
sb109 = score.section(109, 119, "Sine Bass") # once
sb121 = score.section(121, 124, "Sine Bass") # loop
sm13 = score.section(13, 16, "Sine Mid") # loop
sm109 = score.section(109, 112, "Sine Mid") # once
sm114 = score.section(114, 116, "Sine Mid") # loop
sm189 = score.section(189, 197, "Sine Mid") # 3 times
ss19 = score.section(19, 22, "Sine Sub") # loop
ss109 = score.section(109, 116, "Sine Sub") # once
ss170 = score.section(170, 181, "Sine Sub") # 5 times
sh19 = score.section(19, 22, "Sine Hi") # loop
sh109 = score.section(109, 117, "Sine Hi") # play 4 times
sh141 = score.section(141, 144, "Sine Hi") # 6 times
sh170 = score.section(170, 173, "Sine Hi") # 4 times
sh190 = score.section(190, 193, "Sine Hi") # 4 times
sh206 = score.section(206, 209, "Sine Hi") # 2 times
sh222 = score.section(222, 225, "Sine Hi") # 4 times
fbm77 = score.section(77, 83, "FB Mid") # once
fbm109 = score.section(109, 149, "FB Mid") # once
fbm150 = score.section(150, 153, "FB Mid") # loop
fbh69 = score.section(69, 76, "FB Hi") # 4 times
fbh125 = score.section(125, 132, "FB Hi") # 3 times
fbh167 = score.section(167, 173, "FB Hi") # once
fbh174 = score.section(174, 184, "FB Hi") # 3 times
vl90 = score.section(90, 109, "Voice Low") # once
vl133 = score.section(133, 154, "Voice Low") # once
vl170 = score.section(170, 181, "Voice Low") # once
vl182 = score.section(182, 185, "Voice Low") # 13 times
vl186 = score.section(186, 186, "Voice Low") # every 2 measures since 186
vl220 = score.section(220, 224, "Voice Low") # 3 times
vl228 = score.section(228, 228, "Voice Low") # overlay since 228, add octave above
vh102 = score.section(102, 102, "Voice Hi") # once or twice
vh141 = score.section(141, 145, "Voice Hi") # 2 times
