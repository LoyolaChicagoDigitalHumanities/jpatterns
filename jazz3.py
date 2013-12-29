import sys
from abjad import *

import common

# This pattern generates a 5/4 measure's worth of notes

def pattern3(pitch_delta=0):
    transpose = common.transpose(pitch_delta)
    pitches = map(transpose, [0, 4, 7, 12, 12, 7, 4, 0])
    durations = [common.eighth] * 4 + [common.eighth] * 4 + [common.quarter]
    notes = scoretools.make_notes(pitches, durations)

    key=pitches[0]
    common.respell_notes(notes, key)
    t1_notes = notes[0:3]
    t2_notes = notes[3:6]
    landing_note = notes[6:]
    return t1_notes + t2_notes + landing_note


# This pattern is linear in all 12 keys (e.g. c', df', d', ...)
def get_score():
    notes = []
    note_count = 0
    slurs = []
    for i in range(0, 12):
        p3 = pattern3(i)
        notes = notes + p3
        slurs.append( (note_count+3, note_count+4) )
        slurs.append( (note_count+7, note_count+8) )
        note_count += len(p3)

    # The parameter (1) here means whole note for each chord symbol (to keep things general for other patterns)
    chord_string = common.get_lilypond_major_chords(1, 4)
    staff = Staff(notes)

    for (slur_start, slur_end) in slurs:
        slur = spannertools.Slur()
        attach(slur, staff[slur_start:slur_end+1])

    chords = Staff(chord_string, context_name='ChordNames')
    score = Score([chords, staff])
    time_signature = indicatortools.TimeSignature((5, 4))
    attach(time_signature, staff)
    attach(time_signature, chords)
    return score

def title():
    return "Jazz Pattern 3"

def composer():
    return "Jerry Greene et al"

def filename():
    return "jazz3.pdf"

if __name__ == '__main__':
    common.main( get_score(), title(), composer(), filename())
