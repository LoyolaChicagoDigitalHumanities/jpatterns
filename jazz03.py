import sys
from abjad import *

import common, sideman

# This is a 5/4 pattern!

def get_pattern3(jazz_scale):
    pitches = jazz_scale.get_named_pitches([1, 3, 5, 8, 8, 5, 3, 1, 1])
    durations = [sideman.eighth] * 4 + [sideman.eighth] * 4 + [sideman.quarter]
    notes = scoretools.make_notes(pitches, durations)

    measure = Measure((5, 4))
    for note in notes: 
        measure.append(note)
    tie = spannertools.Tie()
    attach(tie, measure[3:5])
    tie = spannertools.Tie()
    attach(tie, measure[7:9])
    return measure

def get_pattern3_chord_measure(jazz_scale):
    pitches = jazz_scale.get_chord_as_named([1 ,3, 5])
    measure = Measure((5, 4))
    chord = Chord(pitches, (4, 4))
    measure.append(chord)
    multiplier = Multiplier(measure.time_signature.duration)
    attach(multiplier, chord)
    return measure

def get_score():
    treble_pattern = Staff()
    chords = Staff(context_name='ChordNames')

    for key in sideman.keys_in_order():
        jazz_scale = sideman.JazzScale(key)
        treble_pattern.append( get_pattern3(jazz_scale) )
        chords.append( get_pattern3_chord_measure(jazz_scale) )

    score = Score([chords, treble_pattern])
    tempo = Tempo(Duration(1, 4), (80, 132))
    attach(tempo, treble_pattern)
    return score

def title():
    return "Jazz Pattern 3"

def composer():
    return "Jerry Greene et al, Thiruvathukal"

def pdf():
    return "jazz03.pdf"

def midi():
    return "jazz03.midi"


if __name__ == '__main__':
    common.main( get_score(), title(), composer(), 'jazz3.pdf')
    common.main( get_score(), title(), composer(), 'jazz3.midi')