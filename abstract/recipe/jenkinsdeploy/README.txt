Supported options
=================

The recipe supports the following options:

.. Note to recipe author!
   ----------------------
   For each option the recipe uses you should include a description
   about the purpose of the option, the format and semantics of the
   values it accepts, whether it is mandatory or optional and what the
   default value is if it is omitted.

option1
    Description for ``option1``...

option2
    Description for ``option2``...


Example usage
=============

.. Note to recipe author!
   ----------------------
   zc.buildout provides a nice testing environment which makes it
   relatively easy to write doctests that both demonstrate the use of
   the recipe and test it.
   You can find examples of recipe doctests from the PyPI, e.g.
   
     http://pypi.python.org/pypi/zc.recipe.egg

   The PyPI page for zc.buildout contains documentation about the test
   environment.

     http://pypi.python.org/pypi/zc.buildout#testing-support

   Below is a skeleton doctest that you can start with when building
   your own tests.

We'll start by creating a buildout that uses the recipe::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... parts = deploy
    ...
    ... [deploy]
    ... recipe = abstract.recipe.jenkinsdeploy
    ... jobname = %(jobname)s
    ... """ % { 'jobname' : 'MyJob'})

Running the buildout gives us::

	>>> buildout_output_lower = system(buildout).lower()
	>>> "error: missing option: deploy:host.address" in buildout_output_lower
	True

So we have to specify an address and also the jobs_path

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... parts = deploy
    ...
    ... [deploy]
    ... recipe = abstract.recipe.jenkinsdeploy
    ... jobname = %(jobname)s
    ... host.address = %(address)s
    ... host.jobs_path = %(path)s
    ... """ % { 'jobname' : 'MyJob', 'address': 'localhost', 'path':'/path/to/jobs'})

Running:

    >>> buildout_output_lower = system(buildout).lower()
	>>> "installing deploy"  in buildout_output_lower and not "while:" in buildout_output_lower
	True

Ok, it seems working
Let's check if the config was created

    >>> ls(sample_buildout+'/parts/deploy')
    -  _config
    -  config.xml
    -  fabfile.py
    >>> cat(sample_buildout+'/parts/deploy/_config')
    path=/path/to/jobs|host=...@localhost:22|overwrite=false|jobname=MyJob

So we have defaults for user and port. Ok let's specify user and port::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... parts = deploy
    ...
    ... [deploy]
    ... recipe = abstract.recipe.jenkinsdeploy
    ... jobname = %(jobname)s
    ... host.address = %(address)s
    ... host.jobs_path = %(path)s
    ... host.user = %(user)s
    ... host.port = %(port)s
    ... """ % { 'jobname' : 'MyJob', 'address': 'localhost', 'path':'/path/to/jobs', 'user': 'zope', 'port': '8022'})


And run buildout:

    >>> buildout_output_lower = system(buildout).lower()
    >>> cat(sample_buildout+'/parts/deploy/_config')
    path=/path/to/jobs|host=zope@localhost:8022|overwrite=false|jobname=MyJob

    

