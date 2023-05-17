cd $(dirname $0)
cd ../

sudo rm -rf .venv

sudo apt -y remove adminer apache2
sudo dpkg -P adminer apache2

sudo apt -y autoremove
