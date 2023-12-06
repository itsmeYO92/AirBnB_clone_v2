#!/usr/bin/python3
""" Fabric script that generates a .tgz archive from the contents of the web_static """


from fabric.api import local
from datetime import date
from time import strftime

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
