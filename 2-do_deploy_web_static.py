#!/usr/bin/python3
"""
Fabric script based on the file 1-pack_web_static.py that distributes an
archive to the web servers
"""
from os.path import exists
from fabric.api import put, run, env, sudo

env.hosts = ["54.175.45.148", "52.207.249.170"]


def do_deploy(archive_path):
    """
    Distributes an archive to your web servers
    Returns False if the file at the path archive_path doesn't exist
    """
    if exists(archive_path) is False:
        return False
    
    filename = archive_path.split("/")[1]
    unfile = filename[0:-4]
    path = "/data/web_static/releases/"
    put(archive_path, "/tmp/")
    run("sudo mkdir -p {}{}".format(path, unfile))
    run("sudo tar -xzf /tmp/{} -C {}{}".format(filename, path, unfile))
    run("sudo rm -rf /tmp/{}".format(filename))
    run("sudo mv {0}{1}/web_static/* {0}{1}/".format(path, unfile))
    run("sudo rm -rf {}{}/web_static".format(path, unfile))
    run("sudo rm -rf /data/web_static/current")
    run("sudo ln -s {}{}/ /data/web_static/current".format(path, unfile))
    print("New version deployed!")
    sudo('service nginx restart')
    return True
