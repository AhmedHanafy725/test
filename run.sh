cd / 
git clone https://github.com/minio/mint.git
chmod 777 /mint
cd /mint

export MINT_ROOT_DIR=${MINT_ROOT_DIR:-/mint}
export MINT_RUN_CORE_DIR="$MINT_ROOT_DIR/run/core/minio-py"
export MINT_DATA_DIR=~/my-mint-dir
export MINT_MODE=core
export SERVER_ENDPOINT="192.168.192.253:1024"
export ACCESS_KEY="admin"
export SECRET_KEY="adminadmin"
export ENABLE_HTTPS=0
export SERVER_REGION=us-east-1
export MINIO_PY_VERSION=$(curl -s https://api.github.com/repos/minio/minio-py/releases/latest | jq -r .tag_name)

apt-get install python-pip
./create-data-files.sh
./build/minio-py/install.sh
export MINIO_PY_VERSION=$(curl -s https://api.github.com/repos/minio/minio-py/releases/latest | jq -r .tag_name)
wget -O $MINT_RUN_CORE_DIR/tests.py "https://raw.githubusercontent.com/minio/minio-py/${MINIO_PY_VERSION}/tests/functional/tests.py"
./run/core/minio-py/run.sh output.log error.log

wget https://raw.githubusercontent.com/AhmedHanafy725/test/master/format.py
python format.py
cp test.log /
rm -rf /mint 



