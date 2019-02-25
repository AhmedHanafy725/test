set -e
apt-get update
apt-get install -y vim python3.6 curl git locales language-pack-en

# mount disk
mkfs.ext4 /dev/vda
mkdir /mnt/data
mount /dev/vda /mnt/data

#install docker 
apt-get install -y software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
apt-get update
apt-cache policy docker-ce
apt-get install -y docker-ce

# install caddy
mkdir /mnt/data/result
mkdir /mnt/data/scripts
curl https://getcaddy.com | bash -s personal

#load ssh
ssh-keygen -t rsa -N "" -f /root/.ssh/id_rsa -q -P ""
eval `ssh-agent`
ssh-add /root/.ssh/id_rsa

#install jumpscale
export LANGUAGE=en_US
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
git clone https://github.com/threefoldtech/jumpscaleX.git
python3.6 jumpscaleX/install/install.py -1 -y
rm -rf /sandbox/code/github/threefoldtech/jumpscaleX
cd /sandbox/code/github/threefoldtech/
git clone https://github.com/threefoldtech/jumpscaleX.git
cd jumpscaleX
git checkout development_testing
