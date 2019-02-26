from zeroos.core0.client import Client
from subprocess import run, PIPE
from uuid import uuid4
import random
import os
import time


def load_ssh_key():
    home_user = os.path.expanduser('~')
    if os.path.exists('{}/.ssh/id_rsa.pub'.format(home_user)):
        with open('{}/.ssh/id_rsa.pub'.format(home_user), 'r') as file:
            ssh = file.readline().replace('\n', '')
    else:
        cmd = 'ssh-keygen -t rsa -N "" -f {}/.ssh/id_rsa -q -P ""; ssh-add {}/.ssh/id_rsa'.format(home_user, home_user)
        run(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        ssh = load_ssh_key()
    return ssh


def random_string():
    return str(uuid4()).replace('-', '')[:10]


def execute_command(cmd, ip='', port=22):
    target = "ssh -o 'StrictHostKeyChecking no' -p {} root@{} '{}'".format(port, ip, cmd)
    execute(target)
    # "response" has stderr, stdout and returncode(should be 0 in successful case)


def execute(cmd):
    response = run(cmd, shell=True, universal_newlines=True, stdout=PIPE, stderr=PIPE)
    if response.returncode:
        raise RuntimeError(response.stderr)


if __name__ == "__main__":

    jwt = os.environ.get('JWT')
    node_ip = os.environ.get('node_ip')
    cl = Client(node_ip, password=jwt)
    # create vm ubuntu 18.04
    ens4 = """network:
  version: 2
  renderer: networkd
  ethernets:
    ens4:
      dhcp4: true
      dhcp6: true"""
    ssh_key = load_ssh_key()
    disk_path = '/var/cache/jsx{}.qcow2'.format(random_string())
    disk_cmd = 'qemu-img create -f qcow2 {} 50G'.format(disk_path)
    cl.bash(disk_cmd).get()
    flist = 'https://hub.grid.tf/tf-bootable/ubuntu:18.04.flist'
    pub_port = random.randint(6000, 7000)
    server_port = random.randint(7000, 8000)
    port = {server_port: 5050, pub_port: 22, 6010: 6010}
    vm_uuid = cl.kvm.create(name='jsx_testing', flist=flist, port=port, memory=2048, nics=[{'type': 'default'}], config={
                            '/root/.ssh/authorized_keys': ssh_key, '/etc/netplan/ens4.yaml': ens4}, media=[{'url': disk_path}])
    time.sleep(30)

    # copy files to machine
    execute('scp -P {} 2_installation.sh root@{}:/home'.format(pub_port, node_ip))
    execute('scp -P {} 3_write_files.py root@{}:/home'.format(pub_port, node_ip))
    # run installation script
    execute_command(cmd='bash /home/2_installation.sh ', ip=node_ip, port=pub_port)
    # set the env
    public_ip = os.environ.get('public_ip')
    telegram_bot_token = os.environ.get('telegram_bot_token')
    telegram_chat_id = os.environ.get('telegram_chat_id')
    NACL_SECRET = os.environ.get('NACL_SECRET')
    username = os.environ.get('username')
    password = os.environ.get('password')
    cmd = 'export server_port={};\
           export public_ip={};\
           export telegram_bot_token={};\
           export telegram_chat_id={};\
           source /sandbox/env.sh;\
           export NACL_SECRET={};\
           export username={};\
           export password={};\
           python3.6 /home/3_write_files.py'.format(server_port, public_ip, telegram_bot_token, telegram_chat_id, NACL_SECRET, username, password)
    execute_command(cmd=cmd, ip=node_ip, port=pub_port)
