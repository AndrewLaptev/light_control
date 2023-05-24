uid=$(id -u $USER)
super=sudo

if [ $uid = 0 ]; then
    super=''
fi

cd $(dirname $0)
cd ../../

source .env

exec $super touch ${DBMS_PATH}/${DBMS_NAME}
exec $super chmod 777 -R ${DBMS_PATH}
exec $super mkdir -p ${DBMS_ACCESS_PATH}
exec $super chmod 777 ${DBMS_ACCESS_PATH}
ln -sf $(realpath ${DBMS_PATH})/${DBMS_NAME} ${DBMS_ACCESS_PATH}/${DBMS_NAME}

exec $super gpasswd -a www-data $(id -gn)
exec $super service php*-fpm restart

exec $super cp -r bare_install/adminer /var/www/html/
exec $super cp bare_install/apache/adminer.conf /etc/apache2/conf-available/
exec $super ln -sf /etc/apache2/conf-available/adminer.conf /etc/apache2/conf-enabled/adminer.conf
cp bare_install/apache/000-default.conf.src bare_install/apache/000-default.conf.apache.site

exec $super sed -i "s~DBMS_ADMINER_PASSWORD~${DBMS_ADMINER_PASSWORD}~" /var/www/html/adminer/index.php
sed -i "s~ROOT_PATH_UNSLASHED_END~${ROOT_PATH///}~" bare_install/apache/000-default.conf.apache.site
sed -i "s~ROOT_PATH~${ROOT_PATH}~" bare_install/apache/000-default.conf.apache.site
sed -i "s~LIGHT_CONTROL_PORT~${LIGHT_CONTROL_PORT}~" bare_install/apache/000-default.conf.apache.site

exec $super a2enmod proxy_http
exec $super a2enconf adminer
exec $super a2enconf php*-fpm
exec $super a2dismod mpm_event
exec $super a2enmod mpm_prefork
exec $super a2enconf php*

exec $super service apache2 restart

python3 -m venv .venv
source .venv/bin/activate

pip install .

echo
echo "Основная часть установки прошла успешно! Скопируйте данные из файла .apache.site к вашим настройкам Apache и перезагрузите сервер"
