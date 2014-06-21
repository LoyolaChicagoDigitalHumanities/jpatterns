import sys
from abjad import *

import common, sideman

def get_pattern6(jazz_scale, ascend):
    pitches = jazz_scale.get_named_pitches([1, 3, 5, 8])
    durations = [sideman.quarter] * 4
    notes = scoretools.make_notes(pitches, durations)

    measure = Measure((4, 4))
    for note in notes: 
        measure.append(note)
    if not ascend:
        measure.reverse()
    return measure

def get_pattern6_chord_measure(jazz_scale):
    pitches = jazz_scale.get_chord_as_named([1, 3, 5])
    measure = Measure((4, 4))
    chord = Chord(pitches, (4, 4))
    measure.append(chord)
    return measure

def get_score():
    treble_pattern = Staff()
    chords = Staff(context_name='ChordNames')

    for key in sideman.keys_in_order():
        jazz_scale = sideman.JazzScale(key)
        treble_pattern.append( get_pattern6(jazz_scale, key % 2 == 1) )
        chords.append( get_pattern6_chord_measure(jazz_scale) )

    score = Score([chords, treble_pattern])
    tempo = Tempo(Duration(1, 4), (100, 160))
    attach(tempo, treble_pattern)
    return score

def title():
    return "Jazz Pattern 6"

def composer():
    return "Jerry Greene et al, Thiruvathukal, Moe"

def pdf():
    return "jazz006.pdf"

def midi():
    return "jazz006.midi"

if __name__ == '__main__':
    score = get_score()
    common.main( score, title(), composer(), pdf())
    common.main( score, title(), composer(), midi())
