
Tutorial
========

The main class of this packaage is :class:`vzlog.vzlog.VzLog`, which manages an HTML
output.

Using the default ``VzLog`` object
----------------------------------

Instead of manually creating a VzLog instance, it is more common to
implement one that sets its path automatically:

>>> from vzlog.default import vz

This will draw information from the following environment variables:

``VZ_DIR``
    Directory of all your VzLog outputs.

``VZ_NAME``
    Directory name of your output.

``VZ_FILE_RIGHTS``
    File rights of all your images.

The path of a default VzLog object is constructed by joining ``VZ_DIR`` and
``VZ_NAME``. This means that it is easy to keep a folder with many
different plotting documents. Here is an example where a new directory will be
used::

    $ VZ_NAME=simple python examples/simple_test.py

You can also set these up more permanently by adding them to your ``~/.bashrc``::

    export VZ_DIR=~/html
    export VZ_NAME=plot
    export VZ_FILE_RIGHTS=0775

In this example, your document file will be placed in
``~/html/plot/index.html`` and the file rights 0775 mean that user/group can
read, write and execute and the rest can read and execute.
