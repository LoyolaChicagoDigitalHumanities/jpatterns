import sys
from abjad import *

import common, sideman

def get_pattern_n77(scale):
    pitches = sideman.get_pattern_pitches([1, 7, 2, 1, 3, "2s", 4, 3, 5, "4s", 6, 5, 8, 7, 9, 8], scale)
    durations = [sideman.eighth] * 16
    notes = scoretools.make_notes(pitches, durations)

    measure = Measure((8, 4))
    for note in notes: 
        measure.append(note)
    return measure

def get_pattern_n77_chords(scale):
    pitches = sideman.get_chord_pitches([1 ,3, 5], scale)
    measure = Measure((8, 4))
    chord = Chord(pitches, (4, 4))
    measure.append(chord)
    chord = Chord(pitches, (4, 4))
    measure.append(chord)
    return measure

def get_score():
    treble_pattern = Staff()
    chords = Staff(context_name='ChordNames')

    for key in sideman.keynames_in_fifths():
        scale = sideman.get_scale(key, 'major')
        pattern_measure = get_pattern_n77(scale)
        chord_measure =get_pattern_n77_chords(scale)
        treble_pattern.append( pattern_measure )
        chords.append( chord_measure )
    
    tempo = Tempo(Duration(1, 4), (100,138))
    attach(tempo, treble_pattern)
    score = Score([chords, treble_pattern])
    return score

def title():
    return "Jazz Pattern 77"

def composer():
    return "Jerry Greene et al, Thiruvathukal"

def pdf():
    return "jazz77.pdf"

def midi():
    return "jazz77.midi"

if __name__ == '__main__':
    common.main( get_score(), title(), composer(), pdf())
    common.main( get_score(), title(), composer(), midi())