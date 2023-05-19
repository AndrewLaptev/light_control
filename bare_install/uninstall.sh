cd $(dirname $0)
cd ../

source .env

sudo rm -rf {$DBMS_ACCESS_PATH}
rm ${DBMS_PATH}/${DBMS_NAME}
sudo rm -rf /etc/adminer/*

sudo gpasswd -d www-data $(id -gn)

sudo apt -y remove adminer apache2
sudo dpkg -P adminer apache2

sudo apt -y autoremove

rm -rf .venv
