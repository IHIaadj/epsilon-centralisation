 if [ -f /usr/pw/server/bin/setup_env.sh ]; then
        source /usr/pw/server/bin/setup_env.sh
    elif [ -f /etc/mcell/setup_env.sh ]; then
        source /etc/mcell/setup_env.sh
    else
        echo "setup_env.sh not found, exiting"
        exit 1
    fi
    mcstat -q -n "'"$i"'" | grep "Running"' || echo "Sorry"