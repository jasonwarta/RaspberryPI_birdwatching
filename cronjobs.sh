# get temps every 20 minutes
*/20 * * * * /usr/bin/python /root/get_info.py

#start flask-powered video streaming server
@reboot nohup /usr/bin/python /root/streaming/app.py

#update time on reboot, as soon as network connectivity is established
@reboot while ! nc -z google.com 80 >/dev/null;do sleep 5;done; curl http://www.unixtimestamp.com/|grep "seconds since"|sed "s/.*\([0-9]\{10\}\).*/date -s '@\1'/"|/bin/bash

# start media capturing script
@reboot nohup /usr/bin/python /root/capture_media.py

# repackage movies into mp4 on a regular basis
*/10 * * * * /root/conv_vids.sh
