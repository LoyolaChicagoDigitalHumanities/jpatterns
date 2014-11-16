# Build Status #

[![Build Status](https://travis-ci.org/gkthiruvathukal/jpatterns.svg?branch=master)](https://travis-ci.org/gkthiruvathukal/jpatterns)

# README #

This is the patterns for jazz project, a collection of printable and playable patterns for learning the basics of jazz, composition in general, and ear training. This project is made possible by two awesome projects:

* Lilypond, http://lilypond.org
* Abjad, http://abjad.mbrsi.org/

You must install Lilypond using the installers provided on the abovementioned Lilypond web site. I recommend that you install all of your Python-related stuff in a virtualenv, especially when working on Mac or a Linux distribution (especially those so-called LTS distributions, which feature an ancient Python experience in general).

# Installation

For now, I only provide installation instructions for OS X. The Linux setup is similar and is one I have tested but don't have time to document right now. Will hopefully get around to it soon. 

If you aren't running MacPorts (http://macports.org) or HomeBrew (http://brew.sh), do it now. I am using MacPorts, so I will be using the port command. HomeBrew uses brew. You'll likely be able to adapt what you see here:

Set up the desired version of Python 2.7 and/or 3.4. Abjad supports Python 2.7 but has recently been updated to support 3.4 (only when you have the latest version of Abjad from repository):

~~~
$ port install python27 py27-virtualenvv
~~~

Create a virtual environment

~~~
$ virtualenv-2.7 ~/.env/abjad
~~~

As a matter of convention, I create all of my virtualenv's in a subdirectory of my home folder, `~/.env`. For my Abjad work, I have `~/.env/abjad`.

Source in the environment

~~~
$ . ~/.env/abjad/bin/activate
~~~

This will change your prompt, indicating that you are now in the virtualenv.

~~~
(abjad)mininuevo:~ gkt$
~~~

Check out Abjad from its repository:


    (abjad)mininuevo:~ gkt$ git clone https://github.com/Abjad/abjad.git
    (abjad)mininuevo:~ gkt$ cd abjad
    (abjad)mininuevo:abjad gkt$ which python
    /Users/gkt/.env/abjad/bin/python
    (abjad)mininuevo:~ gkt$ python setup.py install

Note: If you do not see python coming out of `~/.env/abjad/bin`, your virtualenv was not created successfully. This means that everything we do subsequently would attempt to install to your global Python setup, which is probably not what you want. Go back to the earlier steps and make sure you created a virtualenv successfully.

Now we can sanity check that Abjad was installed correctly. You'll be able to tell if the last few lines of the install process look something like this:

~~~
Installed /Users/gkt/.env/abjad/lib/python2.7/site-packages/MarkupSafe-0.23-py2.7-macosx-10.9-x86_64.egg
Finished processing dependencies for Abjad==2.15
~~~

If all goes well, you should be able to fire up the Python interpreter and import abjad, which means things have gone well:

~~~
(abjad)mininuevo:abjad gkt$ python
Python 2.7.6 (default, Nov 18 2013, 15:12:51)
[GCC 4.2.1 Compatible Apple LLVM 5.0 (clang-500.2.79)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import abjad
>>> abjad.__version_info__
(2, 15)
~~~

You may see a different version than 2.15 here but that is the next release number (for 2014).

You should now be able to check out the jpatterns project and run the build script:

~~~
(abjad)mininuevo:~ gkt$ hg clone https://bitbucket.org/ctsdh/jpatterns
(abjad)mininuevo:~ gkt$ cd jpatterns
(abjad)mininuevo:~ gkt$ ./build.sh 
Generating pattern jazz001.py
Generating pattern jazz002.py
Generating pattern jazz003.py
Generating pattern jazz005.py
Generating pattern jazz008.py
Generating pattern jazz019.py
Generating pattern jazz059.py
Generating pattern jazz077.py
Creating II-V-I in key of C
Creating II-V-I in key of F
~~~

My build script *assumes* that you have a virtualenv for abjad present in `~/.env/abjad`.
