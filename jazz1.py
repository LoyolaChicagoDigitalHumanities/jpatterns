import sys
from abjad import *

import common

# I think Abjad had some change where notetools was removed...now scoretools, ok. :)
notetools = scoretools

def jazz1(pitch_delta=0):
    transpose = common.transpose(pitch_delta)
    pitches = map(transpose, [0, 4, 7, 12, 7, 4, 0])
    durations = [common.eighth] * 3 + [common.eighth] * 3 + [common.half]
    notes = notetools.make_notes(pitches, durations)

    key=pitches[0]
    common.respell_notes(notes, key)
    t1_notes = notes[0:3]
    t2_notes = notes[3:6]
    landing_note = notes[6:]
    t1 = Tuplet(Fraction(2, 3), t1_notes)
    t2 = Tuplet(Fraction(2, 3), t2_notes)
    return [t1, t2] + landing_note


# This pattern is linear in all 12 keys (e.g. c', df', d', ...)
def get_score():
    notes = []
    for i in range(0, 12):
        notes = notes + jazz1(i)

    # The parameter (1) here means whole note for each chord symbol (to keep things general for other patterns)
    chord_string = common.get_lilypond_major_chords(1)
    staff = Staff(notes)
    chords = Staff(chord_string, context_name='ChordNames')
    score = Score([chords, staff])
    return score

def title():
    return "Jazz Pattern 1"

def composer():
    return "Jerry Greene et al"

def main():
    lilypond_file = common.get_lilypond_file(get_score(), title(), composer())
    show(lilypond_file)

if __name__ == '__main__':
    main()

