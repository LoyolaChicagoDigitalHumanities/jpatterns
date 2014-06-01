import sys
from abjad import *

import common, sideman

def get_pattern16(jazz_scale):
    pitches = jazz_scale.get_named_pitches([1, 3, 5, 6, 5, 3, 1])
    durations = [sideman.eighth] * 6 + [sideman.quarter]
    notes = scoretools.make_notes(pitches, durations)

    measure = Measure((4, 4))
    for note in notes: 
        measure.append(note)
    return measure

def get_pattern16_chord_measure(jazz_scale):
    pitches = jazz_scale.get_chord_as_named([1 ,3, 5, 6])
    measure = Measure((4, 4))
    chord = Chord(pitches, (4, 4))
    measure.append(chord)
    return measure

def get_score():
    treble_pattern = Staff()
    chords = Staff(context_name='ChordNames')

    for key in sideman.keys_in_hmm():
        jazz_scale = sideman.JazzScale(key)
        treble_pattern.append( get_pattern16(jazz_scale) )
        chords.append( get_pattern16_chord_measure(jazz_scale) )

    score = Score([chords, treble_pattern])
    tempo = Tempo(Duration(1, 4), (138, 192))
    attach(tempo, treble_pattern)
    return score

def title():
    return "Jazz Pattern 16"

def composer():
    return "Jerry Greene et al, Thiruvathukal"

def pdf():
    return "jazz016.pdf"

def midi():
    return "jazz016.midi"

if __name__ == '__main__':
    common.main( get_score(), title(), composer(), pdf())
    common.main( get_score(), title(), composer(), midi())