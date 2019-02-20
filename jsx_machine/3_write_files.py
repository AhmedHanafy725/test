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
            line = "ExecStart=/usr/bin/docker -g /mnt/data -H fd://\n" 
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
python3.6 /sandbox/code/github/threefoldtech/jumpscaleX/scripts/autotest.py
""".format(os.environ.get('telegram_chat_id'), os.environ.get('NACL_SECRET'), os.environ.get('public_ip'), os.environ.get('server_port'))

with open('/home/test.sh', 'w+') as f:
    f.write(test_script)

# crontab
crontab = "0 3-18 * * 0-5 bash /home/test.sh"
with open('/var/spool/cron/crontabs/root', 'w+') as f:
    f.write(crontab)

# caddy server
caddy = """:5050 {
	root /mnt/data/result
	browse
}
"""
with open('/mnt/data/Caddyfile', 'w+') as f:
    f.write(caddy)
