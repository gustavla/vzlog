from __future__ import division, print_function, absolute_import

import os
import sys
from copy import copy

__all__ = ['VzLog']

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

    div.wrapper {
        display: inline-block; /* important for scaling */
    }

    div.section {
        border-bottom: 2px solid gray;
    }

    p.title {
        text-weight: bold;
    }

    img {
        image-rendering: optimizeSpeed;
        image-rendering: -moz-crisp-edges;
        image-rendering: -webkit-optimize-contrast;
        image-rendering: optimize-contrast;
        -ms-interpolation-mode: nearest-neighbor;
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
    Logging class that manages an HTML log file. Mainly used for visually rich
    logging with plenty of images.

    :param path: Path the directory where the files will be saved.
    :param name: Specify name of the output document. This will be used to set
                 the document title. Inferred from `path` if set to `None`.

    """
    def __init__(self, path, name=None, file_rights=None):
        self._root = os.path.abspath(path)
        if name is None:
            self._name = os.path.basename(path)
        else:
            self._name = name
        self._file_rights = file_rights
        if self._file_rights is not None:
            self._file_rights = int(self._file_rights, 8)
        self._filename_stack = set()
        self._open = False

        self.clear()

        self._counter = 0

        # Make flush unnecessary to call manually
        import atexit
        atexit.register(self.flush)

    def _register_filename(self, fn):
        self._filename_stack.add(fn)

    def _set_rights(self, fn):
        if self._file_rights is not None:
            return os.chmod(fn, self._file_rights)

    def _update_rights(self):
        for fn in copy(self._filename_stack):
            if os.path.exists(fn):
                self._set_rights(fn)
                self._filename_stack.remove(fn)

    def clear(self):
        """
        Prepares a folder for logging. This also clears any previous output and
        can thus be used during an interactive session when
        wanting a clean slate.
        """
        # Construct path.
        dot_vz_fn = os.path.join(self._root, '.vz')

        # First, remove previous folder. Only do this if it looks like
        # it was previously created with vz. Otherwise, throw an error.
        if os.path.isdir(self._root):
            # Check if it has a '.vz' file
            if os.path.exists(dot_vz_fn):
                # Delete the whole directory
                import shutil
                shutil.rmtree(self._root)
            else:
                raise Exception("Folder does not seem to be a vz folder.")

        self._open = True

        # Create folder
        os.mkdir(self._root)

        # Reset counter
        self._counter = 0

        # Output header
        self._output_html(_HEADER.replace('{{title}}', self._name))

        with open(dot_vz_fn, 'w') as f:
            print('ok', file=f)

    def _output_surrounding_html(self, prefix, suffix, *args, **kwargs):
        with open(os.path.join(self._root, 'index.html'), 'a') as f:
            kwargs['file'] = f
            print(prefix, file=f)
            print(*args, **kwargs)
            print(suffix, file=f)

    def _output_html(self, *args, **kwargs):
        with open(os.path.join(self._root, 'index.html'), 'a') as f:
            kwargs['file'] = f
            print(*args, **kwargs)

    def flush(self):
        """
        Flushes the output. This adds a footer and updates the file rights.
        Normally, you do not need to call this yourself. However, it can be
        useful during an interactive session when the file rights have not be
        processed yet.
        """
        self._output_html(_FOOTER)
        self._register_filename(os.path.join(self._root, 'index.html'))
        self._update_rights()
        self._set_rights(self._root)

        if self._filename_stack:
            print("VZLOG WARNING: Could not flush these files:",
                  self._filename_stack, file=sys.stderr)

        self._open = False

    def output_with_tag(self, tag, *args, **kwargs):
        """
        Outputs strings surrounded by a specific HTML tag.
        """
        opening = '<' + tag + '>'
        closing = '</' + tag + '>'
        self._output_surrounding_html(opening, closing, *args, **kwargs)

    def output(self, obj):
        """
        Outputs an object. This will look for ``obj._vzlog_output_`` and pass
        itself along as the only argument. If the object does not have such a
        function, it will fall back to `VzLog.log`.
        """

        if hasattr(obj, '_vzlog_output_'):
            obj._vzlog_output_(self)
        else:
            self.log(obj)


    def log(self, *args, **kwargs):
        """
        Logs text with mono-spaced font (<pre>).

        >>> vz.log('Logging a value', 100)
        """
        self.output_with_tag('pre', *args, **kwargs)

    def title(self, *args, **kwargs):
        """
        Adds a title (<h1>).
        """
        self.output_with_tag('h1', *args, **kwargs)

    def section(self, *args, **kwargs):
        """
        Adds a section title (<h2>).
        """
        self.output_with_tag('h2', *args, **kwargs)

    def text(self, *args, **kwargs):
        """
        Adds a paragraph of text (<p>).
        """
        self.output_with_tag('p', *args)

    def impath(self, ext='png', scale=1.0):
        """
        This generates a path to an image file, outputs the image and
        returns the path. Specify the extension with `ext`.

        >>> from vzlog.default import vz

        We can output an image by saving the file:

        >>> ag.image.save(vz.impath(ext='png'), im)

        Or with matplotlib using a vector format:

        >>> plt.figure()
        >>> plt.plot([1,3,2,3,1])
        >>> plt.savefig(vz.impath(ext='svg'))
        """
        fn = 'plot-{:04}.'.format(self._counter) + ext
        self._counter += 1

        if scale != 1.0:
            scale_str = ('width="{:.2f}%" height="{:.2f}%" '
                         .format(scale * 100.0, scale * 100.0))

        self._output_surrounding_html(
            '<div><div class="wrapper">', '</div></div>', '<img src="{}" {}/>'.format(fn, scale_str))

        path = os.path.join(self._root, fn)
        self._register_filename(path)
        # The file won't exist yet, but this can still update older files
        self._update_rights()
        return path

    def savefig(self, fig=None):
        """
        Saves a matplotlib figure to the log file. This can also be done using
        `impath`, but this will save both a SVG and a PDF version. The SVG will
        be viewed directly in the browser next to a link to the PDF (so it can
        be downloaded).
        """
        if fig is None:
            import pylab as plt
            fig = plt
        base_fn = 'plot-{:04}'.format(self._counter)
        self._counter += 1

        self._output_surrounding_html(
            '<div>', '</div>', """
            <img src="{0}.svg" />
            <div><a href="{0}.pdf">pdf</a></div>""".format(base_fn))

        for ext in 'svg', 'pdf':
            path = os.path.join(self._root, '{}.{}'.format(base_fn, ext))
            self._register_filename(path)
            fig.savefig(path)
        self._update_rights()

    def __repr__(self):
        return 'VzLog(path={!r}, counter={}, unflushed={})'.format(self._root, self._counter, len(self._filename_stack))
