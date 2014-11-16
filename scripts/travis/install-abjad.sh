#
# We install Abjad from repository as opposed to pip to ensure we have the latest developer
# code. This usually doesn't break anything!
#

git checkout https://github.com/Abjad/abjad.git
cd abjad
python setup.py build
python setup.py install
cd ..
