# -*- coding: utf-8 -*-
"""Recipe jenkinsdeploy"""
import os
import zc.buildout

class Recipe(object):
    """zc.buildout recipe"""
    
    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options

        self.location = self.options['location'] = os.path.join(
             self.buildout['buildout']['parts-directory'], self.name
        )    

        self.config_file = os.path.join(self.location, '_config')
        self.fab_file = self.location + '/fabfile.py'
        self.job_file = self.location + '/config.xml'
        self.bin_script = os.path.join(self.buildout['buildout']['bin-directory'], self.name)

        options.setdefault('host.user', os.environ['USER'])
        options.setdefault('host.port', '22')
        options.setdefault('overwrite', 'false')

    def install(self):
        """Installer"""
        part_directory = self.location
        if not os.path.exists(part_directory):
            os.mkdir(part_directory)

        self.write_config()
        self.write_fabfile()
        self.write_jobfile()
        self.write_script()
        return (part_directory, self.config_file, 
                self.fab_file, self.job_file, self.bin_script)

    def update(self):
        """Updater"""
        pass

    def write_config(self):
        config = {}
        with open(self.config_file,"wb") as _config:
            config['jobname'] = self.options['jobname']
            config['host'] = "%(user)s@%(address)s:%(port)s" % { 
                            'user':self.options['host.user'],
                            'address':self.options['host.address'], 
                            'port':self.options['host.port'], } 
            config['path'] = self.options['host.jobs_path']
            config['overwrite'] = self.options['overwrite']

            _config.write(
                '|'.join(['%s=%s' % (k,v) for k,v in config.items()]))

    def write_fabfile(self):
        template = os.path.join(os.path.split(__file__)[0],
                                'templates/fabfile.py.in')
        with open(template,'rb') as _f_fab_template:
            fab_template = _f_fab_template.read()
        
        with open(self.fab_file, 'wb') as _f_fab:
            _f_fab.write(fab_template.replace("$CONFIG_FILE", self.config_file))

    def write_jobfile(self):
        template = os.path.join(os.path.split(__file__)[0],
                                'templates/config.xml.in')
        with open(template,'rb') as _f_job_template:
            job_template = _f_job_template.read()
        
        with open(self.job_file, 'wb') as _f_job:
            _f_job.write(job_template)


    #FIX: I now it's better to use entry_point 'console_script' but the fabfile
    # is dinamically generated in the part directory
    def write_script(self):
        with open(self.bin_script, 'wb') as _f_script:
            _f_script.write('python %s' % self.fab_file)
        os.chmod(self.bin_script, 0755)
