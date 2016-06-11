==============================================================
Control the dependency requirements being passed to `setup.py`
==============================================================


How it works
------------

1. Read and load in the `default` file first

2. Read and load whatever file name matches the `ENV` environment variable


Points of interest
--------------------

If environment is `test` then, load the file into the `test_requirements`
after the `default`
