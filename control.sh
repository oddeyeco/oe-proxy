#!/usr/bin/env bash

### BEGIN INIT INFO
# Provides: oddeye.sh
# Required-Start: $local_fs $network
# Should-Start: ypbind nscd ldap ntpd xntpd
# Required-Stop: $network
# Default-Start:  2 3 4 5
# Default-Stop: 0 1 6
# Short-Description: start and stop TSD Client
# Description: TSD Client
### END INIT INFO#

SCRIPT_DIR="$(cd $(dirname $0) && pwd)"
PYTHON=`which python3`
cd $SCRIPT_DIR

function getValue {
    VALUE=`grep ^$1 conf/config.ini|  awk '{print $NF}'`
    if [ `echo $VALUE  | grep -o ':'` ] ; then VALUE=`echo $VALUE| cut -d ':' -f2` ; fi
    if [ `echo $VALUE  | grep -o '='` ] ; then VALUE=`echo $VALUE| cut -d '=' -f2` ; fi
    echo $VALUE
}

UsID=$(getValue uid)
USER=$(getent passwd $UsID | cut -d: -f1)
PIDFILE=$(getValue pid_file)
UWSGIPID=$(getValue pidfile)

    case "$1" in

    startweb)
    sbin/uwsgi  conf/config.ini
    ;;

    startd)
    su $USER -s /bin/bash -c "$PYTHON startd.py start"
    ;;

    stopweb)
    kill -9 $(cat $UWSGIPID )
    ;;

    stopd)
    su $USER -s /bin/bash -c "$PYTHON startd.py stop"
    ;;

    startall)
    $0 startweb
    sleep 1
    $0 startd
    ;;

    stopall)
    $0 stopweb
    sleep 1
    $0 stopd
    ;;

    restartweb)
    $0 stopweb
    $0 startweb
    ;;
    restard)
    $0 stopd
    $0 stard
    ;;
    restartall)
    $0 stopall
    $0 startall
    ;;

    *)
    echo "Usage: `basename $0` start | stop | restart"
    ;;

    esac
