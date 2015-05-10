====================
Easiest installation
====================

These solution are easy all will be able to handle a personnal website traffic.
For more robust and secure solutions, see :doc:`Apache <./apache_install>`
and :doc:`Nginx <./nginx_install>` setups.

10 seconds setup (if you know Python already)
===============================================

Just type::

    pip install zerobin
    zerobin --host 0.0.0.0 --port 80 --compressed-static # as admin

30 seconds setup (for anybody)
===============================

- Make sure you have Python 2.7 or 3.4+ (`python --version`)
- Download the last `zip of the source code <https://github.com/sametmax/0bin/zipball/master>`_
- Extract all of it where you wish the site to be stored.
- Go to the extracted files.
- Run with the admin rights::

    python zerobin.py --host 0.0.0.0 --port 80 --compressed-static

On ubuntu, this is a one liner::

    wget stuff && unzip zerobin.zip && cd zerobin && sudo python zerobin.py --host 0.0.0.0 --port 80 --compressed-static

Check out for more :doc:`configuration options <./options>`.

Run 0bin in background
=======================

0bin doesn't come with something built in for this. You have several solutions.

*For a small website:*

Just make it a shell background process. E.G in GNU/Linux::

  nohup python zerobin.py --host 0.0.0.0 --port 80 --compressed-static &

Or run it in a screen.

*For a big Website:*

- setup 0bin with :doc:`Apache <./apache_install>`;
- setup 0bin with :doc:`supervisor <./using_supervisor>` (best way to do it).

.. Note::

    You can even use zerobin on your private local network from your laptop.

    Make sure you firewall won't block the port, and run::

        python zerobin.py --host 0.0.0.0 --port 8000

    0bin will now be accessible from http://your.local.ip.address:8000.

    This can be very cool way to share code in a companie or during a code sprint.
