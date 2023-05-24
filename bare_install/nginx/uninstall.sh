uid=$(id -u $USER)
super=sudo

if [ $uid = 0 ]; then
    super=''
fi

cd $(dirname $0)
cd ../../

source .env

exec $super rm -rf ${DBMS_ACCESS_PATH}
rm ${DBMS_PATH}/${DBMS_NAME}
exec $super rm -rf /var/www/html/adminer

exec $super gpasswd -d www-data $(id -gn)
exec $super service php8.1-fpm restart

rm -rf .venv
