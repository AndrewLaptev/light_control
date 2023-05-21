cd $(dirname $0)
cd ../../

source .env

sudo touch ${DBMS_PATH}/${DBMS_NAME}
sudo chmod 777 -R ${DBMS_PATH}
sudo mkdir -p ${DBMS_ACCESS_PATH}
sudo chmod 777 ${DBMS_ACCESS_PATH}
ln -sf $(realpath ${DBMS_PATH})/${DBMS_NAME} ${DBMS_ACCESS_PATH}/${DBMS_NAME}

sudo gpasswd -a www-data $(id -gn)
sudo service php*-fpm restart

sudo cp -r bare_install/adminer /var/www/html/
sudo cp bare_install/apache/adminer.conf /etc/apache2/conf-available/
sudo ln -sf /etc/apache2/conf-available/adminer.conf /etc/apache2/conf-enabled/adminer.conf
cp bare_install/apache/000-default.conf.src bare_install/apache/000-default.conf.apache.site

sudo sed -i "s~DBMS_ADMINER_PASSWORD~${DBMS_ADMINER_PASSWORD}~" /var/www/html/adminer/index.php
sed -i "s~ROOT_PATH_UNSLASHED_END~${ROOT_PATH///}~" bare_install/apache/000-default.conf.apache.site
sed -i "s~ROOT_PATH~${ROOT_PATH}~" bare_install/apache/000-default.conf.apache.site
sed -i "s~LIGHT_CONTROL_PORT~${LIGHT_CONTROL_PORT}~" bare_install/apache/000-default.conf.apache.site

sudo a2enmod proxy_http
sudo a2enconf adminer
sudo a2enconf php*-fpm
sudo a2dismod mpm_event
sudo a2enmod mpm_prefork
sudo a2enconf php*

sudo service apache2 restart

python3 -m venv .venv
source .venv/bin/activate

pip install .

echo
echo "Основная часть установки прошла успешно! Скопируйте данные из файла .apache.site к вашим настройкам Apache и перезагрузите сервер"