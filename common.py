#
# This is a collection of reusable functions/components for the patterns project.
#

# Configuration


flats = 'flats'
sharps = 'sharps'
naturals = 'naturals'
respellings = [naturals, flats, sharps, flats, sharps, flats, flats, sharps, flats, sharps, flats, sharps]

m_chords=["<c' e' g'>", "<df' f' af'>", "<d' fs' a'>", "<ef' g' bf'>", "<e' gs' b'>", "<f' a' c''>",
"<gf' bf' df''>", "<g' b' d''>", "<af' c'' ef''>", "<a' cs'' e''>", "<bf' d'' f''>", "<b' ds'' fs''>"]

m6_chords=["<c' e' g' a'>", "<df' f' af' bf'>", "<d' fs' a' b'>", "<ef' g' bf' af'>", "<e' gs' b' cs'>",
"<f' a' c'' d'>", "<gf' bf' df'' ef''>", "<g' b' d'' e''>", "<af' c'' ef'' f''>", "<a' cs'' e'' fs''>",
"<bf' d'' f'' g''>", "<b' ds'' fs'' g''>"]

# coming soon...
m7_chords=[]

# Support functions

# duration here is 1, 2, 4, etc. (for whole, half, quarter)
def get_lilypond_major_chords(duration):
	return ' '.join([ chord + str(duration) for chord in m_chords])

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

from abjad import *

eighth = Duration(1, 8)
quarter = Duration(1, 4)
half = Duration(1, 2)
whole = Duration(1, 1)

