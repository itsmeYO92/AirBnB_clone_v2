#!/usr/bin/python3
""" Fabric script that transfer files to servers and extract them """


from fabric.api import env, put, run
from datetime import datetime
from os import path

env.hosts = ["34.232.71.74", "100.25.34.189"]


def do_deploy(archive_path):
    """ deploy the archive to the servers """
    try:   
        if not path.exists(archive_path):
            return False
    
        filename = archive_path.split('/')[-1]
        ne_filename = filename.split('.')[0]
    
        put(archive_path, "/tmp/{}".format(filename))
    
        folder = "/data/web_static/releases/{}/".format(ne_filename)
        run("sudo mkdir -p {}".format(folder))
        run ("sudo tar -xzf /tmp/{} -C {}".format(filename, folder))
        run("sudo rm /tmp/{}".format(filename))
        run("sudo mv {}web_static/* {}".format(folder, folder))
        run("sudo rm -rf {}web_static".format(folder))
        run('sudo rm -rf /data/web_static/current')
        run('sudo ln -s {} /data/web_static/current'.format(folder))
    except:
        return False

    return True
