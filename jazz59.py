import sys
from abjad import *

import common, sideman

# This is a 5/4 pattern!

def get_pattern59(jazz_scale):
    pitches = jazz_scale.get_named_pitches([5, 8, 6, 4, 2, 5, 3, 1])
    durations = [sideman.eighth] * 8
    notes = scoretools.make_notes(pitches, durations)

    measure = Measure((4, 4))
    for note in notes: 
        measure.append(note)
    return measure

def get_pattern59_chord_measure(jazz_scale):
    pitches = jazz_scale.get_chord_as_named([1 ,3, 5])
    measure = Measure((4, 4))
    chord = Chord(pitches, (4, 4))
    measure.append(chord)
    return measure

def get_score():
    treble_pattern = Staff()
    chords = Staff(context_name='ChordNames')

    for key in sideman.keys_in_order():
        jazz_scale = sideman.JazzScale(key)
        treble_pattern.append( get_pattern59(jazz_scale) )
        chords.append( get_pattern59_chord_measure(jazz_scale) )

    score = Score([chords, treble_pattern])
    return score

def title():
    return "Jazz Pattern 59"

def composer():
    return "Jerry Greene et al"

def pdf():
    return "jazz59.pdf"

def midi():
    return "jazz59.midi"

if __name__ == '__main__':
    common.main( get_score(), title(), composer(), pdf())
    common.main( get_score(), title(), composer(), midi())