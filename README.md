# README #

This is the patterns for jazz project, a collection of printable and playable patterns for learning the basics of jazz, composition in general, and ear training. This project is made possible by two awesome projects:

* Lilypond, http://lilypond.org
* Abjad, http://abjad.mbrsi.org/

You must install Lilypond using the installers provided on the abovementioned Lilypond web site. I recommend that you install all of your Python-related stuff in a virtualenv, especially when working on Mac or a Linux distribution (especially those so-called LTS distributions, which feature an ancient Python experience in general).

# Installation

For now, I only provide installation instructions for OS X. The Linux setup is similar and is one I have tested but don't have time to document right now. Will hopefully get around to it soon. 

1. If you aren't running MacPorts (http://macports.org) or HomeBrew (http://brew.sh), do it now. I am using MacPorts, so I will be using the port command. HomeBrew uses brew. You'll likely be able to adapt what you see here:

1. Set up the desired version of Python 2.7 and/or 3.4. Abjad supports Python 2.7 but has recently been updated to support 3.4 (only when you have the latest version of Abjad from repository):

   $ port install python27 py27-virtualenv

