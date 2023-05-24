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
exec $super sed -i "s~DBMS_ADMINER_PASSWORD~${DBMS_ADMINER_PASSWORD}~" /var/www/html/adminer/index.php

cp bare_install/nginx/light_control.src bare_install/nginx/light_control.nginx.site
sed -i "s~ROOT_PATH_UNSLASHED_END~${ROOT_PATH///}~" bare_install/nginx/light_control.nginx.site
sed -i "s~ROOT_PATH~${ROOT_PATH}~" bare_install/nginx/light_control.nginx.site
sed -i "s~LIGHT_CONTROL_PORT~${LIGHT_CONTROL_PORT}~" bare_install/nginx/light_control.nginx.site

python3 -m venv .venv
source .venv/bin/activate

pip install .

echo
echo "Основная часть установки прошла успешно! Скопируйте данные из файла .nginx.site к вашим настройкам Nginx и перезагрузите сервер"
