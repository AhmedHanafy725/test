from subprocess import run, PIPE


def execute_cmd(cmd):
    response = run(cmd, shell=True, universal_newlines=True, stdout=PIPE, stderr=PIPE)
    return response

if __name__ == "__main__":
    cmd = 'ps -aux | grep "caddy" | awk "{print \$11}"'
    response = execute_cmd(cmd)
    if 'caddy' not in response.stdout:
        cmd = 'caddy -conf /mnt/data/Caddyfile &> /tmp/server1.log &'
        run(cmd, shell=True, timeout=10)
    
    cmd = 'ps -aux | grep "python3.6 /mnt/data/scripts/flask_server.py" | awk "{print \$11}"'
    response = execute_cmd(cmd)
    if 'python3.6' not in response.stdout:r2
        cmd = 'python3.6 /mnt/data/scripts/flask_server.py &> /tmp/serve.log &'
        run(cmd, shell=True, timeout=10)
