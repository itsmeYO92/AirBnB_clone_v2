#!/usr/bin/python3
""" Fabric script that transfer files to servers and extract them """


from fabric.api import env, put, run, local
from datetime import date
from time import strftime
from os import path

env.hosts = ["34.232.71.74", "100.25.34.189"]


def do_pack():
    """ generates a .tgz archive from the contents of the web_static folder """

    time = strftime("%Y%m%d%H%M%S")
    local("mkdir -p versions")
    command = "tar -cvzf versions/web_static_{}.tgz web_static/".format(time)
    result = local(command)
    if result.failed:
        return None
    else:
        return "versions/web_static_{}.tgz".format(time)


def do_deploy(archive_path):
    """ deploy the archive to the servers """
    if not path.exists(archive_path):
        return False

    filename = archive_path.split('/')[-1]
    ne_filename = filename.split('.')[0]

    put(archive_path, "/tmp/{}".format(filename))

    folder = "/data/web_static/releases/{}/".format(ne_filename)
    if run("sudo mkdir -p {}".format(folder)).failed:
        return False
    if run ("sudo tar -xzf /tmp/{} -C {}".format(filename, folder)).failed:
        return False
    if run("sudo rm /tmp/{}".format(filename)).failed:
        return False
    if run("sudo mv {}web_static/* {}".format(folder, folder)).failed:
        return False
    if run("sudo rm -rf {}web_static".format(folder)).failed:
        return False
    if run('sudo rm -rf /data/web_static/current').failed:
        return False
    if run('sudo ln -s {} /data/web_static/current'.format(folder)).failed:
        return False

    return True


def deploy():
    """ fully deploy webstatic to servers """

    archive = do_pack()
    if not archive:
        return False
    return do_deploy(archive)
