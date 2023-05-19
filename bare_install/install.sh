cd $(dirname $0)
cd ../

source .env

sudo apt -y install adminer

sudo touch ${DBMS_PATH}/${DBMS_NAME}
sudo chmod 777 -R ${DBMS_PATH}
sudo mkdir -p ${DBMS_ACCESS_PATH}
sudo chmod 777 ${DBMS_ACCESS_PATH}
ln -sf $(realpath ${DBMS_PATH})/${DBMS_NAME} ${DBMS_ACCESS_PATH}/${DBMS_NAME}

sudo gpasswd -a www-data $(id -gn)

sudo cp -r bare_install/etc/adminer/* /etc/adminer/
sudo cp -r bare_install/etc/apache2/sites-enabled/* /etc/apache2/sites-enabled/

sudo sed -i "s~DBMS_ADMINER_PASSWORD~${DBMS_ADMINER_PASSWORD}~" /etc/adminer/conf.php
sudo sed -i "s~ROOT_PATH_UNSLAHED_END~${ROOT_PATH///}~" /etc/apache2/sites-enabled/000-default.conf
sudo sed -i "s~ROOT_PATH~${ROOT_PATH}~" /etc/apache2/sites-enabled/000-default.conf
sudo sed -i "s~LIGHT_CONTROL_PORT~${LIGHT_CONTROL_PORT}~" /etc/apache2/sites-enabled/000-default.conf

sudo a2enmod proxy_http
sudo a2enconf adminer

sudo systemctl restart apache2.service

python3.10 -m venv .venv
source .venv/bin/activate

pip install .
