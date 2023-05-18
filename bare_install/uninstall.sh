cd $(dirname $0)
cd ../

source .env

sudo rm -rf /dbms
rm volumes/dbms/${DBMS_NAME}
sudo rm -rf /etc/adminer/*

sudo apt -y remove adminer apache2
sudo dpkg -P adminer apache2

sudo apt -y autoremove

rm -rf .venv
