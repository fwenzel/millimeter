millimeter
==========

*millimeter* is a [Django][django]-based URL shortener. All other shorteners
I found were a huge pain, because they wanted to do everything, but did none
of it right. Instead, millimeter will not start off with 500 features, but
grow as I need them.

millimeter is supposed to be a private URL shortener. I might add an option to
allow the general public to make URLs at some point, but don't count on it.

Patches are welcome! Feel free to fork and contribute to this project on
[github][gh-mm].

[django]: http://www.djangoproject.com/
[gh-mm]: http://github.com/fwenzel/millimeter

Authors
-------
* Frederic Wenzel (fwenzel@mozilla.com)

Requirements
------------
You need Python 2.6. You probably want to run install this in a [virtualenv
environment][virtualenv].

To install the prerequisites for this tool, run:

    easy_install pip
    pip install -r requirements.txt

[virtualenv]: http://pypi.python.org/pypi/virtualenv

License
-------
This software is licensed under the [New BSD License][BSD]. For more
information, read the file ``LICENSE``.

[BSD]: http://creativecommons.org/licenses/BSD/

