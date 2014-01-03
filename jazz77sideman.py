import sys
from abjad import *

import common, sideman

# This is a 5/4 pattern!

#
# This patern needs to fill a (4, 4) measure with (2, 4) worth of notes at a time
# I didn't figure out how to combine two Measure instances into a single one via Abjad
#

def get_pattern_n77(scale):
    pitches = scale.get_altered_pitches_as_named([1, -7, 2, 1, 3, "2s", 4, 3, 5, "4s", 6, 5, 8, 7, 9, 8])
    print(pitches)
    durations = [sideman.eighth] * 16
    notes = scoretools.make_notes(pitches, durations)

    measure = Measure((8, 4))
    for note in notes: 
        measure.append(note)
    return measure

def get_pattern_n77_chords(scale):
    pitches = scale.get_chord_as_named([1 ,3, 5])
    measure = Measure((8, 4))
    chord = Chord(pitches, (4, 4))
    measure.append(chord)
    multiplier = Multiplier(measure.time_signature.duration)
    attach(multiplier, chord)
    return measure

def get_score():
    treble_pattern = Staff()
    chords = Staff(context_name='ChordNames')

    for key in sideman.keys_in_fifths():
        scale = sideman.JazzScale(key)
        pattern_measure = get_pattern_n77(scale)
        chord_measure =get_pattern_n77_chords(scale)
        treble_pattern.append( pattern_measure )
        chords.append( chord_measure )
    
    mutate(treble_pattern[:]).split([(4, 4)], cyclic=True)
    #mutate(chords[:]).split([(4, 4)], cyclic=True)



#    staves = [chords, treble_pattern]
#    for staff in staves:
#        parts = sequencetools.partition_sequence_by_counts(staff[:], [2], cyclic=True)
#        for part in parts:
#            mutate(part).fuse()

    #tempo = Tempo(Duration(1, 4), (100,138))
    tempo = Tempo(Duration(1, 4), 100)

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
#    common.main( get_score(), title(), composer(), midi())