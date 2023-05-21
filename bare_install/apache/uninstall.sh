cd $(dirname $0)
cd ../../

source .env

sudo rm -rf ${DBMS_ACCESS_PATH}
rm ${DBMS_PATH}/${DBMS_NAME}
sudo rm -rf /var/www/html/adminer

sudo gpasswd -d www-data $(id -gn)
sudo service php8.1-fpm restart

sudo a2disconf adminer
sudo service apache2 restart

rm -rf .venv
