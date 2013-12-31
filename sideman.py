#
# sideman.py (a.k.a. sideperson.py) - a collection of utilties that act as a "side man"
# (in the Jazz sense) to the Abjad toolkit. These tools are strictly aimed at 
# faciliting work with jazz and jazz patterns.
#

from abjad import *

import unittest
import os, os.path

flats = 'flat'
sharps = 'sharp'
naturals = 'naturals'
eighth = Duration(1, 8)
quarter = Duration(1, 4)
half = Duration(1, 2)
whole = Duration(1, 1)

class JazzScale(object):
    KEY_SPELLINGS = [naturals, flats, sharps, flats, sharps, flats, flats, 
       sharps, flats, sharps, flats, sharps]


    def __init__(self, key=0):
        self.key = key                         # should be 0...11
        self.spelling = JazzScale.KEY_SPELLINGS[self.key]     # this can be set by user.
        self.set_major_mode()

    def set_spelling_sharps(self):
        self.spelling = sharps
        self.respell()

    def set_spelling_flats(self):
        self.spelling = flats
        self.respell()

    def set_spelling_naturals(self):
        self.spelling = naturals
        self.respell()

    def reset_spelling(self):
        self.spelling = KEY_SPELLINGS[self.key]
        self.respell()

    # Internal Methods

    def set_major_mode(self):
        self.steps = [2, 2, 1, 2, 2, 2, 1]
        self.compute_jazz_scale()

    def set_minor_mode(self):
        self.steps = [2, 1, 2, 2, 1, 2, 2] 
        self.compute_jazz_scale()

    def set_key(self, key):
        self.key = key
        self.compute_jazz_scale()
    
    def pitch_iterator(self):
        pitch = self.key
        while True:
            for step in self.steps:
                yield pitch
                pitch = pitch + step

    def compute_jazz_scale(self):
        pitches = self.pitch_iterator()
        self.scale = [ pitches.next() for i in range(0, 15)]
        self.initialize_pitches()
        self.respell()

    def initialize_pitches(self):
        self.pitches = [ NamedPitch(pitch) for pitch in self.scale ]


    def respell(self):
        if self.spelling == flats:
            self.respell_as_flats()
        elif self.spelling == sharps:
            self.respell_as_sharps()
        else:
            pass

    def respell_as_flats(self):
        for n in range(0, len(self.pitches)):
            named_pitch = self.pitches[n]
            if named_pitch.accidental.name == sharps:
                self.pitches[n] = named_pitch.respell_with_flats()

    def respell_as_sharps(self):
        for n in range(0, len(self.pitches)):
            named_pitch = self.pitches[n]
            if named_pitch.accidental.name == flats:
                self.pitches[n] = named_pitch.respell_with_sharps()

    # Interface Methods (users may also use set_major_mode/set_minor_mode)

    def get_chord_as_numbered(self, pitch_list):
        return [ self.get_numbered_pitch(i) for i in pitch_list]

    def get_chord_as_named(self, pitch_list):
        return [ self.get_named_pitch(i) for i in pitch_list]

    def get_chord_as_lilypond(self, pitch_list):
        return "<%s>" % " ".join([ str(self.get_named_pitch(i)) for i in pitch_list])

    def get_numbered_pitch(self, n):
        assert n > 0 and n < 16
        return self.scale[n-1]

    def get_named_pitch(self, n):
        assert n > 0 and n < 16
        return self.pitches[n-1]

    def get_named_pitches(self, list_of_numbers):
        return [ self.get_named_pitch(i) for i in list_of_numbers ]

def linear():
    for i in range(0, 12):
        yield i

def fifths():
    for i in range(0, 12):
        yield 5*i % 12

def get_lilypond_major_chords(duration, spacer_rest=0, iterate=linear):

    # This is Lilyponds way of having a rest without generating a rest symbol.
    # In the case of a Lilypond chord, this means a chord will not be displayed on that beat.
    if spacer_rest > 0:
        spacer = " s%d" % spacer_rest
    else:
        spacer = ""

    key_iterator = iterate()

    return ' '.join([ m_chords[i] + str(duration) + spacer for i in key_iterator])

def respell_notes(notes, key):
    how_to_spell = respellings[key]
    if how_to_spell == flats:
        respell_as_flats(notes)
    elif how_to_spell == sharps:
        respell_as_sharps(notes)
    else:
        pass

def respell_as_flats(notes):
    for note in notes:
        written_pitch = note.written_pitch
        accidental_name = written_pitch.accidental.name
        if accidental_name == 'sharp':
            note.written_pitch = written_pitch.respell_with_flats()

def respell_as_sharps(notes):
    for note in notes:
        written_pitch = note.written_pitch
        accidental_name = written_pitch.accidental.name
        if accidental_name == 'flat':
            note.written_pitch = written_pitch.respell_with_sharps()

def transpose(pitch_delta):
    return lambda x : x + pitch_delta

def get_chords(jazz_number_list):
    chords = []
    js = JazzScale()
    for i in range(0, 12):
        js.set_key(i)
        chords.append( js.get_chord_as_lilypond(jazz_number_list))
    return chords

def get_m_chords():
    return get_chords([1, 3, 5])

def get_m6_chords():
    return get_chords([1, 3, 5, 6])

def get_m7_chords():
    return get_chords([1, 3, 5, 7])

def get_m9_chords():
    return get_chords([1, 3, 5, 7, 9])


class TestJazz(unittest.TestCase):
    def setUp(self):
        self.c = JazzScale(0)
        self.b = JazzScale(11)
        self.dflat = self.csharp = JazzScale(1)

    def test_major_pitches(self):
        self.c.set_major_mode()
        assert self.c.scale == [0, 2, 4, 5, 7, 9, 11, 12, 14, 16, 17, 19, 21, 23, 24]

    def test_minor_pitches(self):
        self.c.set_minor_mode()
        assert self.c.scale == [0, 2, 3, 5, 7, 8, 10, 12, 14, 15, 17, 19, 20, 22, 24]

    def test_c_major_triad(self):
        chord = self.c.get_chord_as_numbered([1, 3, 5])
        assert chord == [0, 4, 7]

    def test_c_major_triad_lilypond(self):
        chord = self.c.get_chord_as_lilypond([1, 3, 5])
        assert chord == "<c' e' g'>"

    def test_flat_spelling(self):
        self.dflat.set_spelling_flats()

        pitches_expected = [NamedPitch("df'"), NamedPitch("ef'"), NamedPitch("f'"), 
            NamedPitch("gf'"), NamedPitch("af'"), NamedPitch("bf'"), 
            NamedPitch("c''"), NamedPitch("df''"), NamedPitch("ef''"), 
            NamedPitch("f''"), NamedPitch("gf''"), NamedPitch("af''"), 
            NamedPitch("bf''"), NamedPitch("c'''"), NamedPitch("df'''")]
        assert self.dflat.pitches == pitches_expected

    def test_sharp_spelling(self):
        self.csharp.set_spelling_sharps()

        pitches_expected = [NamedPitch("cs'"), NamedPitch("ds'"), NamedPitch("f'"), 
            NamedPitch("fs'"), NamedPitch("gs'"), NamedPitch("as'"),
            NamedPitch("c''"), NamedPitch("cs''"), NamedPitch("ds''"), 
            NamedPitch("f''"), NamedPitch("fs''"), NamedPitch("gs''"), 
            NamedPitch("as''"), NamedPitch("c'''"), NamedPitch("cs'''")]
        assert self.csharp.pitches == pitches_expected

if __name__ == '__main__':
    unittest.main()



