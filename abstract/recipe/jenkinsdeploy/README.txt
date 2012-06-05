Introduction
============
This recipe simplify the job creation/deploy for Jenkins.
It creates a script in your ${buildout:bin-directory} you can use to
automatically deploy a job to your Jenkins instance through SSH.

Is uses Fabric under the hood.
It assumes you are using at least this buildout (https://github.com/abstract-open-solutions/Jenkins-Buildout/) 
to ensure you have installed all the required plugins

NOTE: IT WORKS ONLY FOR GIT HOSTED BUILDOUT

Supported options
=================

The recipe supports the following options:

jobname
    The name of the job will be created in Jenkins

jobdescription
    The job description

host.{address|port|jobs_path}
    Address, SSH Port and filesystem jobs folder path of the remote jenkins
    If you are using the above mentioed buildout, the jobs folder is in
${buildout:directory}/var/jenkins/jobs

user
    The user used for authenticating in via SSH

overwrite
    Default to False. Specify if an existing `jobname` job in Jenkins must be replaced.

repository
    The GIT repository Jenkins will use to fetch the buildout (GIT plugin in
Jenkins is required, of course)

timing
    The timing of the build, in the crontab format. Default: */45 * * * * (every 45 minutes)

email
    Email of the user for Jenkins email notification

Example usage
=============

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

Check if the fab script is created
    >>> bin_files = system('ls %s/bin' % sample_buildout).lower()
    >>> 'deploy' in bin_files
    True

Run it:
    >>> script_output = system('%s/bin/deploy' % sample_buildout).lower()
    >>> 'connection refused' in script_output
    True

Yes, connection fail of course. I have to test the script itself, learning about fabric testing/mocking
