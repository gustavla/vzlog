vzlog
=====

Tool for logging rich content to an HTML file. It has two main advantages over
interactive logging:

* You can run experiments with loads of output, without having to be halted by
  an interactive plot. If you solve this by dumping plots to individual images,
  you might want to try vzlog instead, since it can seamlessly integrate text
  and images.
* If you often work remotely from a computer with a public HTML directory (such
  as a University account), you can plot directly to that directory. VzLog can
  in that case make sure the files have public viewing permissions.

Installation
------------
::

    pip install vzlog

Documentation |doc|
-------------------

* http://vzlog.readthedocs.org/ 

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
which returns an image path. The path is at the same time added to the log
output:

.. code:: python

    from vzlog import VzLog

    vz = VzLog('mylog')
    vz.title('Plots')
    vz.section('Silly plot')

    x = [1, 2, 3, 1, 2, 3]
    vz.log('x =', x)

    # Plot directly to the vzlog file
    import vzlog.pyplot as plt

    plt.figure(figsize=(4, 4))
    plt.plot(x)
    plt.savefig(vz.impath('svg'))

.. |doc| image:: https://readthedocs.org/projects/vzlog/badge/?version=latest 
         :target: https://readthedocs.org/projects/vzlog/?badge=latest 
         :alt: Documentation Status

