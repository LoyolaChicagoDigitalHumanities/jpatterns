import sys

from abjad import *
import common, sideman

def get_pattern15(jazz_scale):
    pitches = jazz_scale.get_named_pitches([1, 3, 5, 6, 5, 3, 1])
    durations = [sideman.eighth] * 3 + [sideman.eighth] * 3 + [sideman.half]
    notes = scoretools.make_notes(pitches, durations)

    t1_notes = notes[0:3]
    t2_notes = notes[3:6]
    last_note = notes[6]
    t1 = Tuplet(Fraction(2, 3), t1_notes)
    t2 = Tuplet(Fraction(2, 3), t2_notes)
    measure = Measure((4, 4))
    measure.append(t1)
    measure.append(t2)
    measure.append(last_note)
    return measure

def get_pattern15_chord_measure(jazz_scale):
    pitches = jazz_scale.get_chord_as_named([1 ,3, 5, 6])
    measure = Measure( (4, 4))
    chord = Chord(pitches, (4, 4))
    measure.append(chord)
    return measure

def get_score():
    treble_pattern = Staff()
    chords = Staff(context_name='ChordNames')
    for key in sideman.keys_in_fifths():
        jazz_scale = sideman.JazzScale(key)
        treble_pattern.append( get_pattern15(jazz_scale) )
        chords.append( get_pattern15_chord_measure(jazz_scale) )
    score = Score([chords, treble_pattern])
    tempo = Tempo(Duration(1, 4), (138, 192))
    attach(tempo, treble_pattern)
    return score

def title():
    return "Jazz Pattern 15"

def composer():
    return "Jerry Greene et al, Thiruvathukal"

def pdf():
    return "jazz015.pdf"

def png():
    return "jazz015.png"

def midi():
    return "jazz015.midi"

if __name__ == '__main__':
    score = get_score()
    common.main( score, title(), composer(), pdf())
    common.main( score, title(), composer(), midi())


