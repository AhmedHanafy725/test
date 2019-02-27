from flask import Flask, request
from subprocess import run
app = Flask(__name__)


@app.route('/', methods=["POST"])
def triggar(**kwargs):
    if request.json and request.json.get('ref') and request.json.get('pusher') and request.json.get('after'):
        if request.json['ref'][request.json['ref'].rfind('/') + 1:] == 'development':
            cmd = 'bash /mnt/data/scripts/test.sh {} {}'.format(request.json['pusher']['name'], request.json['after'])
            run(cmd, shell=True)
    return "Done", 201


@app.route('/', methods=["GET"])
def ping():
    return 'pong'


if __name__ == "__main__":
    app.run("0.0.0.0", 6010)
