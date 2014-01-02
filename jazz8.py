import sys
from abjad import *

import common, sideman

# This is a 5/4 pattern!

#
# This patern needs to fill a (4, 4) measure with (2, 4) worth of notes at a time
# I didn't figure out how to combine two Measure instances into a single one via Abjad
#

def get_pattern8(jazz_scale, measure):
    pitches = jazz_scale.get_named_pitches([1, 3, 5, 8])
    durations = [sideman.eighth] * 4
    notes = scoretools.make_notes(pitches, durations)

    for note in notes: 
        measure.append(note)
    return measure

def get_pattern8_chord_measure(jazz_scale, measure):
    pitches = jazz_scale.get_chord_as_named([1 ,3, 5])
    chord = Chord(pitches, (2, 4))
    measure.append(chord)
    return measure

def get_score():
    treble_pattern = Staff()
    chords = Staff(context_name='ChordNames')

    keys_in_fifths = list(sideman.keys_in_fifths())
    for i in range(0, len(keys_in_fifths), 2):
        jazz_scale1 = sideman.JazzScale(keys_in_fifths[i])
        jazz_scale2 = sideman.JazzScale(keys_in_fifths[i+1])
        pattern_measure = Measure((4, 4))
        chord_measure = Measure((4, 4))
        get_pattern8(jazz_scale1, pattern_measure)
        get_pattern8(jazz_scale2, pattern_measure)
        treble_pattern.append( pattern_measure )
        get_pattern8_chord_measure(jazz_scale1, chord_measure)
        get_pattern8_chord_measure(jazz_scale2, chord_measure)
        chords.append( chord_measure )

    tempo = Tempo(Duration(1, 4), (100, 138))
    attach(tempo, treble_pattern)
    score = Score([chords, treble_pattern])
    return score

def title():
    return "Jazz Pattern 8"

def composer():
    return "Jerry Greene et al, Thiruvathukal"

def pdf():
    return "jazz8.pdf"

def midi():
    return "jazz8.midi"

if __name__ == '__main__':
    common.main( get_score(), title(), composer(), pdf())
    common.main( get_score(), title(), composer(), midi())