IPython Notebook on Uppmax with SSH Port Forwarding
###################################################
:date: 2014-10-15
:tags: ssh, uppmax, ipython notebook
:slug: ipython-notebook-uppmax-ssh-forwarding
:author: Ino de Bruijn
:summary: Set up SSH Port Forwarding for IPython Notebook on UPPMAX.

`IPython Notebook <http://ipython.org/notebook.html>`_ is a great tool to
easily make plots of your data. It also makes it very simple to keep a close
connection between the commands you are running for an analysis and the
documentation of the steps you did. Instead of copying all the commands you ran
for analysis and explaining them, you can just run them straight from the
notebook and describe the steps there. Rerunning a step is a simple
``Shift+Enter``. This post assumes that you already know how to run ipython
notebook. If not head to their `website <http://ipython.org/notebook.html>`_.
Since I perform most of my analysis on an `UPPMAX cluster
<http://www.uppmax.uu.se/the-milou-cluster>`_ it is useful for me to be able to
use the notebook there. Couple of issues:

- HTTP connections are not allowed to the cluster.
- Running Firefox over ``ssh -X`` is very slow.
- Mounting with the drive remotely with `sshfs
  <http://fuse.sourceforge.net/sshfs.html>`_ works but will still transfer all
  the files.
  
The way you can get around these issues is by using SSH port forwarding. In
this case only the notebook itself is transferred over the internet and not the
data that you are analyzing. The first thing you should do before you start
forwarding your notebook is to protect it with a password. When you have your
notebook connected to a port, other people with access to the cluster can also
connect to that port and run anything through the browser on the ipython kernel
that's running on your username. They could basically submit jobs and what not
in your name so **BE CAREFUL**! Just follow `these steps
<http://ipython.org/ipython-doc/1/interactive/public_server.html>`_ to password
protect your notebook. I skipped generating the SSL certificate since we inted
to send everything over SSH anyway. I simply created the profile:

.. code-block:: bash

    [local] $ ssh username@milou2.uppmax.uu.se
    [milou2] $ ipython profile create nbserver

Generated a hashed password with ``ipython``:

.. code-block:: python

    import IPython.lib
    IPython.lib.passwd()

And changed the profile ``ipython_notebook_config.py`` like:

.. code-block:: python

    # Configuration file for ipython-nbconvert.
    c = get_config()

    # Notebook config
    #c.NotebookApp.certfile = u''
    c.NotebookApp.ip = '*'
    c.NotebookApp.open_browser = False
    # add the hashed password you got from ipython below
    c.NotebookApp.password = u'sha1:bcd259ccf...[your hashed password here]'
    # It is a good idea to put it on a known, fixed port
    c.NotebookApp.port = 9990

Run the notebook on milou with:

.. code-block:: bash

   [milou2] $ ipython notebook --profile=nbserver

Then run the following command  on your local computer that forwards a local
port (could be any port) to the remote port on milou2. I picked a common port
for HTTP (8080), since Firefox didn't want to connect to port 9990 for security
reasons.

.. code-block:: bash

   [local]  $ ssh -N -f -L localhost:8080:localhost:9990 inod@milou2.uppmax.uu.se
    
Now you should be able to open the notebook in your browser on
``http://localhost:8080``. Make sure it asks you for the password you provided.
Enjoy!
