uid=$(id -u $USER)
super=sudo

if [ $uid = 0 ]; then
    super=''
fi

cd $(dirname $0)
cd ../../

source .env


WORK_DIR_PATH=$(realpath .)

cp bare_install/systemd/light-control.service.src bare_install/systemd/light-control.service

sed -i "s~USER~${USER}~" bare_install/systemd/light-control.service
sed -i "s~WORK_DIR_PATH~${WORK_DIR_PATH}~" bare_install/systemd/light-control.service
sed -i "s~LIGHT_CONTROL_PORT~${LIGHT_CONTROL_PORT}~" bare_install/systemd/light-control.service

eval $super cp bare_install/systemd/light-control.service /etc/systemd/system/
eval $super chmod 755 /etc/systemd/system/light-control.service
eval $super systemctl daemon-reload

python3 -m venv .venv
source .venv/bin/activate

pip install .

eval $super systemctl enable light-control.service
eval $super systemctl start light-control.service

echo
echo "Установка завершена успешно! Веб-приложение запущено в качестве демона. 
Управлять им можно с помощью утилит systemctl или service по имени light-control"
