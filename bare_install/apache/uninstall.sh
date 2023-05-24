uid=$(id -u $USER)
super=sudo

if [ $uid = 0 ]; then
    super=''
fi

cd $(dirname $0)
cd ../../

source .env

eval $super rm -rf ${DBMS_ACCESS_PATH}
rm ${DBMS_PATH}/${DBMS_NAME}
eval $super
eval $super rm -rf /var/www/html/adminer

eval $super gpasswd -d www-data $(id -gn)
eval $super service php8.1-fpm restart

eval $super a2disconf adminer
eval $super service apache2 restart

rm -rf .venv
