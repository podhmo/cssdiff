cssdiff
========================================

semantic css diff

install
----------------------------------------

::

  pip install cssdiff

see css difference
----------------------------------------

`cssdiff` command is installed. using this command, be enable to see css difference.

adding detection
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
we have two files.

- x-only.css
- all.css

x-only.css include only about x element, all.css has about x and y.

.. code-block:: bash

  $ cat data/x-only.css
  x {
    color: black;
    display: none;
  }
  $ cat data/all.css
  x {
    color: black;
    display: none;
  }

  y {
    color: white;
    display: none;
  }

so, cssdiff answered, addition about y.

.. code-block:: bash

  $ cssdiff data/x-only.css data/all.css
  y {
  +  color: white;
  +  display: none;
  }

changing detection
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If x's color is changed, cssdiff tell me that x's color is changed.

.. code-block:: bash

  $ cat data/x-color-changed.css
  x {
    color: white;
    display: none;
  }

  y {
    color: white;
    display: none;
  }

  $ cssdiff data/all.css data/x-color-changed.css
  x {
  -  color: black;
  +  color: white;
  }

semantic diff
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

below files are same meaning of all.css. so, no-difference.

.. code-block:: bash

  $ cat data/all-separated.css
  x {
    color: black;
  }

  y {
    color: white;
  }

  x {
    display: none;
  }

  y {
    display: none;
  }
  $ cssdiff data/all.css data/all-separated.css

  $ cat data/all-squashed.css
  x,
  y{
    display: none;
  }

  x {
    color: black;
  }

  y {
    color: white;
  }
  $ cssdiff data/all.css data/all-separated.css

  $ cat data/all-conflicted.css
  x {
    color: white;
    display: none;
  }

  y {
    color: white;
    display: none;
  }

  x {
    color: black;
    display: none;
  }

  y {
    color: white;
    display: none;
  }
  $ cssdiff data/all.css data/all-conflicted.css


appendix
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

extra.css has extra information. so, cssdiff notify it.

.. code-block:: bash

  $ cat data/extra.css
  x,
  y,
  a > b,
  a + b{
    display: none;
  }

  x {
    color: black;
  }

  y {
    color: white;
  }
  $ cssdiff data/all.css data/extra.css
  a + b {
  +  display: none;
  }

  a > b {
  +  display: none;
  }

