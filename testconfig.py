import configparser

config = configparser.ConfigParser()
config.read('config.ini')
class Utils:
    def __init__(self):
        self.username = config['docker']['username']
        self.password = config['docker']['password']
        self.serverip = config['main']['server_ip']
        self.chat_id = config['main']['chat_id']
        self.commit = config['commit']['commit']
        self.commiter = config['commit']['commiter']
        self.nacl = config['main']['nacl']
        self.access_token = config['github']['access_token']
if __name__ == "__main__":
    test = Utils()
    print(test.username)
