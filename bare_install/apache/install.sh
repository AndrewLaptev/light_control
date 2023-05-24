uid=$(id -u $USER)
super=sudo

if [ $uid = 0 ]; then
    super=''
fi

cd $(dirname $0)
cd ../../

source .env

eval $super touch ${DBMS_PATH}/${DBMS_NAME}
eval $super chmod 777 -R ${DBMS_PATH}
eval $super mkdir -p ${DBMS_ACCESS_PATH}
eval $super chmod 777 ${DBMS_ACCESS_PATH}
ln -sf $(realpath ${DBMS_PATH})/${DBMS_NAME} ${DBMS_ACCESS_PATH}/${DBMS_NAME}

eval $super gpasswd -a www-data $(id -gn)
eval $super service php*-fpm restart

eval $super cp -r bare_install/adminer /var/www/html/
eval $super cp bare_install/apache/adminer.conf /etc/apache2/conf-available/
eval $super ln -sf /etc/apache2/conf-available/adminer.conf /etc/apache2/conf-enabled/adminer.conf
cp bare_install/apache/000-default.conf.src bare_install/apache/000-default.conf.apache.site

eval $super sed -i "s~DBMS_ADMINER_PASSWORD~${DBMS_ADMINER_PASSWORD}~" /var/www/html/adminer/index.php
sed -i "s~ROOT_PATH_UNSLASHED_END~${ROOT_PATH///}~" bare_install/apache/000-default.conf.apache.site
sed -i "s~ROOT_PATH~${ROOT_PATH}~" bare_install/apache/000-default.conf.apache.site
sed -i "s~LIGHT_CONTROL_PORT~${LIGHT_CONTROL_PORT}~" bare_install/apache/000-default.conf.apache.site

eval $super a2enmod proxy_http
eval $super a2enconf adminer
eval $super a2enconf php*-fpm
eval $super a2dismod mpm_event
eval $super a2enmod mpm_prefork
eval $super a2enconf php*

eval $super service apache2 restart

python3 -m venv .venv
source .venv/bin/activate

pip install .

echo
echo "Основная часть установки прошла успешно! Скопируйте данные из файла .apache.site к вашим настройкам Apache и перезагрузите сервер"
