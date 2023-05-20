cd $(dirname $0)
cd ../../

source .env

sudo apt install php8.1-fpm php8.1-sqlite3

sudo touch ${DBMS_PATH}/${DBMS_NAME}
sudo chmod 777 -R ${DBMS_PATH}
sudo mkdir -p ${DBMS_ACCESS_PATH}
sudo chmod 777 ${DBMS_ACCESS_PATH}
ln -sf $(realpath ${DBMS_PATH})/${DBMS_NAME} ${DBMS_ACCESS_PATH}/${DBMS_NAME}

sudo gpasswd -a www-data $(id -gn)

sudo cp -r bare_install/nginx/var/www/html/adminer /var/www/html/adminer
sudo sed -i "s~DBMS_ADMINER_PASSWORD~${DBMS_ADMINER_PASSWORD}~" /var/www/html/adminer/index.php

cp bare_install/nginx/etc/nginx/sites-enabled/light_control.src bare_install/nginx/etc/nginx/sites-enabled/light_control
sed -i "s~ROOT_PATH~${ROOT_PATH}~" bare_install/nginx/etc/nginx/sites-enabled/light_control
sed -i "s~LIGHT_CONTROL_PORT~${LIGHT_CONTROL_PORT}~" bare_install/nginx/etc/nginx/sites-enabled/light_control