import sys
from abjad import *

import common, sideman

# This is a 5/4 pattern!

#
# This patern needs to fill a (4, 4) measure with (2, 4) worth of notes at a time
# I didn't figure out how to combine two Measure instances into a single one via Abjad
#

def get_pattern_ii_v_i(scale):
    pitches = scale.get_altered_pitches_as_named([2, 3, 4, "4s", 5, 4, 3, 2, 1, 3, 5, 7, 8, 5, 3])
    durations = [sideman.eighth] * 16
    notes = scoretools.make_notes(pitches, durations)

    measure = Measure((8, 4))
    for note in notes: 
        measure.append(note)
    return measure

def get_pattern_ii_v_i_chords(scale):
    pitches = scale.get_chord_as_named([1 ,3, 5])
    measure = Measure((8, 4))
    chord = Chord(pitches, (4, 4))
    measure.append(chord)
    multiplier = Multiplier(measure.time_signature.duration)
    attach(multiplier, chord)
    return measure

# TODO: Put this in bass cleff for piano version.
# Should be a matter of transposing a couple of octaves down and using a bass clef staff.
def get_pattern_ii_v_i_voicing(scale):
    measure = Measure((8, 4))
    ii_chord = Chord(scale.get_chord_as_named([2, 4, 6, 8]), (2, 4))
    v_chord = Chord(scale.get_chord_as_named([2, 4, 5, 7]), (2, 4))
    i_chord = Chord(scale.get_chord_as_named([1, 3, 5, 7]), (4, 4))
    measure.append(ii_chord)
    measure.append(v_chord)
    measure.append(i_chord)
    return measure

def get_score():
    treble_pattern = Staff()
    chords = Staff(context_name='ChordNames')
    voicing = Staff()
    for key in sideman.keys_for_ii_v_i_descending():
        scale = sideman.JazzScale(key)
        pattern_measure = get_pattern_ii_v_i(scale)
        chord_measure =get_pattern_ii_v_i_chords(scale)
        voicing_measure = get_pattern_ii_v_i_voicing(scale)
        treble_pattern.append( pattern_measure )
        chords.append( chord_measure )
        voicing.append(voicing_measure)
    
    mutate(treble_pattern[:]).split([(4, 4)], cyclic=True)
    mutate(voicing[:]).split([(4, 4)], cyclic=True)
    #mutate(chords[:]).split([(4, 4)], cyclic=True)



#    staves = [chords, treble_pattern]
#    for staff in staves:
#        parts = sequencetools.partition_sequence_by_counts(staff[:], [2], cyclic=True)
#        for part in parts:
#            mutate(part).fuse()

    #tempo = Tempo(Duration(1, 4), (100,138))
    tempo = Tempo(Duration(1, 4), 100)

    attach(tempo, treble_pattern)
    score = Score([chords, treble_pattern, voicing])
    return score

def title():
    return "II-V-I Progression"

def composer():
    return "Unknown"

def pdf():
    return "ii-v-i.pdf"

def midi():
    return "ii-v-i.midi"

if __name__ == '__main__':
    score = get_score()
    common.main( score, title(), composer(), pdf())
    common.main( score, title(), composer(), midi())