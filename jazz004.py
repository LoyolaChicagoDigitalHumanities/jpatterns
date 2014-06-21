import sys
from abjad import *

import common, sideman

def get_pattern4(jazz_scale):
    pitches = jazz_scale.get_named_pitches([1, 3, 5, 8, 8])
    durations = [sideman.eighth] * 4 + [sideman.quarter]
    notes = scoretools.make_notes(pitches, durations)

    measure = Measure((4, 4))
    for note in notes: 
        measure.append(note)
    measure.append(Rest('r4'))
    tie = spannertools.Tie()
    attach(tie, measure[3:5])
    return measure

def get_pattern4_chord_measure(jazz_scale):
    pitches = jazz_scale.get_chord_as_named([1 ,3, 5])
    measure = Measure((4, 4))
    chord = Chord(pitches, (4, 4))
    measure.append(chord)
    multiplier = Multiplier(measure.time_signature.duration)
    attach(multiplier, chord)
    return measure

def get_score():
    treble_pattern = Staff()
    chords = Staff(context_name='ChordNames')

    for key in (0, 3, 6, 9, 5, 8, 11, 2, 10, 1, 4, 7):
        jazz_scale = sideman.JazzScale(key)
        treble_pattern.append( get_pattern4(jazz_scale) )
        chords.append( get_pattern4_chord_measure(jazz_scale) )

    score = Score([chords, treble_pattern])
    tempo = Tempo(Duration(1, 4), (100, 132))
    attach(tempo, treble_pattern)
    return score

def title():
    return "Jazz Pattern 4"

def composer():
    return "Jerry Greene et al, Thiruvathukal, Moe"

def pdf():
    return "jazz004.pdf"

def midi():
    return "jazz004.midi"

if __name__ == '__main__':
    score = get_score()
    common.main( score, title(), composer(), pdf())
    common.main( score, title(), composer(), midi())
