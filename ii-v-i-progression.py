import sys
import argparse

from abjad import *

import common, sideman

def get_pattern_ii_v_i(scale):
    pitches = scale.get_altered_pitches_as_named([2, 3, 4, "4s", 5, 4, 3, 2, 1, 3, 5, 7, 8, 7, 5, 3])
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

def get_pattern_ii_v_i_voicing(scale):
    measure = Measure((8, 4))
    ii_chord = Chord(scale.get_chord_as_named([4, 6, 8, 10]), (2, 4))
    v_chord = Chord(scale.get_chord_as_named([4, 6, 7, 10]), (2, 4))
    i_chord = Chord(scale.get_chord_as_named([3, 5, 7, 9]), (4, 4))
    measure.append(ii_chord)
    measure.append(v_chord)
    measure.append(i_chord)
    return measure

def get_score(key_name):

    # This pattern is computed starting in C (II, V, and I in C).
    # By specifying key_name == 'F", we can transform it accordingly

    bass_pattern = Staff()
    chords = Staff(context_name='ChordNames')
    voicing = Staff()
    for key in sideman.keys_for_ii_v_i_descending():
        scale = sideman.JazzScale(key)
        pattern_measure = get_pattern_ii_v_i(scale)
        chord_measure =get_pattern_ii_v_i_chords(scale)
        voicing_measure = get_pattern_ii_v_i_voicing(scale)
        bass_pattern.append( pattern_measure )
        chords.append( chord_measure )
        voicing.append(voicing_measure)

    if  key_name == 'F':
        key_offset = -7
        voice_offset = 12
    else:
        voice_offset = 0
        key_offset = 0

    mutate(voicing).transpose(-12 + key_offset + voice_offset)
    mutate(bass_pattern).transpose(-24 + key_offset)
    mutate(chords).transpose(key_offset)
    clef = Clef('bass')
    attach(clef, bass_pattern)    

    mutate(bass_pattern[:]).split([(4, 4)], cyclic=True)
    mutate(voicing[:]).split([(4, 4)], cyclic=True)
    #mutate(chords[:]).split([(4, 4)], cyclic=True)

    tempo = Tempo(Duration(1, 4), 100)

    attach(tempo, bass_pattern)
    score = Score([chords, voicing, bass_pattern])
    return score

def title(key_name):
    return "II-V-I Progression (in %s), Piano" % key_name

def composer():
    return "Not Specified"

def pdf(key_name):
    return "ii-v-i-%s.pdf" % key_name.lower()

def midi(key_name):
    return "ii-v-i-%s.midi" % key_name.lower()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="compute the II-V-I progression exercise in C or F")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-c", "--key_of_c", action="store_true")
    group.add_argument("-f", "--key_of_f", action="store_true")
    args = parser.parse_args()

    key_name = 'f' if args.key_of_f else 'c'
    key_name = key_name.upper()

    print("Creating II-V-I in key of %s" % key_name)
    score = get_score(key_name)
    common.main( score, title(key_name), composer(), pdf(key_name))
    common.main( score, title(key_name), composer(), midi(key_name))