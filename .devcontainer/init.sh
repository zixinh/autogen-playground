sudo apt-get update -y
sudo apt-get upgrade -y

sudo apt install python3-pip python3.11 python3-venv -y
python3 -m venv .venv
source .venv/bin/activate
pip install -r ./dev-requirements.txt

echo PYTHONPATH=./.venv/bin/python > .env