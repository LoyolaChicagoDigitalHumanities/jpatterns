#
# Proof of concept for Pattern 13

from abjad import *
import sideman
js = sideman.JazzScale(0)
m = Measure( (8, 4) )
m.append( Note("c'", (1, 2)))
m.append( Note("e'", (1, 8)))
m.append( Note("g'", (1, 4)))
m.append( Note("a'", (1, 8)))
m.append( Note("a'", (4, 4)))
t = spannertools.Tie()
attach(t, m[3:5])
print(t)
staff = Staff()
staff.append(m)
print(staff)
mutate(staff[0:1]).split([Duration(4,4), Duration(4,4)])
print("mutated ",staff)
show(staff)



