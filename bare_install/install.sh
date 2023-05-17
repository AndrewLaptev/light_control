cd $(dirname $0)
cd ../

source .env

sudo python3.10 -m venv .venv
source .venv/bin/activate

pip install .

sudo apt -y install adminer

sed -i "s~DBMS_ADMINER_PASSWORD~${DBMS_ADMINER_PASSWORD}~" bare_install/etc/adminer/conf.php
sed -i "s~ROOT_PATH_UNSLAHED_END~${ROOT_PATH///}~" bare_install/etc/apache2/sites-enabled/000-default.conf
sed -i "s~ROOT_PATH~${ROOT_PATH}~" bare_install/etc/apache2/sites-enabled/000-default.conf
sed -i "s~LIGHT_CONTROL_PORT~${LIGHT_CONTROL_PORT}~" bare_install/etc/apache2/sites-enabled/000-default.conf

sudo cp -r etc/adminer/* /etc/adminer/
sudo cp -r etc/apache2/sites-enabled/* /etc/apache2/sites-enabled/

sudo a2enmod proxy_http
sudo a2enconf adminer

sudo systemctl restart apache2.service
