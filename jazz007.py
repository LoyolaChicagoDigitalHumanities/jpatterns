import sys
from abjad import *

import common, sideman

# TODO: Fix weird chord spellings

def get_pattern7(jazz_scale):
    pitches = jazz_scale.get_named_pitches([1, 3, 5, 8])
    pitches.extend(map(lambda x: x+1, pitches))
    durations = [sideman.eighth] * 8
    notes = scoretools.make_notes(pitches, durations)

    measure = Measure((4, 4))
    for note in notes: 
        measure.append(note)
    return measure

def get_pattern7_chord_measure(jazz_scale):
    pitches = jazz_scale.get_chord_as_named([1, 3, 5])
    pitches2 = map(lambda x: x+1, pitches) 
    measure = Measure((4, 4))
    measure.append(Chord(pitches, (2, 4)))
    measure.append(Chord(pitches2, (2, 4)))
    return measure

def get_score():
    treble_pattern = Staff()
    chords = Staff(context_name='ChordNames')

    for key in range(0,12,2):
        jazz_scale = sideman.JazzScale(key)
        treble_pattern.append( get_pattern7(jazz_scale) )
        chords.append( get_pattern7_chord_measure(jazz_scale) )

    score = Score([chords, treble_pattern])
    tempo = Tempo(Duration(1, 4), (100, 138))
    attach(tempo, treble_pattern)
    return score

def title():
    return "Jazz Pattern 7"

def composer():
    return "Jerry Greene et al, Thiruvathukal, Moe"

def pdf():
    return "jazz007.pdf"

def midi():
    return "jazz007.midi"

if __name__ == '__main__' and False:
    score = get_score()
    common.main( score, title(), composer(), pdf())
    common.main( score, title(), composer(), midi())
