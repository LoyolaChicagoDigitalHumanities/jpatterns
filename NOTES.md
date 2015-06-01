Chromebook
-----------

Ubuntu on the Chromebook seems not to set the locale properly.

Make sure to edit /etc/default/locale.

Here in the USA, I just added these lines:

LANG=en_US.UTF-8
LC_MESSAGES=POSIX

