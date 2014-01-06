import re
from abjad import *


def realize_pattern(pattern, scale):
    regex = re.compile('(-+|\++)?([\d+])(f|s)?')
    pitches = []
    for x in pattern:
        alteration = None
        octave_transposition = 0
        if isinstance(x, int):
            scale_degree = abs(x)
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
        scale_degree = tonalanalysistools.ScaleDegree(alteration, scale_degree)
        pitch_class = scale.scale_degree_to_named_pitch_class(scale_degree)
        pitch = pitchtools.NamedPitch(pitch_class, 4 + octave_transposition)
        pitches.append(pitch)
    return pitchtools.PitchSegment(pitches)

pattern = [1, "-7", 2, 1, 3, "2s", 4, 3]
c = tonalanalysistools.Scale('c', 'major')
realized_pattern = realize_pattern(pattern, c)
print realized_pattern
f = tonalanalysistools.Scale('f', 'major')
realized_pattern = realize_pattern(pattern, f)
print realized_pattern

