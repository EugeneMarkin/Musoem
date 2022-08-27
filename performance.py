"""
section(N): play section N times, loop if N is None
 >> : play next section after this one stops playing
 * : play section N times
 + : start the right section when the left section starts
 ~ : stop playing section
 """


sb1()


sb1 >> sm13*2 + sh19*3 >> sb1

sb1 >> sb1*2

~sb1
