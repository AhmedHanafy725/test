from Jumpscale import j
from subprocess import run, PIPE
import os


# telegram bot
cl = j.clients.telegram_bot.get("test", bot_token_=os.environ.get('telegram_bot_token'))
cl.save()

# docker
run('systemctl stop docker', shell=True)
with open('/lib/systemd/system/docker.service', 'r') as f:
    lines = f.readlines()
with open('/lib/systemd/system/docker.service', 'w+') as f:
    for line in lines:
        if line.startswith('ExecStart=/usr/bin/docker'):
            line = "ExecStart=/usr/bin/dockerd -g /mnt/data -H fd://\n"
        f.write(line)

with open('/etc/default/docker', 'r') as f:
    lines = f.readlines()
with open('/etc/default/docker', 'w+') as f:
    for line in lines:
        if line.startswith('#DOCKER_OPTS='):
            line = 'DOCKER_OPTS="--dns 8.8.8.8 --dns 8.8.4.4 -g /mnt/data"'
        f.write(line)

run('systemctl daemon-reload', shell=True)
run('systemctl start docker', shell=True)

# test script
test_script = """set -e
source /sandbox/env.sh
cd /mnt/data/result
export chat_id=@{}
export Nacl={}
export ServerIp='http://{}:{}'
export name=$1
export commit=$2
python3.6 /sandbox/code/github/threefoldtech/jumpscaleX/scripts/autotest.py
""".format(os.environ.get('telegram_chat_id'), os.environ.get('NACL_SECRET'), os.environ.get('public_ip'), os.environ.get('server_port'))

with open('/mnt/data/scripts/test.sh', 'w+') as f:
    f.write(test_script)

# image build
build = """set -e
source /sandbox/env.sh
cd /mnt/data/result
export chat_id=@hamadarealtest
export ServerIp='http://188.165.233.148:7070'
python3.6 /sandbox/code/github/threefoldtech/jumpscaleX/scripts/build_image.py
"""

with open('/mnt/data/scripts/bulid.sh', 'w+') as f:
    f.write(test_script)

# night build for jumpscale image
crontab = "0 22 * * 0-5 bash /mnt/data/scripts/build.sh"
with open('/var/spool/cron/crontabs/root', 'w+') as f:
    f.write(crontab)

# caddy server
caddy = """:5050 {
	root /mnt/data/result
	browse
}
"""
with open('/mnt/data/scripts/Caddyfile', 'w+') as f:
    f.write(caddy)

# Flask server
flask = """from flask import Flask, request
from subprocess import run
app = Flask(__name__)

@app.route('/', methods=["POST"])
def triggar(**kwargs):
    if request.json['ref'][request.json['ref'].rfind('/') + 1:] == 'development':
        cmd = 'bash /home/test.sh {} {}'.format(request.json['pusher']['name'], request.json['after'])
        run(cmd, shell=True)
    return "Done", 201

@app.route('/', methods=["GET"])
def ping():
    return 'pong'

if __name__ == "__main__":
    app.run("0.0.0.0", 6010)
"""
with open('/mnt/data/scripts/flask_server.py', 'w+') as f:
    f.write(flask)

# Flask server
flask_server = """[Unit]
Description=Job that runs the python Flask server daemon

[Service]
Type=simple
WorkingDirectory=/home
ExecStart=/usr/bin/python3.6 /mnt/data/scripts/flask_server.py &
ExecStop=/bin/kill `/bin/ps aux | /bin/grep /mnt/data/scripts/flask_server.py | /bin/grep -v grep | /usr/bin/awk '{ print $2 }'`
Restart=on-abort

[Install]
WantedBy=multi-user.target"""

with open('/etc/systemd/system/flask_ser.service', 'w+') as f:
    f.write(flask_server)

# Caddy server
caddy_server = """[Unit]
Description=Job that runs the Caddy server daemon

[Service]
Type=simple
WorkingDirectory=/home
ExecStart=/usr/local/bin/caddy -log stdout -agree=true -conf=/mnt/data/scripts/Caddyfile -root=/var/tmp
ExecStop=/bin/kill `/bin/ps aux | /bin/grep caddy | /bin/grep -v grep | /usr/bin/awk '{ print $2 }'`
Restart=on-abort

[Install]
WantedBy=multi-user.target
"""

with open('/etc/systemd/system/caddy_server.service', 'w+') as f:
    f.write(caddy_server)

run('systemctl daemon-reload', shell=True)
run('systemctl start flask_ser.service', shell=True)
run('systemctl start caddy_server.service', shell=True)
