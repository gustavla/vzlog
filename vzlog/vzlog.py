from __future__ import division, print_function, absolute_import

import os
import sys
from copy import copy

__all__ = ['VzLog', 'default']

_HEADER = """
<!DOCTYPE html>
<html>
<head>
    <title>{{title}}</title>
    <style>
    html {
        background: white;
        font-family: Verdana;
        font-size: 12px
    }

    div.section {
        border-bottom: 2px solid gray;
    }

    p.title {
        text-weight: bold;
    }
    </style>
</head>
<body>
"""

_FOOTER = """
</body>
</html>
"""


class VzLog:
    """
    Logging class that manages a HTML log file. Mainly used for visually rich
    logging with plenty of images.

    Parameters
    ----------
    name : str
        Name of the directory.
    """
    def __init__(self, name):
        self.name = name
        self._file_rights = os.environ.get('VZ_FILE_RIGHTS')
        self._filename_stack = set()
        if self._file_rights is not None:
            self._file_rights = int(self._file_rights, 8)
        self._open = False

        self.clear()

        self._counter = 0

        # Make flush unnecessary to call manually
        import atexit
        atexit.register(self.flush)

    def register_filename(self, fn):
        self._filename_stack.add(fn)

    def set_rights(self, fn):
        if self._file_rights is not None:
            return os.chmod(fn, self._file_rights)

    def update_rights(self):
        for fn in copy(self._filename_stack):
            if os.path.exists(fn):
                self.set_rights(fn)
                self._filename_stack.remove(fn)

    def clear(self):
        """
        Prepares a folder for logging. This also clears any previous output and
        can thus be used for instance during an interactive session when
        wanting a clean slate.
        """
        # Construct path.
        root = self._get_root()
        dot_vz_fn = os.path.join(root, '.vz')

        # First, remove previous folder. Only do this if it looks like
        # it was previously created with vz. Otherwise, throw an error.
        if os.path.isdir(root):
            # Check if it has a '.vz' file
            if os.path.exists(dot_vz_fn):
                # Delete the whole directory
                import shutil
                shutil.rmtree(root)
            else:
                raise Exception("Folder does not seem to be a vz folder.")

        self._open = True

        # Create folder
        os.mkdir(root)

        self._output_html(_HEADER.replace('{{title}}', self.name))

        with open(dot_vz_fn, 'w') as f:
            print('ok', file=f)

    def _get_root(self):
        vz_dir = os.environ.get('VZ_DIR', '')
        vz_dir = os.path.expandvars(os.path.expanduser(vz_dir))
        return os.path.join(vz_dir, self.name)

    def _output_surrounding_html(self, prefix, suffix, *args):
        self._output_html(*((prefix,) + args + (suffix,)))

    def _output_html(self, *args):
        with open(os.path.join(self._get_root(), 'index.html'), 'a') as f:
            print(*args, file=f)

    def flush(self):
        self._output_html(_FOOTER)
        self.register_filename(os.path.join(self._get_root(), 'index.html'))
        self.update_rights()
        self.set_rights(self._get_root())

        if self._filename_stack:
            print("VZLOG WARNING: Could not flush these files:",
                  self._filename_stack, file=sys.stderr)

        self._open = False

    def impath(self, ext='png'):
        """
        This generates a path to an image file, outputs the image and
        returns the path.

        Examples
        --------
        >>> import amitgroup as ag
        >>> from vzlog import default as vz

        We can output an image by saving the file:

        >>> ag.image.save(vz.impath(ext='png'), im)

        Or with matplotlib using a vector format:

        >>> plt.figure()
        >>> plt.plot([1,3,2,3,1])
        >>> plt.savefig(vz.impath(ext='svg'))
        """
        fn = 'plot-{:04}.'.format(self._counter) + ext
        self._counter += 1

        self._output_surrounding_html(
            '<div>', '</div>', '<img src="{}" />'.format(fn))

        self.register_filename(os.path.join(self._get_root(), fn))
        # The file won't exist yet, but this can still update older files
        self.update_rights()
        fn = os.path.join(self._get_root(), fn)
        return fn

    def log(self, *args):
        """
        Log text with mono-spaced font.

        Parameters
        ----------
        Similar to 
        """
        self._output_surrounding_html('<pre>', '</pre>', *args)

    def title(self, *args):
        self._output_surrounding_html('<h1>', '</h1>', *args)

    def section(self, *args):
        self._output_surrounding_html('<h2>', '</h2>', *args)

    def text(self, *args):
        self._output_surrounding_html('<p>', '</p>', *args)

    def output(self, obj):
        if hasattr(obj, '_vzlog_output_'):
            obj._vzlog_output_(self)
        else:
            self.log(obj)
