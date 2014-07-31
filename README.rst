vzlog
=====

Tool for logging rich content, particularly plots and images. It has two main
advantages over interactive logging:

* You can run experiments with loads of output, without having to be halted by
  an interactive plot. If you solve this by dumping plots to individual images,
  you might want to test vzlog instead, since it can seamlessly integrate text
  and images.
* If you often work remotely from a computer with a public HTML directory (such
  as a University account), you can plot directly to that directory. VzLog can
  in that case make sure the files have public viewing permissions.

Installation
------------
::

    python setup.py install

Features
--------
* Logs rich content data, such as plots and images, to an HTML file.
* Works with any plotting library that can save to file (e.g. matplotlib).
* Ability to explicitly set file permissions. This is useful if you are using
  this on a server with a restrictive umask, but you are plotting to a public
  HTML folder. No more clunky X redirection to do remote plotting.

Example
-------
Apart from commands that print text, the key command here is ``vz.impath``,
which returns an image path. The path is at the same added to the log output::

    from vzlog.default import vz
    import matplotlib as mpl
    mpl.rc('font', size=8)
    mpl.use('Agg')
    import matplotlib.pylab as plt

    vz.title('Plots')
    vz.section('Silly plot')

    x = [1,2,3,1,2,3]
    vz.log('x = ', x)

    plt.figure(figsize=(4, 4))
    plt.plot(x)
    plt.savefig(vz.impath('svg'))
