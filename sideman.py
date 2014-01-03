#
# sideman.py (a.k.a. sideperson.py) - a collection of utilties that act as a "side man"
# (in the Jazz sense) to the Abjad toolkit. These tools are strictly aimed at 
# faciliting work with jazz and jazz patterns.
#

from abjad import *

import unittest
import os, os.path, re

#
# These constants are the names associated with accidentals in Abjad.
#

flats = 'flat'
sharps = 'sharp'
naturals = 'naturals'

#
# Standard durations needed by most patterns. 
#

eighth = Duration(1, 8)
quarter = Duration(1, 4)
half = Duration(1, 2)
whole = Duration(1, 1)


#
# Iterators for walking in key order (e.g. 0, 1, 2, ...) or 
# by the circle of fifths (e.g. 0, 5, 10, 3, 8, 1, ...)
#

def keys_in_order():
    for i in range(0, 12):
        yield i

def keys_in_fifths():
    for i in range(0, 12):
        yield 5*i % 12

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

    # the get_chord*() methods ensure uniqueness of the numbers provided

    def get_unique_jazz_numbers(self, jazz_number_list):
        jazz_number_list_unique = list(set(jazz_number_list))
        jazz_number_list_unique.sort()
        return jazz_number_list_unique

    def get_chord_as_numbered(self, jazz_number_list):
        return [ self.get_numbered_pitch(i) for i in self.get_unique_jazz_numbers(jazz_number_list)]

    def get_chord_as_named(self, jazz_number_list):
        return [ self.get_pitch(i) for i in self.get_unique_jazz_numbers(jazz_number_list)]

    def get_chord_as_lilypond(self, jazz_number_list):
        return "<%s>" % " ".join([ str(self.get_pitch(i)) for i in self.get_unique_jazz_numbers(jazz_number_list)])

    # the get_pitches*() methods do not require uniqueness

    def get_numbered_pitch(self, n):
        assert n > 0 and n < 16
        return self.scale[n-1]

    def get_pitches(self, jazz_number_list):
        return [ self.get_numbered_pitch(i) for i in jazz_number_list]

    def get_pitch(self, jazz_number):
        assert jazz_number > 0 and jazz_number < 16
        return self.pitches[jazz_number-1]

    def get_pitches_as_named(self, jazz_number_list):
        return [ self.get_pitch(i) for i in jazz_number_list ]

    # TODO: "deprecated" name used in examples...will clean up later
    get_named_pitches = get_pitches_as_named

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

    def test_get_chord_group(self):

        c1 = self.c.get_chord_as_numbered([1, 3, 5, 7, 3, 1])   # should only include 1,3,5,7
        assert c1 == [0, 4, 7, 11]

        c2 = self.c.get_chord_as_named([1, 3, 5, 7, 7, 3, 1])
        print(c2)
        assert c2 == [ NamedPitch("c'"), NamedPitch("e'"), NamedPitch("g'"), NamedPitch("b'")]

        c3 = self.c.get_chord_as_lilypond([1, 3, 5, 7, 7, 3, 1])
        assert c3 == "<c' e' g' b'>"

    def test_get_pitches_group(self):

        simple_jazz_pattern = [1, 3, 5, 7, 7, 5, 3, 1, 1]       # used by jazz1.py :-)
        c_pitches = [0, 4, 7, 11, 11, 7, 4, 0, 0]

        c1 = self.c.get_pitches(simple_jazz_pattern)   # should only include 1,3,5,7
        assert c1 == c_pitches

        c2 = self.c.get_pitches_as_named(simple_jazz_pattern)
        assert c2 == [NamedPitch("c'"), NamedPitch("e'"), NamedPitch("g'"), NamedPitch("b'"), 
                      NamedPitch("b'"), NamedPitch("g'"), NamedPitch("e'"), NamedPitch("c'"), NamedPitch("c'")]

        # This is essentially a spelling test to ensure the pitches are spelled the way they should for this (flat) scale
        dflat1 = self.dflat.get_pitches_as_named(simple_jazz_pattern)
        assert dflat1 == [NamedPitch("df'"), NamedPitch("f'"), NamedPitch("af'"), NamedPitch("c''"),
                        NamedPitch("c''"), NamedPitch("af'"), NamedPitch("f'"), NamedPitch("df'"), NamedPitch("df'")]

    def get_chord_as_lilypond(self, pitch_list):
        return "<%s>" % " ".join([ str(self.get_pitch(i)) for i in self.get_chord_as_numbered(jazz_number_list)])

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

KEYS = ['c', 'df', 'd', 'ef', 'e', 'f', 'gf', 'g', 'af', 'a', 'bf', 'b']

def keys_in_order():
    for i in range(0, 12):
        yield i

def keys_in_fifths():
    for i in range(0, 12):
        yield 5*i % 12

def keynames_in_order():
    assert len(KEYS) == 12
    for key in KEYS:
        yield key

def keynames_in_fifths():
    assert len(KEYS) == 12
    for i in range(0, len(KEYS)):
        yield KEYS[5*i % 12]

def get_scale(key, mode):
    return tonalanalysistools.Scale(key, mode)


#
# Thanks to Josiah for helping write this
# I made a few modifications to support 1...15
#

def get_pattern_pitches(pattern, scale):
    regex = re.compile('(-+|\++)?([\d+])(f|s)?')
    pitches = []
    for x in pattern:
        alteration = None
        octave_transposition = 0
        if isinstance(x, int):
            scale_degree = abs(x)
            assert 1 <= scale_degree and scale_degree <= 15
            if x < 0:
                octave_transposition -= 1

        elif isinstance(x, str):
            octaves, scale_degree, alteration = regex.match(x).groups()
            if isinstance(octaves, str):
                if octaves.startswith('-'):
                    octave_transposition = -1 * len(octaves)
                else:
                    octave_transposition = len(octaves)
            scale_degree = int(scale_degree)
            if alteration == 's':
                alteration = 'sharp'
            elif alteration == 'f':
                alteration = 'flat'

        if scale_degree >= 8:
            scale_degree = scale_degree - 8 + 1
            octave_transposition += 1

        print((scale_degree, octave_transposition, alteration))
        scale_degree = tonalanalysistools.ScaleDegree(alteration, scale_degree)
        pitch_class = scale.scale_degree_to_named_pitch_class(scale_degree)
        pitch = pitchtools.NamedPitch(pitch_class, 4 + octave_transposition)
        pitches.append(pitch)
    return pitches

def get_chord_pitches(pattern, scale):
    pitch_list = list(set(pattern))
    pitch_list.sort()
    return get_pattern_pitches(pattern, scale)

def get_chord_lilypond(pattern, scale):
    pitch_list = get_chord_pitches(pattern, scale)
    return '<' + ' '.join([ str(pitch) for pitch in pitch_list]) + '>'

if __name__ == '__main__':
    unittest.main()



