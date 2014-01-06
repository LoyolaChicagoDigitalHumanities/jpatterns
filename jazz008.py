import sys
from abjad import *

import common, sideman

# This is a 5/4 pattern!

#
# This patern needs to fill a (4, 4) measure with (2, 4) worth of notes at a time
# I didn't figure out how to combine two Measure instances into a single one via Abjad
#

def get_pattern8(jazz_scale):
    pitches = jazz_scale.get_named_pitches([1, 3, 5, 8])
    durations = [sideman.eighth] * 4
    notes = scoretools.make_notes(pitches, durations)

    measure = Measure((2, 4))
    for note in notes: 
        measure.append(note)
    return measure

def get_pattern8_chord_measure(jazz_scale):
    pitches = jazz_scale.get_chord_as_named([1 ,3, 5])
    measure = Measure((2, 4))
    chord = Chord(pitches, (2, 4))
    measure.append(chord)
    return measure

def get_score():
    treble_pattern = Staff()
    chords = Staff(context_name='ChordNames')

    for key in sideman.keys_in_fifths():
        jazz_scale = sideman.JazzScale(key)
        pattern_measure = get_pattern8(jazz_scale)
        chord_measure =get_pattern8_chord_measure(jazz_scale)
        treble_pattern.append( pattern_measure )
        chords.append( chord_measure )

    # Merge all the pairs of 2/4 measures into 4/4 measures

    # TODO: Can probably just put a loop over both staves...
    
    staves = [chords, treble_pattern]
    for staff in staves:
        parts = sequencetools.partition_sequence_by_counts(staff[:], [2], cyclic=True)
        for part in parts:
            mutate(part).fuse()

    tempo = Tempo(Duration(1, 4), (100,138))
    attach(tempo, treble_pattern)
    score = Score([chords, treble_pattern])
    return score

def title():
    return "Jazz Pattern 8"

def composer():
    return "Jerry Greene et al, Thiruvathukal"

def pdf():
    return "jazz008.pdf"

def midi():
    return "jazz008.midi"

if __name__ == '__main__':
    score = get_score()
    common.main( score, title(), composer(), pdf())
    common.main( score, title(), composer(), midi())