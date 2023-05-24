uid=$(id -u $USER)
super=sudo

if [ $uid = 0 ]; then
    super=''
fi

exec $super rm /etc/systemd/system/light-control.service
exec $super systemctl daemon-reload
