uid=$(id -u $USER)
super=sudo

if [ $uid = 0 ]; then
    super=''
fi

eval $super systemctl stop light-control.service
eval $super systemctl disable light-control.service
eval $super rm /etc/systemd/system/light-control.service
eval $super systemctl daemon-reload
