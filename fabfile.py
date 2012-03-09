from fabric.api import local, env, run, put, abort
from fabric.operations import require
from fabric.contrib.console import confirm
import os

# avoid messages like "stdin is not a tty"
#print env
env.shell = '/bin/bash -c'
env.pwd = os.path.dirname(env.real_fabfile)

"""
Private functions
"""

def _put_dir(local_dir, remote_dir):
    """http://wiki.fabfile.org/Recipes#Improved_Directory_Upload

    Copy a local directory to a remote one, using tar and put. Silently
    overwrites remote directory if it exists, creates it if it does not
    exist."""
    local_tgz = "/tmp/fabtemp.tgz"
    remote_tgz = os.path.basename(local_dir) + ".tgz"
    local('tar -C "{0}" -czf "{1}" .'.format(local_dir, local_tgz))
    put(local_tgz, remote_tgz)
    local('rm -f "{0}"'.format(local_tgz))
    run('rm -Rf "{0}"; mkdir "{0}"; tar -C "{0}" -xzf "{1}" && rm -f "{1}"'\
    .format(remote_dir, remote_tgz))

"""
Environnments
"""

def staging():
    print("staging environnement is defined.")
    env.hosts=['localhost']
    env.apppath='/var/www/starred2bookmarks/'
    env.staticpath='/var/www/starred2bookmarks/static/'

def prod():
    print("prod environnement is defined.")
    env.hosts=['samk@ssh.alwaysdata.com']
    env.apppath='www/'
    env.staticpath='www/static/'

"""
Actions
"""

def _get_deps():
    if not os.path.exists('firefoxize_starred_items.py'):
        local("wget https://github.com/samyboy/firefoxize_starred_items/raw/master/firefoxize_starred_items.py")

def build():
    _get_deps()
    local("touch .build")

def deploy_app():
    if not os.path.exists(".build") and not confirm("Looks like there is no build. Continue anyway? [DANGEROUS]"):
        abort("Aborting at user request. Type \"fab build\" before deployment.")
    require('hosts', provided_by=[staging, prod])
    require('apppath', provided_by=[staging,prod])

    run("mkdir -p %svar" % env.apppath)
    #run("chmod 777 %s/var" % env.path)
    _put_dir('templates', env.apppath + 'templates')
    put('.htaccess',  env.apppath + '.htaccess')
    put('model.py',  env.apppath + 'model.py')
    put('site.py',  env.apppath + 'site.fcgi')
    put('firefoxize_starred_items.py', env.apppath + 'firefoxize_starred_items.py')

def deploy_static():
    if not os.path.exists(".build") and not confirm("Looks like there is no build. Continue anyway? [DANGEROUS]"):
        abort("Aborting at user request. Type \"fab build\" before deployment.")
        
    require('hosts', provided_by=[staging, prod])
    require('staticpath', provided_by=[staging,prod])
    _put_dir('static',  env.staticpath )

def clean():
    local("/bin/rm firefoxize_starred_items.py")
    local("/bin/rm .build")

