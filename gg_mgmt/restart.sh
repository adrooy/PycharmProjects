#!/bin/bash
echo '--------------------------------before kill, all uwsgi process list:';
ps -ef | grep uwsgi | grep -v 'grep';
echo '----------------------';
ps -ef | grep uwsgi | grep gg_mgmt | grep -v 'grep' | awk '{print $2}' | xargs -i kill -3 {};
sleep 1
echo '--------------------------------after kill gg_mgmt, all uwsgi process list:';
ps -ef | grep uwsgi | grep -v 'grep';

echo '--------------------------------start new uwsgi:';
nohup /usr/bin/uwsgi /opt/www/gg_mgmt/django_uwsgi.ini --uid 500 --gid 500 &
sleep 1
echo '--------------------------------verify:';
ps -ef | grep uwsgi | grep -v 'grep';
