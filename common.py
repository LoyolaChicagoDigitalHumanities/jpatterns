#
# common.py: common routines to support each Jazz pattern
#

import os, os.path
from abjad import *

def keys_in_order():
    for i in range(0, 12):
        yield i

def keys_in_fifths():
    for i in range(0, 12):
        yield 5*i % 12

unix_path = './build'.split('/')
write_dir = os.path.join(*unix_path)

class MissingOutputDir(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return "Please mkdir %s before running." % self.value

class UnsupportedExtension(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return "Extension %s specified but only .pdf and .ly are supported." % self.value

def save(abjad_object, filename):
    os.path.join(write_dir, filename)
    if os.path.exists(write_dir):
        write_path = os.path.join(write_dir, filename)
        (base, ext) = os.path.splitext(write_path)
        if ext == '.pdf':
            persist(abjad_object).as_pdf(write_path)
        elif ext == '.png':
            persist(abjad_object).as_png(write_path)
        elif ext == '.ly':
            persist(abjad_object).as_ly(write_path)
        elif ext == '.midi':
            persist(abjad_object).as_midi(write_path)
        else:
            raise UnsupportedExtension(ext)
    else:
        raise MissingOutputDir(write_dir)


def get_lilypond_file(score, title, composer):
    r'''Makes LilyPond file.
    '''

    lily = lilypondfiletools.make_basic_lilypond_file(score)
    lily_title = markuptools.Markup(r'\bold \sans "%s"' % title)
    lily_composer = schemetools.Scheme(composer)
    lily.global_staff_size = 16
    lily.header_block.title = lily_title
    lily.header_block.composer = lily_composer
    lily.layout_block.ragged_right = False
    lily.layout_block.indent = 0
    lily.paper_block.markup_system_spacing__basic_distance = 8
    lily.paper_block.paper_width = 180
    return lily

def main(score, title, composer, filename):
    lilypond_file = get_lilypond_file(score, title, composer)
    save(lilypond_file, filename)
